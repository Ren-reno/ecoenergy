# EcoEnergy Monitor — Fase 1

Panel interno que permite a EcoEnergy consultar sus zonas de consumo energético y el detalle de los dispositivos instalados en cada una, utilizando archivos JSON como fuente de datos.

## Requisitos

* Python 3.11 o superior
* pip

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/Ren-reno/ecoenergy
cd ecoenergy
```

### 2. Crear y activar el entorno virtual

**Windows PowerShell:**

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

**Linux:**

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

## Ejecución

Antes de iniciar el servidor, se puede verificar que el proyecto no tenga errores de configuración:

```bash
python manage.py check
```

Luego, iniciar el servidor de desarrollo:

```bash
python manage.py runserver
```

La aplicación estará disponible en:

`http://127.0.0.1:8000/`

## Rutas funcionales

| Ruta           | Descripción                                                                                                                                             |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `/zonas/`      | Lista todas las zonas registradas, mostrando su límite de consumo y la cantidad de dispositivos.                                                        |
| `/zonas/<id>/` | Muestra el detalle de una zona, incluyendo dispositivos, categoría, consumo total, margen disponible y estado (`NORMAL`/`ALERTA`).                      |
| `/zonas/<id>/` | Si el ID de la zona no existe, responde con un error 404 mediante una página personalizada, sin exponer información de depuración cuando `DEBUG=False`. |

## Datos

Los datos de la aplicación se almacenan en tres archivos JSON ubicados dentro de `monitor/fixtures/`:

* `zonas.json` — Contiene el ID, nombre y límite de consumo en kWh de cada zona.
* `categorias.json` — Contiene el ID, nombre y descripción de cada categoría.
* `dispositivos.json` — Contiene el ID, nombre, consumo en kWh, ID de zona e ID de categoría de cada dispositivo.

## Lógica de estados

El estado de cada zona se determina comparando el consumo total de sus dispositivos con el límite de consumo establecido:

* **NORMAL:** el consumo total se encuentra dentro del límite establecido.
* **ALERTA:** el consumo total supera el límite establecido.

## Pruebas realizadas

* Se verificó que el listado de zonas muestra correctamente las **4 zonas registradas**, incluyendo una zona sin dispositivos.

* Se comprobó que el detalle de las zonas muestra correctamente los estados:

  * **NORMAL:** Oficinas Administrativas.
  * **NORMAL:** Centro de Distribución.
  * **ALERTA:** Planta Industrial, con un consumo de **575 kWh**, superando el límite de **550 kWh**.

* Se probó la zona sin dispositivos (**Depósito Anexo Sur**), mostrando correctamente el mensaje:

  > Esta zona todavía no tiene dispositivos registrados.

* Se probó el acceso a una zona inexistente mediante `/zonas/99/`, obteniendo una respuesta **404** con una página personalizada y sin exponer un traceback, utilizando `DEBUG=False`.

* Se agregaron nuevos dispositivos al archivo JSON y se comprobó que estos aparecen automáticamente en la interfaz sin necesidad de modificar el código de las vistas.

## Dependencias externas

El proyecto utiliza `jsonschema` para validar los datos antes de procesarlos.

La validación comprueba el tipo de cada campo de los registros de los archivos JSON. No se utiliza un único esquema para validar el archivo completo, sino que la validación se realiza sobre cada campo de cada registro.

## Tecnologías utilizadas

* **Python**
* **Django**
* **JSON**
* **jsonschema**
* **HTML/CSS**
* **Git/GitHub**


