# 🌐 Lección 6 - Motor de Plantillas Jinja2 (Parte 1)
> **Curso:** Desarrollo Web con Flask desde Cero  
> **Unidad:** Renderizado de HTML con Jinja2  
> **Duración estimada:** 60 - 90 minutos

---

# 📖 Descripción General

Hasta este momento hemos desarrollado aplicaciones capaces de responder solicitudes HTTP utilizando únicamente **texto plano**.

Por ejemplo, cuando un usuario visita la ruta principal de nuestra aplicación:

```
http://localhost:5000/
```

Flask responde algo similar a:

```python
return "¡Hola Mundo!"
```

Aunque esto nos permitió comprender cómo funciona un servidor web, las aplicaciones profesionales funcionan de una manera muy diferente.

Cuando visitas sitios como:

- 🌎 Google
- ▶️ YouTube
- 📦 Mercado Libre
- 🏦 BancoEstado
- 📧 Gmail

el navegador no recibe únicamente texto.

Recibe documentos **HTML completos**, acompañados de hojas de estilo (CSS), archivos JavaScript e información generada dinámicamente desde el servidor.

La gran pregunta es:

> **¿Cómo puede Python insertar información dentro de un archivo HTML?**

La respuesta es mediante un **Motor de Plantillas**.

Durante esta lección aprenderemos a utilizar **Jinja2**, el motor de plantillas oficial de Flask, que nos permitirá conectar nuestro código Python con páginas HTML dinámicas.

A partir de esta clase comenzaremos a desarrollar aplicaciones web mucho más parecidas a las utilizadas en entornos profesionales.

---

# 🎯 Objetivos

Al finalizar esta lección serás capaz de:

- Comprender qué es un motor de plantillas.
- Entender por qué Flask utiliza Jinja2.
- Organizar correctamente un proyecto Flask.
- Crear la carpeta **templates**.
- Renderizar un archivo HTML mediante `render_template()`.
- Comprender el flujo entre Flask, Jinja2 y el navegador.

---

# ✅ Requisitos

Antes de comenzar verifica que tengas listo el proyecto desarrollado en las clases anteriores.

Debes contar con la siguiente estructura:

```text
hola_flask/
│
├── Pipfile
├── Pipfile.lock
└── server.py
```

Además, recuerda activar el entorno virtual antes de ejecutar cualquier aplicación.

```bash
pipenv shell
```

Si el entorno está activo observarás algo similar a:

```text
(hola_flask)
```

---

# 🤔 ¿Qué problema resuelve un Motor de Plantillas?

Imaginemos que queremos mostrar una página web utilizando únicamente Python.

Podríamos hacer algo como esto.

```python
@app.route("/")
def inicio():

    return """
    <h1>Bienvenido</h1>

    <p>Esta es mi primera página web.</p>
    """
```

Aunque funciona, rápidamente aparecen varios problemas.

- ❌ HTML mezclado con Python.
- ❌ Código difícil de mantener.
- ❌ Poco reutilizable.
- ❌ Difícil de leer.
- ❌ Poco profesional.

En proyectos pequeños esto puede parecer suficiente.

Sin embargo, imagina escribir una tienda online completa utilizando esta técnica.

Sería prácticamente imposible mantener el proyecto.

---

# 🏗️ Separando responsabilidades

Las aplicaciones profesionales dividen cada responsabilidad en un archivo distinto.

| Archivo       | Responsabilidad                   |
|---------------|-----------------------------------|
| **Python**    | Procesar la lógica del sistema.   |
| **HTML**      | Mostrar la información al usuario.|
| **CSS**       | Dar diseño y apariencia.          |
| **JavaScript**| Agregar interactividad.           |

Esta separación facilita el mantenimiento del proyecto y permite que distintos desarrolladores trabajen simultáneamente.

---

# 🧩 ¿Qué es Jinja2?

**Jinja2** es el motor de plantillas utilizado por Flask.

Su función consiste en:

1. Recibir un archivo HTML.
2. Recibir información enviada desde Python.
3. Reemplazar las variables dinámicas.
4. Generar un documento HTML final.
5. Enviarlo al navegador.

Es importante comprender que **el navegador nunca ejecuta código Python**.

Todo el procesamiento ocurre en el servidor.

