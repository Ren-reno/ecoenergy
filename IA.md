# Registro de uso de IA — EcoEnergy Monitor Fase 1

## 1. Herramienta utilizada

**Claude (Anthropic)**, a través de la interfaz de chat — utilizada para el diseño de la
estructura del proyecto y la generación/adaptación del código base (app Django, `utils.py`,
`views.py`, `urls.py`, templates Bootstrap).

**Google Gemini** — utilizada puntualmente para resolver dudas de teoría y para depurar
errores concretos que aparecieron al ejecutar el proyecto.

## 2. Prompts utilizados (resumen)

**Planificación y preparación (Claude)**

* Solicité convertir el enunciado de la evaluación a un archivo `.md` para tener el contexto siempre disponible durante el desarrollo.
* Pedí que me indicara qué conocimientos debía reforzar antes de empezar (Django, JSON, relaciones entre archivos, etc.).
* Pedí una guía general de los pasos a seguir para cumplir el enunciado completo.
* Consulté cómo verificar que el entorno virtual estuviera correctamente creado y activado.
* Pregunté qué librerías externas necesitaba para el alcance de la evaluación.

**Generación de código base (Claude)**

* Pedí que generara `zonas.json`, `categorias.json` y `dispositivos.json` cumpliendo los requisitos y relaciones (`zona_id`, `categoria_id`) especificados en el enunciado.
* Pedí el contenido de `utils.py` con la lógica de negocio pedida (carga y validación de JSON, relación entre zonas/dispositivos/categorías, cálculo de consumo, estado y margen disponible).
* Pedí el código de los templates `base.html`, `listado.html`, `detalle.html` y `404.html` siguiendo Bootstrap y los criterios de aceptación del enunciado.

**Resolución de errores durante el desarrollo (mixto)**

* Con Claude resolví cómo relacionar correctamente las rutas (`urls.py` con `app_name` y namespace `monitor:`) y qué archivos de configuración faltaba ajustar en `config/settings.py` (bloque `TEMPLATES`).
* Con Gemini consulté por qué la página 404 personalizada no aparecía y cómo se soluciona (relacionado con `DEBUG=True` mostrando el traceback de Django en vez de la plantilla propia), lo que llevó a configurar `DEBUG=False` y `ALLOWED_HOSTS`.
* Con Gemini resolví errores de encoding que aparecieron al leer los archivos JSON.
* Con Gemini pregunté qué significaban distintos mensajes de error que aparecían en la consola de Django durante las pruebas, para entender la causa antes de corregirlos.

**Documentación (Claude)**

* Pedí ayuda para redactar `README.md` y `ANALISIS.md`, incluyendo la tabla de rutas funcionales, la matriz de criterios de aceptación y el resumen de pruebas realizadas.
* Pedí que revisara y corrigiera la gramática y redacción de este mismo archivo (`IA.md`), manteniendo el contenido y las decisiones que yo había definido.

## 3. Partes utilizadas y cambios propios

**`utils.py`** **— corrección de lógica de negocio**
La versión inicial que propuso Claude dejaba el cálculo de la diferencia entre consumo y
límite resuelto directamente en el template, usando un encadenado de filtros Django
(`{{ zona.consumo_total|add:zona.limite_kwh|add:zona.limite_kwh|add:"-999999" }}`) que no
correspondía a ninguna fórmula real. Detecté que ese cálculo no tenía sentido matemático
(sumaba el límite dos veces y restaba una constante arbitraria) y lo reemplacé por un
cálculo correcto hecho en Python dentro de `obtener_detalle_zona()`, como
`margen_disponible = zona['limite_kwh'] - consumo_total`, devuelto ya resuelto en el
contexto de la vista. Esto además es consistente con CA-04 del enunciado, que exige que la
lógica de cálculo viva en la capa de datos y no en el template.

**`views.py`** **y** **`urls.py`**
Usados como base propuesta por Claude, adaptando el manejo de 404 (`raise Http404`) y el
namespace `monitor:` según lo exige CA-08.

**`monitor/urls.py`** **y** **`config/urls.py`** **— corrección de la ruta**
Inicialmente dejé el prefijo de la URL como `/monitoreo/`, siguiendo el nombre de la app
(`monitor`). Al revisar nuevamente el enunciado noté que explícitamente pedía que la ruta
fuera `/zonas/`, y que no me había fijado en ese detalle al integrar `urls.py`. Corregí el
`path()` en `config/urls.py` de `path('monitoreo/', include('monitor.urls'))` a
`path('zonas/', include('monitor.urls'))`, dejando el nombre interno de la app (`monitor`)
y `monitor/urls.py` sin cambios, pero ajustando la ruta pública para que cumpliera
literalmente lo pedido.

