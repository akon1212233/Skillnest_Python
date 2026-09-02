# 🌐 Lección 7 - Archivos Estáticos (Parte 1)

> **Curso:** Desarrollo Web con Flask desde Cero  
> **Unidad:** Archivos Estáticos (Static Files)  
> **Duración estimada:** 60 - 90 minutos

---

# 📖 Descripción General

Hasta este momento nuestras aplicaciones Flask han sido capaces de:

- Crear un servidor web.
- Definir rutas.
- Renderizar plantillas HTML utilizando Jinja2.
- Mostrar información dinámica proveniente del servidor.

Sin embargo, nuestras páginas todavía tienen un diseño muy simple.

En el desarrollo web profesional, una página no está formada únicamente por HTML.

Normalmente una aplicación también utiliza:

- 🎨 Hojas de estilo (CSS)
- ⚙️ Archivos JavaScript (JS)
- 🖼️ Imágenes
- 🔤 Fuentes personalizadas
- 🎥 Videos
- 🎵 Audios

Todos estos archivos reciben el nombre de **Archivos Estáticos (Static Files)**.

En Flask existe una carpeta especial llamada **static**, destinada exclusivamente para almacenar este tipo de recursos.

Durante esta lección aprenderemos a organizar correctamente estos archivos y enlazarlos con nuestras plantillas HTML.

---

# 🎯 Objetivos

Al finalizar esta lección serás capaz de:

- Comprender qué son los archivos estáticos.
- Diferenciar la carpeta **templates** de **static**.
- Organizar correctamente un proyecto Flask.
- Crear una hoja de estilos externa.
- Enlazar archivos CSS utilizando `url_for()`.
- Aplicar estilos a una plantilla HTML.

---

# 🤔 ¿Qué es un archivo estático?

Un archivo estático es cualquier recurso que el servidor entrega **sin modificar su contenido**.

Por ejemplo:

| Archivo | ¿Es estático? |
|----------|---------------|
| HTML generado con Jinja2 | ❌ No |
| CSS | ✅ Sí |
| JavaScript | ✅ Sí |
| Imagen PNG | ✅ Sí |
| Imagen JPG | ✅ Sí |
| Archivo PDF | ✅ Sí |
| Fuente (.ttf) | ✅ Sí |

---

## ¿Por qué se llaman "estáticos"?

Porque Flask simplemente los envía al navegador tal como están almacenados.

Por ejemplo.

Cuando solicitamos una hoja de estilos.

```
http://localhost:5000/static/css/style.css
```

Flask **no modifica** el archivo.

Simplemente lo entrega al navegador.

En cambio, una plantilla HTML sí es procesada por Jinja2 antes de ser enviada.

---

# 🧠 Templates vs Static

Una de las dudas más comunes al comenzar con Flask es la diferencia entre estas dos carpetas.

| Carpeta | Contenido | ¿Jinja2 la procesa? |
|----------|-----------|---------------------|
| **templates/** | Archivos HTML | ✅ Sí |
| **static/** | CSS, JS, imágenes, fuentes | ❌ No |

---

## Templates

Aquí colocaremos nuestras páginas HTML.

Ejemplo.

```text
templates/

│

├── index.html

├── ranking.html

└── contacto.html
```

Estas páginas pueden contener:

```jinja
{{ nombre }}

{% if %}

{% for %}
```

Porque son procesadas por Jinja2.

---

## Static

Aquí almacenaremos todos los recursos que complementan nuestra página.

```text
static/

│

├── css/

├── js/

├── img/

└── fonts/
```

Estos archivos **no son procesados por Flask**.

Simplemente son enviados al navegador.

---

# 📂 Estructura del proyecto

Trabajaremos sobre el siguiente proyecto.

```text
mi_proyecto/

│

├── app.py

│

├── templates/

│   └── index.html

│

└── static/

    │

    ├── css/

    │   └── style.css

    │

    ├── js/

    │

    └── img/
```

Observa que ahora el proyecto se encuentra mucho más organizado.

---

# 📝 Paso 1 - Crear la carpeta static

Dentro del proyecto crea la siguiente estructura.

```text
mi_proyecto/

│

├── app.py

│

├── templates/

│   └── index.html

│

└── static/

    │

    ├── css/

    ├── js/

    └── img/
```

---

# 🤔 ¿Por qué crear subcarpetas?

Aunque podríamos guardar todos los archivos directamente dentro de **static**, en proyectos reales esto dificultaría su organización.

Una buena práctica consiste en clasificarlos según su tipo.

| Carpeta | Contenido |
|----------|-----------|
| css | Hojas de estilo |
| js | JavaScript |
| img | Imágenes |
| fonts | Tipografías |

Esto facilita el mantenimiento del proyecto.

---

# 📝 Paso 2 - Crear la hoja de estilos

Dentro de:

```text
static/css/
```

crea el archivo.

```text
style.css
```

Agrega el siguiente código.

```css
/* ==========================
   Configuración general
========================== */

