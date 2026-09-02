# 🏆 Desafío 1 - Ranking de Jugadores (Parte 1)

## 📖 Descripción

En este desafío construiremos nuestra primera aplicación web dinámica utilizando Flask y Jinja2.

El objetivo será mostrar un ranking de jugadores utilizando información enviada desde el servidor hacia una plantilla HTML.

Durante esta primera parte prepararemos el proyecto, construiremos el servidor Flask y renderizaremos nuestra primera plantilla.

En la siguiente parte utilizaremos Jinja2 para mostrar dinámicamente los jugadores.

---

# 🎯 Objetivos

Al finalizar esta práctica serás capaz de:

- Crear un nuevo proyecto Flask.
- Organizar correctamente la estructura del proyecto.
- Enviar información desde Flask hacia una plantilla HTML.
- Comprender cómo viajan los datos desde Python hasta el navegador.

---

# 📝 Paso 1 - Crear el proyecto

Crea una carpeta llamada:

```text
ranking_game
```

Abre esta carpeta utilizando **Visual Studio Code**.

---

# 📝 Paso 2 - Crear el entorno virtual

Abre una terminal.

Instala Flask utilizando Pipenv.

```bash
pipenv install flask
```

Una vez finalizada la instalación activa el entorno virtual.

```bash
pipenv shell
```

Si todo salió correctamente deberías observar algo similar a:

```text
(ranking_game)
```

---

# 📝 Paso 3 - Crear la estructura del proyecto

Dentro de la carpeta crea la siguiente estructura.

```text
ranking_game/
│
├── app.py
│
└── templates/
    │
    └── ranking.html
```

---

# 📝 Paso 4 - Crear el servidor Flask

Abre el archivo **app.py** y escribe el siguiente código.

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/ranking")
def ranking():

    return render_template("ranking.html")

if __name__ == "__main__":

    app.run(debug=True)
```

---

## ¿Qué hace este código?

- Importa Flask.
- Crea la aplicación.
- Define la ruta **/ranking**.
- Renderiza el archivo **ranking.html**.
- Ejecuta el servidor.

Por el momento todavía no enviamos información al HTML.

---

# 📝 Paso 5 - Crear la plantilla HTML

Abre el archivo:

```
templates/ranking.html
```

Escribe el siguiente código.

```html
<!DOCTYPE html>
<html lang="es">

<head>

    <meta charset="UTF-8">

    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">

    <title>Ranking de Jugadores</title>

</head>

<body>

    <h1>🏆 Ranking de Jugadores</h1>

    <p>Bienvenido a nuestro ranking.</p>

</body>

</html>
```

---

# 📝 Paso 6 - Ejecutar el proyecto

Con el entorno virtual activo ejecuta.

Windows

```bash
python app.py
```

macOS

```bash
python3 app.py
```

Abre el navegador.

```
http://localhost:5000/ranking
```

Deberías obtener un resultado similar a este.

```
🏆 Ranking de Jugadores

Bienvenido a nuestro ranking.
```

Si obtienes este resultado significa que Flask encontró correctamente la carpeta **templates**, renderizó el archivo HTML y lo envió al navegador.

---

# 📝 Paso 7 - Agregar los datos del servidor

Ahora modificaremos **app.py** para que el servidor tenga información de los jugadores.

Reemplaza completamente el contenido del archivo por el siguiente código.

```python
from flask import Flask, render_template

app = Flask(__name__)

jugadores = [

    {
        "nombre": "AlexGamer",
        "puntaje": 5000
    },

    {
        "nombre": "PixelMaster",
        "puntaje": 7500
    },

    {
        "nombre": "ShadowNinja",
        "puntaje": 8200
    },

    {
        "nombre": "CyberWarrior",
        "puntaje": 9100
    },

    {
        "nombre": "UltraNoob",
        "puntaje": 3000
    }

]

@app.route("/ranking")
def ranking():

    return render_template(

        "ranking.html",

        jugadores=jugadores

    )

if __name__ == "__main__":

    app.run(debug=True)