---

# 🔄 Flujo de una aplicación con Jinja2

Cuando un usuario solicita una página web ocurre el siguiente proceso.

```text
               Usuario
                  │
                  ▼
           Navegador Web
                  │
          Solicitud HTTP
                  │
                  ▼
            Flask (Python)
                  │
          Procesa la lógica
                  │
                  ▼
        Motor de Plantillas
               Jinja2
                  │
     Genera el HTML final
                  │
                  ▼
          Navegador Web
```

Observa que Jinja2 actúa como un puente entre Python y HTML.

---

# 📂 Estructura del proyecto

Hasta ahora nuestro proyecto tenía la siguiente estructura.

```text
hola_flask/
│
├── Pipfile
├── Pipfile.lock
└── server.py
```

A partir de esta lección agregaremos una nueva carpeta.

```text
hola_flask/
│
├── Pipfile
├── Pipfile.lock
├── server.py
│
└── templates/
```

---

# 📌 ¿Por qué la carpeta debe llamarse "templates"?

Flask busca automáticamente todos los archivos HTML dentro de una carpeta llamada exactamente:

```text
templates
```

Si utilizamos otro nombre como:

```text
html
```

o

```text
vistas
```

Flask no podrá encontrar nuestros archivos.

Por esta razón **siempre** utilizaremos el nombre:

```text
templates
```

---

# 📝 Paso 1 - Crear la carpeta templates

Dentro de la carpeta **hola_flask** crea una nueva carpeta llamada:

```text
templates
```

La estructura ahora debe verse así.

```text
hola_flask/
│
├── Pipfile
├── Pipfile.lock
├── server.py
│
└── templates/
```

---

# 📝 Paso 2 - Crear nuestra primera plantilla

Dentro de la carpeta **templates** crea un archivo llamado:

```text
index.html
```

Con el siguiente contenido.

```html
<!DOCTYPE html>
<html lang="es">

<head>

    <meta charset="UTF-8">

    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Mi primera plantilla Flask</title>

</head>

<body>

    <h1>¡Bienvenido a Flask!</h1>

    <p>Esta es nuestra primera página HTML renderizada desde Flask.</p>

</body>

</html>
```

Observa que este archivo es un HTML completamente normal.

Todavía no contiene ninguna instrucción de Jinja2.

---

# 📝 Paso 3 - Modificar el servidor

Hasta ahora nuestro archivo **server.py** era muy similar a este.

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def inicio():

    return "Hola Mundo"

if __name__ == "__main__":

    app.run(debug=True)
```

Ahora debemos modificarlo.

El archivo completo debe quedar así.

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

# 🔍 Analizando el nuevo código

La única diferencia respecto a las lecciones anteriores es esta línea.

```python
from flask import Flask, render_template
```

Hemos agregado la función:

```python
render_template()
```

Esta función será la encargada de buscar nuestro archivo HTML y enviarlo al navegador.

---

# 📝 Paso 4 - ¿Qué hace render_template()?

Cuando escribimos:

```python
return render_template("index.html")
```

Flask realiza automáticamente las siguientes acciones.

1️⃣ Busca el archivo.

```text
templates/index.html
```

↓

2️⃣ Lo entrega al motor de plantillas Jinja2.

↓

3️⃣ Jinja2 procesa el archivo.

↓

4️⃣ Genera el HTML final.

↓

5️⃣ Flask envía la respuesta al navegador.

Todo esto ocurre en apenas unos milisegundos.

---

# ▶️ Paso 5 - Ejecutar la aplicación

Con el entorno virtual activado ejecuta:

## Windows

```bash
python server.py
```

## macOS

```bash
python3 server.py
```

Si todo salió correctamente observarás algo similar a:

```text
* Serving Flask app 'server'

* Debug mode: on

* Running on http://127.0.0.1:5000
```

---

# 🌐 Paso 6 - Abrir el navegador

Abre tu navegador favorito.

Escribe la siguiente dirección.

```
http://localhost:5000
```

También puedes utilizar.

```
http://127.0.0.1:5000
```

Ambas direcciones apuntan al mismo servidor.

---

# ✅ Resultado esperado

Si todos los pasos fueron realizados correctamente deberías observar una página muy similar a esta.

```text
¡Bienvenido a Flask!