body{

    font-family: Arial, Helvetica, sans-serif;

    background-color: #f4f4f4;

    margin: 0;

    padding: 40px;

    text-align: center;

}


/* ==========================
   Título principal
========================== */

h1{

    color: #0d6efd;

}


/* ==========================
   Párrafos
========================== */

p{

    color: #555;

    font-size: 18px;

}
```

---

# 📝 Paso 3 - Crear la plantilla HTML

Dentro de la carpeta:

```text
templates
```

crea el archivo:

```text
index.html
```

Escribe el siguiente código.

```html
<!DOCTYPE html>
<html lang="es">

<head>

    <meta charset="UTF-8">

    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">

    <title>Archivos Estáticos</title>

</head>

<body>

    <h1>🚀 Mi primera página con CSS</h1>

    <p>

        Esta página utilizará una hoja de estilos ubicada
        en la carpeta <strong>static</strong>.

    </p>

</body>

</html>
```

Si ejecutaras el proyecto en este momento, la página aparecería sin estilos.

¿Por qué?

Porque todavía no hemos conectado el archivo CSS con el HTML.

---

# 📝 Paso 4 - Enlazar la hoja de estilos

Modifica el archivo **index.html** agregando la siguiente línea dentro del elemento `<head>`.

```html
<link rel="stylesheet"
      href="{{ url_for('static', filename='css/style.css') }}">
```

El archivo completo quedará así.

```html
<!DOCTYPE html>
<html lang="es">

<head>

    <meta charset="UTF-8">

    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">

    <title>Archivos Estáticos</title>

    <!-- Hoja de estilos -->

    <link rel="stylesheet"
          href="{{ url_for('static', filename='css/style.css') }}">

</head>

<body>

    <h1>🚀 Mi primera página con CSS</h1>

    <p>

        Esta página utilizará una hoja de estilos ubicada
        en la carpeta <strong>static</strong>.

    </p>

</body>

</html>
```

---

# 🔎 Analizando el enlace

Observa la siguiente línea.

```html
<link rel="stylesheet"
      href="{{ url_for('static', filename='css/style.css') }}">
```

Está compuesta por tres partes importantes.

### `rel="stylesheet"`

Indica al navegador que el archivo enlazado corresponde a una hoja de estilos CSS.

---

### `url_for()`

Es una función proporcionada por Flask.

Su objetivo es generar automáticamente la ruta correcta hacia un recurso.

---

### `filename`

Indica la ubicación del archivo dentro de la carpeta **static**.

En este caso.

```text
static/

└── css/

    └── style.css
```

Por eso escribimos.

```python
filename="css/style.css"
```

---

# 📝 Paso 5 - Crear el servidor Flask

Crea el archivo **app.py**.

Escribe el siguiente código.

```python
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def inicio():

    return render_template("index.html")


if __name__ == "__main__":

    app.run(debug=True)
```

---

# ▶️ Paso 6 - Ejecutar la aplicación

Activa el entorno virtual.

```bash
pipenv shell
```

Ejecuta Flask.

Windows.

```bash
python app.py
```

macOS.

```bash
python3 app.py
```

Abre el navegador.

```
http://localhost:5000/
```

---

# ✅ Resultado esperado

Si todos los pasos fueron realizados correctamente observarás:

- Un fondo gris claro.
- Un título azul.
- Texto centrado.
- Márgenes más amplios.
- Una página con mejor apariencia gracias al archivo CSS.

Si eliminas la línea.

```html
<link rel="stylesheet"
      href="{{ url_for('static', filename='css/style.css') }}">