```

---

## ¿Qué cambió?

Ahora existe una nueva variable.

```python
jugadores
```

Esta variable contiene una lista de diccionarios.

Cada diccionario representa un jugador.

Por ejemplo.

```python
{
    "nombre": "AlexGamer",
    "puntaje": 5000
}
```

Finalmente, la lista completa se envía hacia la plantilla mediante:

```python
return render_template(
    "ranking.html",
    jugadores=jugadores
)
```

En este momento el HTML ya está recibiendo la información.

Sin embargo, todavía no sabemos cómo mostrarla.

Eso lo haremos en la siguiente parte utilizando **Jinja2**.

---

# ✅ Resultado esperado

Si vuelves a ejecutar el servidor observarás exactamente la misma página.

¿Por qué?

Porque aunque Flask ya está enviando la lista de jugadores, el archivo **ranking.html** todavía no contiene instrucciones para mostrarla.

En la siguiente parte aprenderemos a utilizar:

- `{{ }}`
- `{% for %}`
- `{% if %}`

para construir completamente el ranking dinámico.

# 🏆 Desafío 1 - Ranking de Jugadores (Parte 2)

## 📖 Descripción

En la primera parte dejamos preparado nuestro proyecto Flask y enviamos una lista de jugadores desde el servidor hacia la plantilla HTML.

Sin embargo, aunque la información ya está disponible, todavía no aparece en la página.

En esta segunda parte utilizaremos **Jinja2** para recorrer la lista de jugadores y mostrarla dinámicamente en el navegador.

Además, aprenderemos a utilizar:

- Bucles `for`
- Variables de Jinja
- `loop.index`
- Condicionales `if`

---

# 🎯 Objetivos

Al finalizar esta práctica serás capaz de:

- Recorrer listas utilizando Jinja2.
- Mostrar información dinámica enviada desde Flask.
- Destacar elementos utilizando condicionales.
- Comprender cómo funciona `loop.index`.
- Construir una interfaz dinámica utilizando HTML y CSS.

---

# 📝 Paso 1 - Actualizar la plantilla HTML

Ahora reemplaza completamente el contenido de **templates/ranking.html** por el siguiente código.

```html
<!DOCTYPE html>
<html lang="es">

<head>

    <meta charset="UTF-8">

    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">

    <title>Ranking de Jugadores</title>

    <style>

        body{
            font-family: Arial, Helvetica, sans-serif;
            background:#f4f4f4;
            text-align:center;
            padding:40px;
        }

        h1{
            color:#333;
        }

        .ranking{

            width:600px;
            margin:auto;

            background:white;

            border-radius:10px;

            box-shadow:0 4px 10px rgba(0,0,0,.2);

            overflow:hidden;

        }

        ul{

            list-style:none;

            margin:0;

            padding:0;

        }

        li{

            display:flex;

            justify-content:space-between;

            padding:15px;

            border-bottom:1px solid #ddd;

            font-size:18px;

        }

        .lider{

            background:#fff8dc;

            font-weight:bold;

            color:darkgoldenrod;

        }

    </style>

</head>

<body>

<h1>🏆 Ranking de Jugadores</h1>

<div class="ranking">

<ul>

{% for jugador in jugadores %}

<li>

<span>

{{ jugador.nombre }}

</span>

<span>

{{ jugador.puntaje }} pts

</span>

</li>

{% endfor %}

</ul>

</div>

</body>

</html>
```

---

## ¿Qué cambió?

Antes nuestro HTML solamente tenía un título.

Ahora aparece un bloque muy importante.

```jinja
{% for jugador in jugadores %}

...

{% endfor %}
```

Este ciclo recorre todos los jugadores enviados desde Flask.

Cada vez que encuentra uno, crea automáticamente un nuevo elemento `<li>`.

---

# 📝 Paso 2 - Ejecutar nuevamente el proyecto

Ejecuta nuevamente el servidor.

```bash
python app.py
```

Abre el navegador.

```
http://localhost:5000/ranking
```

Ahora deberías obtener un resultado parecido al siguiente.

```
AlexGamer ........... 5000 pts

PixelMaster ......... 7500 pts

ShadowNinja ......... 8200 pts

CyberWarrior ........ 9100 pts

UltraNoob ........... 3000 pts
```

¡Nuestro primer listado dinámico ya está funcionando!

---

# 📝 Paso 3 - Mostrar la posición del jugador

Jinja posee una variable especial llamada:

```jinja
loop.index
```

Esta variable indica la posición actual del ciclo.

Modifica únicamente el contenido del `<li>`.

Reemplaza esto.

```jinja
<span>

{{ jugador.nombre }}

</span>
```

Por esto.

```jinja
<span>

{{ loop.index }}.

{{ jugador.nombre }}

</span>
```

---

## Resultado esperado

Ahora el navegador mostrará.

```
1. AlexGamer

2. PixelMaster

3. ShadowNinja

4. CyberWarrior

5. UltraNoob
```

No fue necesario crear un contador.

Jinja lo hace automáticamente.

---

# 📝 Paso 4 - Destacar al primer lugar

Ahora utilizaremos un condicional.

Modifica la etiqueta `<li>`.

Reemplaza.

```html
<li>
```

por

```jinja
<li

