# Analisis — EcoEnergy Monitor Fase 1

## Relaciones y multiplicidades

* Una **Zona** contiene **0 o muchos Dispositivos** (1 : 0..*).
* Un **Dispositivo** pertenece a **una sola Zona** (relación mediante `zona_id`).
* Una **Categoría** clasifica **0 o muchos Dispositivos** (1 : 0..*).
* Un **Dispositivo** pertenece a **una sola Categoría** (relación mediante `categoria_id`).

Las relaciones no utilizan claves foráneas de una base de datos. Se resuelven en Python mediante los identificadores presentes en los archivos JSON. Los dispositivos se indexan por `zona_id` mediante un diccionario (`defaultdict`) y las categorías se buscan mediante un diccionario indexado por su `id`.

## Claves de conexión

| Archivo             | Clave propia | Clave(s) que referencia a otros archivos                           |
| ------------------- | ------------ | ------------------------------------------------------------------ |
| `zonas.json`        | `id`         | —                                                                  |
| `categorias.json`   | `id`         | —                                                                  |
| `dispositivos.json` | `id`         | `zona_id` → `zonas.json.id`, `categoria_id` → `categorias.json.id` |

## Matriz de criterios de aceptación

| Criterio | Archivo/Componente                                                                         | Prueba realizada                                                                                                                                                                                     |
| -------- | ------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| CA-01    | `views.py` (`vista_listado`), `utils.py` (`listar_zonas_con_conteo`)                       | Se verificó que `/zonas/` muestra las 4 zonas registradas en `zonas.json`.                                                                                                                           |
| CA-02    | `listado.html`                                                                             | Cada tarjeta muestra nombre, límite, cantidad de dispositivos y botón "Ver detalle".                                                                                                                 |
| CA-03    | `detalle.html`, `utils.py` (`obtener_detalle_zona`)                                        | El detalle muestra dispositivos, categoría, consumo total, margen disponible y estado de cada zona.                                                                                                  |
| CA-04    | `utils.py`                                                                                 | Los conteos, el consumo total, el margen disponible y el estado se calculan en Python mediante estructuras y operaciones de datos, sin realizar cálculos en el HTML ni mediante filtros de template. |
| CA-05    | `utils.py` (`'ALERTA' if consumo_total > zona['limite_kwh'] else 'NORMAL'`)                | Se probó con Planta Industrial (575 > 550 → ALERTA) y Oficinas Administrativas (25 < 80 → NORMAL).                                                                                                   |
| CA-06    | `dispositivos.json`, `utils.py`                                                            | Se agregaron dispositivos nuevos al JSON y aparecieron automáticamente en la interfaz sin modificar `views.py` ni los templates.                                                                     |
| CA-07    | `detalle.html` (bloque `{% else %}`)                                                       | Depósito Anexo Sur no tiene dispositivos asociados en el JSON y muestra el mensaje "Esta zona todavía no tiene dispositivos registrados".                                                            |
| CA-08    | `views.py` (`raise Http404`), `config/settings.py` (`DEBUG = False`), `templates/404.html` | Se probó `/zonas/99/` con un ID inexistente: Django respondió con código 404 y mostró la página personalizada sin exponer un traceback.                                                              |
| CA-09    | `base.html`, `listado.html`, `detalle.html`                                                | Se agregaron zonas y dispositivos y se comprobó que la navegación y la interfaz se mantuvieron accesibles.                                                                                           |
| CA-10    | `detalle.html` (`table-responsive` + altura máxima con scroll)                             | La tabla de dispositivos permite desplazamiento horizontal y vertical sin desbordar la página.                                                                                                       |
| CA-11    | `base.html`                                                                                | El encabezado, la navegación y las tarjetas utilizan componentes y clases Bootstrap de manera consistente (`navbar`, `card`, `badge`).                                                               |
| CA-12    | `detalle.html` (badges con texto "NORMAL"/"ALERTA" + color)                                | El estado de la zona se comunica mediante texto y color, evitando depender únicamente del color.                                                                                                     |
| CA-13    | Proyecto completo                                                                          | Se ejecutó `python manage.py check` sin errores de configuración.                                                                                                                                    |

## Lógica de estados

El estado de una zona se determina comparando el consumo total de sus dispositivos con el límite de consumo establecido:

* **NORMAL:** el consumo total es menor o igual al límite establecido.
* **ALERTA:** el consumo total supera el límite establecido.

Por ejemplo:

* Planta Industrial: `575 kWh > 550 kWh` → **ALERTA**.
* Oficinas Administrativas: `25 kWh < 80 kWh` → **NORMAL**.
* Centro de Distribución: `355 kWh < 400 kWh` → **NORMAL**.
* Depósito Anexo Sur: `0 dispositivos` → muestra el estado vacío correspondiente.

## Alcance respetado

No se implementaron Models, migraciones, ORM, CRUD, formularios, autenticación ni soft delete, conforme al alcance obligatorio del enunciado.

Toda la lógica de datos se resuelve mediante estructuras Python, como diccionarios, listas y comprensiones de listas, utilizando los archivos JSON como fuente de datos.

La aplicación permite consultar las zonas y sus dispositivos sin utilizar una base de datos ni un sistema de persistencia adicional.