```

y vuelves a cargar la página, observarás que desaparecen todos los estilos.

Esto demuestra que la hoja de estilos está siendo cargada correctamente desde la carpeta **static**.

---

# 🧠 Resumen

En esta primera parte aprendimos que:

- Los archivos estáticos no son procesados por Jinja2.
- Flask utiliza la carpeta **static** para almacenar recursos como CSS, JavaScript e imágenes.
- Es recomendable organizar estos archivos en subcarpetas (`css`, `js`, `img`, etc.).
- La función `url_for('static', filename=...)` permite enlazar archivos estáticos de forma segura y profesional.

---

# 🚀 Próxima Parte

En la siguiente parte aprenderemos a trabajar con:

- Archivos JavaScript.
- Imágenes.
- Organización profesional de recursos estáticos.
- Caché del navegador.
- Buenas prácticas para proyectos Flask.
- Una actividad práctica para aplicar todos estos conceptos.

# 🌐 Lección 7 - Archivos Estáticos (Parte 2)

> **Curso:** Desarrollo Web con Flask desde Cero  
> **Unidad:** Archivos Estáticos (Static Files)  
> **Duración estimada:** 60 - 90 minutos

---

# 📖 Descripción General

En la primera parte aprendimos qué son los archivos estáticos, cómo organizar la carpeta **static** y cómo enlazar una hoja de estilos CSS utilizando `url_for()`.

En esta segunda parte aprenderemos a trabajar con otros recursos estáticos muy utilizados en el desarrollo web:

- JavaScript.
- Imágenes.
- Organización profesional del proyecto.
- Caché del navegador.
- Buenas prácticas.

Al finalizar tendrás una estructura muy similar a la utilizada en proyectos profesionales con Flask.

---

# 🎯 Objetivos

Al finalizar esta lección serás capaz de:

- Enlazar archivos JavaScript.
- Mostrar imágenes almacenadas en la carpeta **static**.
- Comprender el funcionamiento de la caché del navegador.
- Organizar correctamente los recursos de un proyecto Flask.
- Aplicar buenas prácticas de desarrollo.

---

# 📂 Estructura final del proyecto

Al finalizar la lección, tu proyecto deberá quedar con la siguiente estructura.

```text
mi_proyecto/
│
├── app.py
│
├── templates/
│   └── index.html
│
└── static/
    │
    ├── css/
    │   └── style.css
    │
    ├── js/
    │   └── script.js
    │
    └── img/
        └── logo.png
```

---

# 📝 Paso 1 - Crear el archivo JavaScript

Dentro de la carpeta:

```text
static/js
```

crea un archivo llamado:

```text
script.js
```

Escribe el siguiente código.

```javascript
// Mensaje que se ejecuta al cargar la página

console.log("JavaScript cargado correctamente.");


// Mostrar un mensaje de bienvenida

alert("¡Bienvenido a Flask!");
```

---

# 📝 Paso 2 - Enlazar JavaScript

Abre nuevamente el archivo **templates/index.html**.

Agrega la siguiente línea antes del cierre del elemento `</body>`.

```html
<script src="{{ url_for('static', filename='js/script.js') }}"></script>
```

El archivo completo ahora será.

```html
<!DOCTYPE html>
<html lang="es">

<head>

    <meta charset="UTF-8">

    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">

    <title>Archivos Estáticos</title>

    <link rel="stylesheet"
          href="{{ url_for('static', filename='css/style.css') }}">

</head>

<body>

    <h1>🚀 Mi primera página con CSS y JavaScript</h1>

    <p>

        Flask permite organizar correctamente nuestros recursos
        utilizando la carpeta <strong>static</strong>.

    </p>

    <script src="{{ url_for('static', filename='js/script.js') }}"></script>

</body>

</html>
```

---

# 🔎 ¿Por qué el script se coloca al final?

Es una buena práctica colocar los archivos JavaScript antes del cierre de la etiqueta:

```html
</body>
```

De esta forma:

- Primero se carga el contenido HTML.
- Luego se ejecuta JavaScript.

Esto mejora la experiencia del usuario y evita problemas cuando el script necesita acceder a elementos del documento.

---

# 📝 Paso 3 - Agregar una imagen

Copia cualquier imagen dentro de la carpeta.

```text
static/img
```

Por ejemplo.

```text
logo.png
```

La estructura quedará.

```text
static/

└── img/

    └── logo.png
```

---

# 📝 Paso 4 - Mostrar la imagen

Agrega la siguiente línea debajo del título.

```html
<img src="{{ url_for('static', filename='img/logo.png') }}"
     alt="Logo Flask"
     width="250">
```

El archivo **index.html** quedará así.

```html
<!DOCTYPE html>
<html lang="es">

<head>

    <meta charset="UTF-8">

    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">

    <title>Archivos Estáticos</title>

    <link rel="stylesheet"
          href="{{ url_for('static', filename='css/style.css') }}">

</head>

<body>

    <h1>🚀 Mi primera página con CSS y JavaScript</h1>

    <img src="{{ url_for('static', filename='img/logo.png') }}"
         alt="Logo Flask"
         width="250">

    <p>

        Flask permite organizar correctamente nuestros recursos
        utilizando la carpeta <strong>static</strong>.

    </p>

    <script src="{{ url_for('static', filename='js/script.js') }}"></script>

</body>