{% if loop.index == 1 %}

class="lider"

{% endif %}

>
```

---

## ¿Qué significa esto?

Mientras el ciclo recorre la lista, preguntamos:

```jinja
¿Estoy en la posición 1?
```

Si la respuesta es **Sí**, Jinja agrega automáticamente.

```html
class="lider"
```

Gracias al CSS definido anteriormente, ese jugador aparecerá resaltado.

---

# 📝 Paso 5 - Mostrar el total de jugadores

Debajo del listado agrega.

```html
<h3>

Total de jugadores:

{{ jugadores|length }}

</h3>
```

---

## ¿Qué significa `|length`?

Jinja posee filtros.

Uno de ellos es:

```jinja
length
```

Este filtro obtiene la cantidad de elementos de una lista.

En este caso devolverá.

```
5
```

---

# 📝 Paso 6 - Código completo actualizado

Ahora el archivo **ranking.html** debe quedar exactamente así.

```html
<!DOCTYPE html>
<html lang="es">

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<title>Ranking de Jugadores</title>

<style>

body{
font-family:Arial, Helvetica, sans-serif;
background:#f4f4f4;
text-align:center;
padding:40px;
}

.ranking{
width:600px;
margin:auto;
background:white;
border-radius:10px;
box-shadow:0 4px 10px rgba(0,0,0,.2);
overflow:hidden;
}

ul{
list-style:none;
margin:0;
padding:0;
}

li{
display:flex;
justify-content:space-between;
padding:15px;
border-bottom:1px solid #ddd;
font-size:18px;
}

.lider{
background:#fff8dc;
font-weight:bold;
color:darkgoldenrod;
}

</style>

</head>

<body>

<h1>🏆 Ranking de Jugadores</h1>

<div class="ranking">

<ul>

{% for jugador in jugadores %}

<li

{% if loop.index == 1 %}

class="lider"

{% endif %}

>

<span>

{{ loop.index }}.

{{ jugador.nombre }}

</span>

<span>

{{ jugador.puntaje }} pts

</span>

</li>

{% endfor %}

</ul>

</div>

<h3>

Total de jugadores:

{{ jugadores|length }}

</h3>

</body>

</html>
```

---

# 🧠 ¿Qué aprendimos?

En esta parte utilizamos varios elementos nuevos de Jinja2.

| Sintaxis | Función |
|----------|----------|
| `{{ variable }}` | Mostrar información. |
| `{% for %}` | Recorrer listas. |
| `{% if %}` | Tomar decisiones. |
| `loop.index` | Obtener la posición actual del ciclo. |
| `|length` | Obtener la cantidad de elementos de una lista. |

---

# 📝 Desafío

Realiza las siguientes mejoras en tu aplicación.

### 1️⃣ Agrega un nuevo atributo a cada jugador.

Por ejemplo.

```python
pais
```

Muéstralo en el ranking.

---

### 2️⃣ Agrega un nuevo atributo.

```python
nivel
```

Muéstralo junto al puntaje.

---

### 3️⃣ Modifica el CSS.

Cambia:

- Colores.
- Tipografía.
- Tamaño del ranking.
- Bordes.

Haz que tenga un diseño propio.

---

### 4️⃣ Destaca también el segundo y tercer lugar.

Puedes utilizar nuevos estilos CSS.

Por ejemplo.

- 🥇 Oro
- 🥈 Plata
- 🥉 Bronce

---

### 5️⃣ Investiga

¿Qué otra información ofrece la variable especial `loop` de Jinja2 además de `loop.index`?

Escribe al menos **tres propiedades** e indica para qué sirven.

---

# 📸 Evidencias

Entrega:

- Proyecto completo.
- Archivo `app.py`.
- Carpeta `templates`.
- Archivo `ranking.html`.
- Captura de la aplicación funcionando.
- Enlace al repositorio de GitHub.

---

# 🚀 Próxima Parte

En la siguiente parte agregaremos nuevas rutas dinámicas para que el usuario pueda:

- Mostrar solamente los primeros **N jugadores**.
- Cambiar el color de fondo desde la URL.
- Reutilizar la misma plantilla HTML para mostrar distintos resultados sin duplicar código.

Con esto construiremos una aplicación mucho más flexible y cercana a un entorno profesional.

# 🏆 Desafío 1 - Ranking de Jugadores (Parte 3)

## 📖 Descripción

Hasta este momento nuestra aplicación muestra correctamente el ranking de todos los jugadores.

Sin embargo, las aplicaciones web modernas suelen permitir mostrar únicamente parte de la información o personalizar la visualización según las preferencias del usuario.

En esta última parte agregaremos dos nuevas funcionalidades:

- Mostrar solamente los primeros **N jugadores**.
- Cambiar el color de fondo de la página mediante la URL.

Todo esto reutilizando la misma plantilla HTML.

---

# 🎯 Objetivos

Al finalizar esta práctica serás capaz de:

- Crear rutas dinámicas con parámetros.
- Utilizar convertidores de tipo (`int`).
- Enviar distintas variables a una misma plantilla.
- Reutilizar una plantilla HTML sin duplicar código.
- Personalizar la apariencia mediante Jinja2.

---

# 📝 Paso 1 - Crear una ruta para limitar la cantidad de jugadores

Hasta ahora nuestro archivo **app.py** contiene únicamente una ruta.

Vamos a agregar una nueva.

Reemplaza completamente el contenido de **app.py** por el siguiente código.

```python
from flask import Flask, render_template