Esta es nuestra primera página HTML renderizada desde Flask.
```

¡Felicidades!

Has renderizado tu primera plantilla HTML utilizando Flask.

---

# 🧠 ¿Qué ocurrió realmente?

Cuando escribiste:

```
http://localhost:5000
```

Flask ejecutó la siguiente función.

```python
@app.route("/")
def inicio():

    return render_template("index.html")
```

Luego buscó automáticamente.

```text
templates/index.html
```

Jinja2 procesó esa plantilla.

Finalmente Flask envió el HTML resultante al navegador.

El navegador nunca ejecutó Python.

Solo recibió un documento HTML completamente generado por el servidor.

---

# 📌 Conclusiones

En esta primera parte aprendimos que:

- Flask puede responder páginas HTML completas.
- Las plantillas HTML deben almacenarse dentro de una carpeta llamada **templates**.
- La función `render_template()` permite renderizar una plantilla y enviarla al navegador.
- Jinja2 es el motor encargado de procesar las plantillas antes de enviarlas al cliente.
- Flask y Jinja2 trabajan juntos para generar páginas web dinámicas.

Hasta este momento nuestras plantillas siguen siendo estáticas.

En la siguiente parte aprenderemos cómo enviar información desde Python al HTML para construir páginas completamente dinámicas.

---

# 🚀 Próxima Parte

En la segunda parte aprenderemos a:

- Enviar variables desde Python.
- Mostrar información utilizando `{{ }}`.
- Comprender la sintaxis básica de Jinja2.
- Utilizar estructuras condicionales (`if`).
- Utilizar ciclos (`for`).
- Construir las bases necesarias para desarrollar nuestro próximo proyecto: **Ranking de Jugadores**.


# 🌐 Lección 6 - Motor de Plantillas Jinja2 (Parte 2)
> **Curso:** Desarrollo Web con Flask desde Cero  
> **Unidad:** Renderizado de HTML con Jinja2  
> **Continuación de la Parte 1**

---

# 📖 Descripción General

En la primera parte aprendimos a renderizar nuestra primera plantilla HTML utilizando la función `render_template()`.

Sin embargo, la página que construimos sigue siendo **estática**, es decir, siempre muestra exactamente el mismo contenido.

Una de las principales ventajas de un servidor web es la capacidad de **generar contenido dinámico**.

Por ejemplo:

- Un usuario inicia sesión y aparece su nombre.
- Una tienda muestra diferentes productos.
- Un sistema escolar muestra los alumnos registrados.
- Una plataforma de videojuegos presenta el ranking actualizado de los jugadores.

Toda esa información proviene del servidor.

En esta segunda parte aprenderemos cómo **enviar información desde Flask hacia nuestras plantillas HTML** utilizando Jinja2.

---

# 🎯 Objetivos

Al finalizar esta lección serás capaz de:

- Enviar variables desde Flask hacia una plantilla HTML.
- Mostrar información dinámica mediante Jinja2.
- Comprender la sintaxis básica del motor de plantillas.
- Utilizar variables, condicionales y bucles.
- Aplicar buenas prácticas al trabajar con Jinja2.
- Prepararte para construir aplicaciones web completamente dinámicas.

---

# 🧠 ¿Cómo viaja la información?

Hasta ahora Flask solamente enviaba un archivo HTML.

```python
return render_template("index.html")
```

Ahora también podrá enviar datos.

```python
return render_template(
    "index.html",
    nombre="Daniel"
)
```

El flujo ahora será el siguiente.

```text
Python
    │
    │ nombre = "Daniel"
    ▼
render_template()
    │
    ▼
Jinja2
    │
    ▼
index.html
    │
    ▼
Navegador
```

Jinja recibe la variable, reemplaza su valor dentro del HTML y finalmente envía la página al navegador.

---

# 📤 Paso 1 - Enviar nuestra primera variable

Modifica el archivo **server.py**.

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def inicio():

    return render_template(
        "index.html",
        nombre="Daniel"
    )

if __name__ == "__main__":

    app.run(debug=True)
```

Observa que ahora `render_template()` recibe un segundo argumento.

```python
nombre="Daniel"
```

Estamos creando una variable llamada:

```
nombre
```