</html>
```

---

# 🔎 Analizando la imagen

Observa la siguiente línea.

```html
<img src="{{ url_for('static', filename='img/logo.png') }}">
```

Funciona exactamente igual que el archivo CSS.

Flask interpreta.

```python
url_for(
    "static",
    filename="img/logo.png"
)
```

y genera automáticamente.

```text
/static/img/logo.png
```

---

# 📝 Paso 5 - Ejecutar el proyecto

Inicia nuevamente el servidor.

Windows.

```bash
python app.py
```

macOS.

```bash
python3 app.py
```

Abre el navegador.

```
http://localhost:5000/
```

---

# ✅ Resultado esperado

Si todo funciona correctamente deberías observar.

- Un título con estilos CSS.
- La imagen cargada desde la carpeta **static/img**.
- El mensaje emergente generado por JavaScript.
- Un mensaje en la consola del navegador.

---

# 📝 ¿Qué ocurre si modifico el CSS y no veo cambios?

Es posible que el navegador esté utilizando una versión almacenada del archivo.

Esto se conoce como **caché**.

La caché permite que las páginas carguen más rápido reutilizando archivos descargados anteriormente.

---

# 🔄 Actualización forzada

Si modificas:

- CSS
- JavaScript
- Imágenes

y los cambios no aparecen, realiza una actualización forzada.

## Windows

```text
Ctrl + Shift + R
```

o

```text
Ctrl + F5
```

---

## macOS

```text
Cmd + Shift + R
```

Esto obliga al navegador a descargar nuevamente los archivos estáticos.

---

# 💡 Buenas prácticas

Cuando desarrolles aplicaciones Flask procura seguir estas recomendaciones.

## ✅ Organiza tus recursos

```text
static/

├── css/

├── js/

├── img/

└── fonts/
```

Evita colocar todos los archivos directamente dentro de **static**.

---

## ✅ Utiliza nombres descriptivos

Correcto.

```text
style.css

login.css

dashboard.css
```

Incorrecto.

```text
archivo1.css

nuevo.css

estilos_final.css
```

---

## ✅ Usa siempre `url_for()`

Correcto.

```html
<link
href="{{ url_for('static', filename='css/style.css') }}">
```

Incorrecto.

```html
<link href="/static/css/style.css">
```

Aunque ambas opciones funcionan, `url_for()` es la recomendada porque Flask genera automáticamente la ruta correcta.

---

## ✅ Mantén separados los archivos

Cada tecnología debe tener su propio archivo.

- HTML → `templates`
- CSS → `static/css`
- JavaScript → `static/js`
- Imágenes → `static/img`

Esta organización facilita el mantenimiento del proyecto.

---

# 🧠 Resumen

En esta lección aprendimos que:

- La carpeta **static** almacena todos los recursos que no requieren procesamiento por parte del servidor.
- Los archivos CSS, JavaScript e imágenes se enlazan utilizando `url_for('static', filename=...)`.
- Es recomendable organizar los recursos en subcarpetas según su tipo.
- Los navegadores almacenan archivos estáticos en caché, por lo que puede ser necesario realizar una actualización forzada para visualizar los cambios.

---

# 📝 Actividad Práctica

## 🎯 Objetivo

Aplicar la organización de archivos estáticos creando una pequeña página web con HTML, CSS, JavaScript e imágenes.

---

## Instrucciones

Crea un nuevo proyecto Flask llamado:

```text
mi_portafolio
```

El proyecto debe contener la siguiente estructura.

```text
mi_portafolio/
│
├── app.py
│
├── templates/
│   └── index.html
│
└── static/
    │
    ├── css/
    │   └── style.css
    │
    ├── js/
    │   └── script.js
    │
    └── img/
        └── foto.jpg
```

---

## La página deberá contener:

- Un título principal.
- Una fotografía.
- Una breve descripción personal.
- Una hoja de estilos propia.
- Un archivo JavaScript que muestre un mensaje de bienvenida.
- Al menos tres estilos CSS diferentes (colores, márgenes, fuentes, etc.).

---

# 📸 Entregables

Cada estudiante deberá entregar.

- Proyecto completo.
- Archivo `app.py`.
- Carpeta `templates`.
- Carpeta `static`.
- Captura de la aplicación funcionando.
- Enlace al repositorio de GitHub.

---

# 🚀 Próxima Lección

Hasta ahora hemos construido aplicaciones que muestran información de forma dinámica utilizando Flask y Jinja2, además de incorporar recursos estáticos para mejorar su presentación.

En la siguiente unidad comenzaremos a trabajar con **formularios HTML**, permitiendo que los usuarios envíen información al servidor mediante solicitudes **GET** y **POST**, uno de los pilares del desarrollo de aplicaciones web interactivas.
Mostrando README.md