app = Flask(__name__)

jugadores = [

    {"nombre": "AlexGamer", "puntaje": 5000},
    {"nombre": "PixelMaster", "puntaje": 7500},
    {"nombre": "ShadowNinja", "puntaje": 8200},
    {"nombre": "CyberWarrior", "puntaje": 9100},
    {"nombre": "UltraNoob", "puntaje": 3000}

]

@app.route("/ranking")
def ranking():

    return render_template(
        "ranking.html",
        jugadores=jugadores,
        color=None
    )


@app.route("/ranking/<int:cantidad>")
def ranking_limitado(cantidad):

    return render_template(
        "ranking.html",
        jugadores=jugadores[:cantidad],
        color=None
    )


if __name__ == "__main__":
    app.run(debug=True)
```

---

## 🧠 ¿Qué cambió?

Agregamos una nueva ruta.

```python
@app.route("/ranking/<int:cantidad>")
```

Esta ruta recibe un número entero desde la URL.

Por ejemplo.

```
/ranking/3
```

La variable

```python
cantidad
```

tendrá el valor

```python
3
```

Luego utilizamos un **slice** de Python.

```python
jugadores[:cantidad]
```

para enviar solamente esa cantidad de jugadores.

---

# ▶️ Prueba

Ejecuta nuevamente el servidor.

Abre las siguientes direcciones.

```
http://localhost:5000/ranking
```

Mostrará los **5 jugadores**.

Ahora prueba.

```
http://localhost:5000/ranking/3
```

Resultado esperado.

```
🥇 AlexGamer

🥈 PixelMaster

🥉 ShadowNinja
```

Observa que **no modificamos el HTML**.

La misma plantilla sirve para ambos casos.

---

# 📝 Paso 2 - Personalizar el color del fondo

Ahora agregaremos una tercera ruta.

Vuelve a reemplazar completamente el archivo **app.py** por el siguiente código.

```python
from flask import Flask, render_template

app = Flask(__name__)

jugadores = [

    {"nombre": "AlexGamer", "puntaje": 5000},
    {"nombre": "PixelMaster", "puntaje": 7500},
    {"nombre": "ShadowNinja", "puntaje": 8200},
    {"nombre": "CyberWarrior", "puntaje": 9100},
    {"nombre": "UltraNoob", "puntaje": 3000}

]

@app.route("/ranking")
def ranking():

    return render_template(
        "ranking.html",
        jugadores=jugadores,
        color=None
    )


@app.route("/ranking/<int:cantidad>")
def ranking_limitado(cantidad):

    return render_template(
        "ranking.html",
        jugadores=jugadores[:cantidad],
        color=None
    )


@app.route("/ranking/<int:cantidad>/<color>")
def ranking_color(cantidad, color):

    return render_template(
        "ranking.html",
        jugadores=jugadores[:cantidad],
        color=color
    )


if __name__ == "__main__":
    app.run(debug=True)
```

---

## 🧠 ¿Qué cambió?

Ahora enviamos una nueva variable.

```python
color
```

Su contenido dependerá de la URL.

Por ejemplo.

```
/ranking/5/red
```

enviará

```python
color="red"
```

---

# 📝 Paso 3 - Actualizar la plantilla

Ahora reemplaza completamente el archivo **templates/ranking.html** por el siguiente código.

```html
<!DOCTYPE html>
<html lang="es">

<head>

<meta charset="UTF-8">

<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Ranking de Jugadores</title>

<style>

body{

font-family:Arial, Helvetica, sans-serif;

background-color:
{% if color %}
{{ color }}
{% else %}
#f4f4f4
{% endif %};

text-align:center;

padding:40px;

}

.ranking{

width:600px;

margin:auto;

background:white;

border-radius:10px;

box-shadow:0 4px 10px rgba(0,0,0,.2);

overflow:hidden;

}

