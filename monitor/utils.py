import json
from collections import defaultdict
from pathlib import Path

from jsonschema import Draft202012Validator

# Rutas a los archivos JSON
BASE_DIR = Path(__file__).resolve().parent.parent
FIXTURES_DIR = BASE_DIR / 'monitor' / 'fixtures'

RUTA_ZONAS = FIXTURES_DIR / 'zonas.json'
RUTA_CATEGORIAS = FIXTURES_DIR / 'categorias.json'
RUTA_DISPOSITIVOS = FIXTURES_DIR / 'dispositivos.json'

# Validadores por campo (no por archivo completo): cada campo declara
# el tipo que debe tener segun el enunciado.
CAMPOS_ZONA = {
    'id': Draft202012Validator({'type': 'integer'}),
    'nombre': Draft202012Validator({'type': 'string'}),
    'limite_kwh': Draft202012Validator({'type': 'number'}),
}

CAMPOS_CATEGORIA = {
    'id': Draft202012Validator({'type': 'integer'}),
    'nombre': Draft202012Validator({'type': 'string'}),
    'descripcion': Draft202012Validator({'type': 'string'}),
}

CAMPOS_DISPOSITIVO = {
    'id': Draft202012Validator({'type': 'integer'}),
    'nombre': Draft202012Validator({'type': 'string'}),
    'consumo_kwh': Draft202012Validator({'type': 'number'}),
    'zona_id': Draft202012Validator({'type': 'integer'}),
    'categoria_id': Draft202012Validator({'type': 'integer'}),
}


def _validar_registros(registros, campos_esperados, nombre_archivo):
    """
    Recorre cada registro y valida, campo por campo, que exista y que su
    tipo coincida con lo declarado en campos_esperados. Lanza ValueError
    con un mensaje puntual (archivo, registro, campo) si algo no calza.
    """
    for indice, registro in enumerate(registros):
        for campo, validador in campos_esperados.items():
            if campo not in registro:
                raise ValueError(
                    f"{nombre_archivo}: falta el campo '{campo}' en el registro {indice}."
                )
            errores = list(validador.iter_errors(registro[campo]))
            if errores:
                raise ValueError(
                    f"{nombre_archivo}: el campo '{campo}' del registro {indice} "
                    f"tiene un tipo invalido ({errores[0].message})."
                )
    return registros


def _leer_json(ruta, campos_esperados):
    """Lee un archivo JSON y valida cada registro campo por campo."""
    with open(ruta, encoding='utf-8') as archivo:
        contenido = json.load(archivo)
    return _validar_registros(contenido, campos_esperados, ruta.name)


def cargar_zonas():
    """Devuelve la lista de zonas leidas desde zonas.json."""
    return _leer_json(RUTA_ZONAS, CAMPOS_ZONA)


def cargar_categorias():
    """Devuelve la lista de categorias leidas desde categorias.json."""
    return _leer_json(RUTA_CATEGORIAS, CAMPOS_CATEGORIA)


def cargar_dispositivos():
    """Devuelve la lista de dispositivos leidos desde dispositivos.json."""
    return _leer_json(RUTA_DISPOSITIVOS, CAMPOS_DISPOSITIVO)


def _indexar_dispositivos_por_zona(dispositivos):
    """
    Agrupa los dispositivos por zona_id en un diccionario, para no recorrer
    la lista completa una vez por cada zona al armar listado o detalle.
    """
    indice = defaultdict(list)
    for dispositivo in dispositivos:
        indice[dispositivo['zona_id']].append(dispositivo)
    return indice


def listar_zonas_con_conteo():
    """
    Devuelve todas las zonas, cada una con su cantidad de dispositivos
    asociados. Se usa para el listado (CA-01, CA-02).
    """
    zonas = cargar_zonas()
    dispositivos_por_zona = _indexar_dispositivos_por_zona(cargar_dispositivos())

    return [
        {**zona, 'total_dispositivos': len(dispositivos_por_zona.get(zona['id'], []))}
        for zona in zonas
    ]


def obtener_detalle_zona(zona_id):
    """
    Busca una zona por id y arma su detalle: dispositivos con su categoria,
    consumo total, margen disponible y estado (NORMAL/ALERTA). Devuelve None
    si la zona no existe, para que la view responda 404 (CA-08).
    """
    zonas_por_id = {zona['id']: zona for zona in cargar_zonas()}
    zona = zonas_por_id.get(zona_id)
    if zona is None:
        return None

    categorias_por_id = {categoria['id']: categoria for categoria in cargar_categorias()}
    dispositivos_por_zona = _indexar_dispositivos_por_zona(cargar_dispositivos())

    dispositivos_detallados = []
    consumo_total = 0
    for dispositivo in dispositivos_por_zona.get(zona_id, []):
        categoria = categorias_por_id.get(dispositivo['categoria_id'])
        dispositivos_detallados.append({
            **dispositivo,
            'categoria_nombre': categoria['nombre'] if categoria else 'Sin categoria asignada',
        })
        consumo_total += dispositivo['consumo_kwh']

    return {
        **zona,
        'dispositivos': dispositivos_detallados,
        'consumo_total': consumo_total,
        'margen_disponible': zona['limite_kwh'] - consumo_total,
        'estado': 'ALERTA' if consumo_total > zona['limite_kwh'] else 'NORMAL',
    }