cuyo valor es:

```
Daniel
```

---

# 📥 Paso 2 - Mostrar la variable en HTML

Ahora abre el archivo:

```
templates/index.html
```

y reemplaza su contenido por el siguiente.

```html
<!DOCTYPE html>
<html lang="es">

<head>

    <meta charset="UTF-8">

    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">

    <title>Motor de Plantillas</title>

</head>

<body>

    <h1>Bienvenido {{ nombre }}</h1>

</body>

</html>
```

---

# 🤔 ¿Qué significa {{ nombre }}?

La expresión

```jinja
{{ nombre }}
```

indica a Jinja2 que debe mostrar el contenido de la variable llamada **nombre**.

Observa que:

- No es HTML.
- No es Python.
- Es sintaxis propia de Jinja2.

Cuando Flask renderiza la plantilla, Jinja reemplaza automáticamente esa expresión por el valor recibido.

El navegador finalmente recibe:

```html
<h1>Bienvenido Daniel</h1>
```

---

# ▶️ Resultado esperado

Al abrir el navegador.

```
http://localhost:5000
```

Deberías observar.

```text
Bienvenido Daniel
```

---

# 📤 Paso 3 - Enviar varias variables

Podemos enviar tantas variables como necesitemos.

Modifica la función.

```python
@app.route("/")
def inicio():

    return render_template(

        "index.html",

        nombre="Daniel",

        curso="Desarrollo Web con Flask",

        ciudad="Santiago",

        anio=2026

    )
```

---

# 📥 Mostrar todas las variables

Actualiza el HTML.

```html
<h1>{{ nombre }}</h1>

<p>Curso: {{ curso }}</p>

<p>Ciudad: {{ ciudad }}</p>

<p>Año: {{ anio }}</p>
```

Resultado.

```text
Daniel

Curso: Desarrollo Web con Flask

Ciudad: Santiago

Año: 2026
```

---

# 🏷️ Sintaxis de Jinja2

Jinja posee tres tipos principales de etiquetas.

| Sintaxis | Función |
|----------|----------|
| `{{ }}` | Mostrar información. |
| `{% %}` | Ejecutar lógica. |
| `{# #}` | Escribir comentarios. |

Las dos primeras serán las más utilizadas durante el curso.

---

# 📝 Mostrar información

Siempre que queramos mostrar una variable utilizaremos:

```jinja
{{ variable }}
```

Ejemplo.

```html
<h2>{{ nombre }}</h2>

<p>{{ ciudad }}</p>
```

---

# 📌 Comentarios

Jinja también permite escribir comentarios.

```jinja
{# Este comentario solamente existe en la plantilla #}
```

Estos comentarios no llegan al navegador.

---

# 🔀 Lógica con if

Otra característica importante de Jinja2 es la posibilidad de ejecutar estructuras condicionales.

Supongamos que enviamos desde Flask.

```python
return render_template(

    "index.html",

    nombre="Daniel",

    profesor=True

)
```

---

En la plantilla.

```html
{% if profesor %}

<p>Bienvenido profesor.</p>

{% endif %}
```

Como el valor recibido es `True`, el navegador mostrará.

```text
Bienvenido profesor.
```

---

# if - else

También podemos utilizar un bloque completo.

```html
{% if profesor %}

<p>Bienvenido profesor.</p>

{% else %}

<p>Bienvenido estudiante.</p>

{% endif %}
```

La sintaxis es muy similar a Python.

---

# 🔁 Bucles con for

Supongamos que enviamos una lista.

```python
return render_template(

    "index.html",

    tecnologias=[

        "Python",

        "Flask",

        "HTML",

        "CSS"

    ]

)
```

---

En la plantilla.

```html
<ul>

{% for tecnologia in tecnologias %}

    <li>{{ tecnologia }}</li>

{% endfor %}

</ul>
```

Resultado.

```text
• Python

• Flask

• HTML

• CSS
```

---

# 💼 Ejemplo real

Imaginemos que estamos desarrollando una plataforma de videojuegos.

Nuestro servidor envía.

```python
return render_template(

    "index.html",

    jugador="CyberWarrior",

    puntaje=9200,

    lider=True

)
```

La plantilla.