**`config/settings.py`**
Claude sugirió inicialmente dejar `DEBUG=True` por defecto (configuración estándar de
`startproject`). Al probar la página 404, noté (con ayuda de Gemini para interpretar el
error) que con `DEBUG=True` Django no muestra una página 404 real, sino su página de
depuración con el traceback completo. Cambié a `DEBUG=False`, agregué `ALLOWED_HOSTS`
(obligatorio cuando `DEBUG=False`) y creé un `templates/404.html` propio para que el error
se mostrara de forma controlada.

**Templates (****`base.html`****,** **`listado.html`****,** **`detalle.html`****,** **`404.html`****)**
Mantuve la estructura HTML y las clases Bootstrap propuestas por Claude sin cambios de
texto, color o disposición — la única modificación relevante en los templates fue eliminar
el filtro `|add:` inventado de `detalle.html` una vez que el cálculo se movió correctamente
a `utils.py`.

**Datos (****`zonas.json`****, **`categorias.json`****, **`dispositivos.json`****)**
Mantuve los valores generados por Claude (nombres de zonas, dispositivos, consumos y
límites), verificando que produjeran de forma natural al menos un caso ALERTA, casos NORMAL
y una zona sin dispositivos, según pedía el enunciado.

**`README.md`** **y** **`ANALISIS.md`**
Usé a Claude para redactar la estructura y el contenido de ambos documentos (instalación,
rutas funcionales, matriz de criterios de aceptación, resumen de pruebas). Revisé que cada
afirmación correspondiera a algo que realmente implementé y probé — en particular, corregí
las referencias a la ruta `/monitoreo/` por `/zonas/` en ambos documentos después de detectar
el error de prefijo descrito más abajo, para que la documentación quedara consistente con el
código final.

**Este archivo (****`IA.md`****)**
El contenido (prompts, decisiones y cambios propios) lo definí yo a partir de mi proceso
real de desarrollo; usé Claude únicamente para corregir gramática y redacción, sin que se
modificara la sustancia de lo declarado.

## 4. Verificación realizada

* Ejecuté `python manage.py check` después de cada cambio estructural, confirmando `System check identified no issues` antes de continuar a la siguiente etapa.
* Probé manualmente en `python manage.py shell` las funciones de `utils.py` antes de conectarlas a las vistas, confirmando que `obtener_detalle_zona(1)` devuelve `estado: 'ALERTA'`, `consumo_total: 575` y `margen_disponible: -25` — validando específicamente que la corrección de la fórmula (antes rota en el template) ahora calculaba el margen de forma coherente.
* Confirmé también que `obtener_detalle_zona(4)` (zona sin dispositivos) devuelve `dispositivos: []`, `consumo_total: 0` y `margen_disponible: 100` sin lanzar error.
* Verifiqué nuevamente el enunciado contra las rutas ya implementadas y detecté que había usado `/monitoreo/` en vez de `/zonas/` como pedía la evaluación; corregí `config/urls.py` y volví a probar `/zonas/`, `/zonas/1/`, `/zonas/4/` y `/zonas/99/` para confirmar que el cambio de prefijo no rompiera ninguna vista ni el manejo de 404.
* Probé en el navegador las rutas `/zonas/`, `/zonas/1/`, `/zonas/2/` y `/zonas/4/`, verificando que los estados NORMAL/ALERTA y el margen disponible se mostraran correctamente en cada tarjeta del detalle.
* Probé el caso de error `/zonas/99/`, confirmando que con `DEBUG=False` se muestra la página 404 propia (`templates/404.html`) y no el traceback técnico de Django — este fue el punto que verifiqué dos veces, primero con `DEBUG=True` (donde efectivamente aparecía el traceback) y luego con `DEBUG=False` ya corregido.
* Agregué temporalmente un dispositivo nuevo en `dispositivos.json` y confirmé que apareció en `/zonas/<id>/` sin modificar `views.py` ni los templates, verificando CA-06.
* Puedo explicar el funcionamiento completo de `utils.py`, `views.py` y los templates, incluyendo por qué se valida campo por campo en vez de contra un schema completo, cómo se calcula correctamente el estado y el margen disponible de cada zona (y por qué la versión original con filtros de template estaba mal), y por qué `DEBUG` debe quedar en `False` para la entrega.