ul{

list-style:none;

padding:0;

margin:0;

}

li{

display:flex;

justify-content:space-between;

padding:15px;

border-bottom:1px solid #ddd;

font-size:18px;

}

.lider{

background:#fff8dc;

font-weight:bold;

color:darkgoldenrod;

}

</style>

</head>

<body>

<h1>🏆 Ranking de Jugadores</h1>

<div class="ranking">

<ul>

{% for jugador in jugadores %}

<li

{% if loop.index == 1 %}

class="lider"

{% endif %}

>

<span>

{{ loop.index }}.
{{ jugador.nombre }}

</span>

<span>

{{ jugador.puntaje }} pts

</span>

</li>

{% endfor %}

</ul>

</div>

<h3>

Total de jugadores:

{{ jugadores|length }}

</h3>

</body>

</html>
```

---

# 🧠 ¿Qué cambió?

Observa el CSS.

```jinja
background-color:

{% if color %}

{{ color }}

{% else %}

#f4f4f4

{% endif %}
```

Este bloque pregunta:

> ¿Existe una variable llamada `color`?

Si existe.

Utiliza ese color.

Si no existe.

Utiliza el gris claro por defecto.

---

# ▶️ Pruebas

Prueba las siguientes rutas.

## Ranking completo

```
http://localhost:5000/ranking
```

---

## Mostrar tres jugadores

```
http://localhost:5000/ranking/3
```

---

## Mostrar tres jugadores con fondo azul

```
http://localhost:5000/ranking/3/lightblue
```

---

## Mostrar cinco jugadores con fondo rojo

```
http://localhost:5000/ranking/5/red
```

---

## Mostrar cuatro jugadores con fondo negro

```
http://localhost:5000/ranking/4/black
```

Prueba distintos colores válidos de CSS como:

- red
- green
- blue
- pink
- orange
- purple
- lightgray
- lightgreen
- gold

---

# 🧠 Resultado final

Ahora una misma plantilla HTML puede generar múltiples resultados.

| URL | Resultado |
|------|-----------|
| `/ranking` | Muestra todos los jugadores. |
| `/ranking/3` | Muestra los tres primeros jugadores. |
| `/ranking/5/red` | Muestra cinco jugadores con fondo rojo. |
| `/ranking/2/lightblue` | Muestra dos jugadores con fondo celeste. |

Este es uno de los grandes beneficios de trabajar con **Flask** y **Jinja2**: reutilizar una misma plantilla para distintos escenarios sin duplicar código.

---

# 📝 Desafío Final

Realiza las siguientes mejoras utilizando los conocimientos adquiridos.

### 1️⃣ Agrega una nueva propiedad

Cada jugador debe tener:

```python
nivel
```

Muéstralo en el ranking.

---

### 2️⃣ Agrega un país

```python
pais
```

Muestra el país debajo del nombre.

---

### 3️⃣ Personaliza el primer, segundo y tercer lugar

Utiliza diferentes colores para:

- 🥇 Oro
- 🥈 Plata
- 🥉 Bronce

---

### 4️⃣ Mensaje cuando no existan jugadores

Investiga cómo mostrar un mensaje utilizando Jinja cuando la lista esté vacía.

Ejemplo.

```
No existen jugadores registrados.
```

---

### 5️⃣ Investigación

Investiga qué hacen las siguientes propiedades de `loop`.

- `loop.first`
- `loop.last`
- `loop.length`

Explica brevemente para qué sirven y en qué situaciones podrían utilizarse.

---

# 📦 Entregables

Cada estudiante deberá entregar:

- Proyecto completo.
- Archivo `app.py`.
- Carpeta `templates`.
- Archivo `ranking.html`.
- Archivo `README.md` explicando el funcionamiento de la aplicación.
- Repositorio en GitHub correctamente organizado.

---

# 🏁 Conclusión

En este desafío desarrollaste tu primera aplicación web dinámica utilizando Flask y Jinja2.

Durante la práctica aplicaste conceptos fundamentales del desarrollo web:

- Creación de rutas.
- Rutas dinámicas.
- Renderizado de plantillas.
- Variables enviadas desde Python.
- Listas y diccionarios.
- Bucles `for`.
- Condicionales `if`.
- Parámetros en la URL.
- Personalización dinámica del contenido.

Estos mismos conceptos serán utilizados en las siguientes unidades, donde reemplazaremos la lista de jugadores por información almacenada en una **base de datos MySQL**, permitiendo construir aplicaciones mucho más completas y cercanas a un entorno profesional.
Mostrando README.md 