```html
<h1>{{ jugador }}</h1>

<p>Puntaje: {{ puntaje }}</p>

{% if lider %}

<p>🏆 Líder del Ranking</p>

{% endif %}
```

El navegador mostrará.

```text
CyberWarrior

Puntaje: 9200

🏆 Líder del Ranking
```

Este mismo principio será utilizado en la siguiente actividad del curso.

---

# ⚠️ Buenas prácticas

Jinja2 permite realizar muchas operaciones.

Sin embargo, debemos recordar una regla muy importante.

## ❌ Incorrecto

Realizar toda la lógica dentro del HTML.

```jinja
{% if %}
...

{% for %}

...

{% if %}

...

{% for %}

...
```

Las plantillas deben ser simples.

---

## ✅ Correcto

Python debe encargarse de:

- Consultar la base de datos.
- Validar información.
- Realizar cálculos.
- Preparar los datos.

Jinja solamente debe:

- Mostrar información.
- Repetir elementos.
- Mostrar u ocultar contenido.

Una buena regla es recordar.

> **Python procesa. Jinja presenta.**

---

# 🏗️ ¿Qué construiremos después?

En la siguiente actividad desarrollaremos un proyecto muy parecido a una aplicación real.

Construiremos un **Ranking de Jugadores**, donde el servidor enviará información como:

- Nombre del jugador.
- Puntaje.
- Posición.
- Estado del jugador.
- Cantidad de jugadores.

Todo ello será mostrado dinámicamente utilizando Jinja2.

Los conceptos aprendidos hoy serán la base para esa práctica.

---

# 🧠 Resumen

En esta segunda parte aprendimos que:

- `render_template()` permite enviar variables al HTML.
- `{{ }}` muestra información enviada desde Python.
- `{% %}` permite utilizar estructuras como `if` y `for`.
- `{# #}` permite escribir comentarios en las plantillas.
- Las plantillas deben contener únicamente la lógica necesaria para presentar información.
- La mayor parte del procesamiento debe permanecer en Python.

Con estos conocimientos ya estamos preparados para comenzar a construir páginas web dinámicas.

---

# 📝 Tarea

## 🎯 Objetivo

Crear una página HTML dinámica utilizando Jinja2 y aplicar los conceptos aprendidos durante la lección.

---

## Parte 1

Modifica tu proyecto para enviar las siguientes variables desde Flask.

```python
nombre

apellido

curso

institucion

anio
```

Muéstralas todas dentro de la plantilla HTML.

---

## Parte 2

Agrega una variable booleana.

```python
es_docente = True
```

Utiliza un bloque `if` para mostrar un mensaje diferente según el valor recibido.

---

## Parte 3

Envía una lista llamada `lenguajes`.

```python
lenguajes = [

    "Python",

    "Flask",

    "HTML",

    "CSS",

    "JavaScript"

]
```

Muéstrala utilizando un ciclo `for` dentro de una lista HTML (`<ul>`).

---

## Parte 4

Agrega un comentario utilizando la sintaxis de Jinja2.

```jinja
{# Comentario de prueba #}
```

Comprueba que dicho comentario no aparece en el navegador.

---

## Parte 5 (Desafío)

Diseña una página de bienvenida que contenga:

- Un título.
- Tu nombre completo.
- El nombre del curso.
- La institución.
- Una lista de tecnologías que conoces.
- Un mensaje diferente dependiendo si `es_docente` es verdadero o falso.

Organiza correctamente el contenido utilizando etiquetas HTML como:

- `<header>`
- `<main>`
- `<section>`
- `<footer>`

No te preocupes por el diseño; en las próximas lecciones aprenderemos a incorporar estilos con CSS.

---

# 📸 Evidencias

Entrega un documento con:

- Captura del archivo `server.py`.
- Captura del archivo `index.html`.
- Captura de la aplicación ejecutándose.
- Evidencia del uso de variables.
- Evidencia del uso del `if`.
- Evidencia del uso del `for`.

---

# 🚀 Próxima Actividad

En la siguiente práctica construiremos un **Ranking de Jugadores** completamente dinámico utilizando Flask y Jinja2, aplicando todos los conceptos aprendidos en esta lección para mostrar información desde el servidor en una interfaz HTML organizada y reutilizable.
Mostrando README.md