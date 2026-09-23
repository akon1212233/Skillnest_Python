# 📚 Lección 11 - Envío de Formularios con el método POST

> **Curso:** Desarrollo Web con Flask desde Cero  
> **Unidad:** Formularios HTML y Solicitudes HTTP  
> **Tema:** Envío de información desde el navegador hacia el servidor utilizando el método **POST**.

---

# 📖 Descripción General

Hasta este momento, todas las aplicaciones que hemos desarrollado tienen un comportamiento similar:

- El navegador solicita una página al servidor.
- Flask procesa la solicitud.
- El servidor responde enviando un archivo HTML.
- El usuario únicamente visualiza información.

En otras palabras, el flujo de información siempre ha sido:

```text
Servidor
    │
    │ Envía información
    ▼
Navegador
```

Sin embargo, las aplicaciones web modernas requieren que el usuario pueda **interactuar** con ellas.

Por ejemplo:

- Registrarse en una página.
- Iniciar sesión.
- Escribir un comentario.
- Completar una encuesta.
- Crear un nuevo producto.
- Actualizar información.
- Enviar un mensaje.

Todas estas acciones tienen algo en común:

👉 **El usuario debe enviar información al servidor.**

La forma más común de realizar esta tarea es mediante **formularios HTML**.

En esta lección aprenderemos cómo crear formularios y cómo Flask recibe la información ingresada por el usuario.

---

# 🎯 Objetivos

Al finalizar esta lección serás capaz de:

- Comprender qué es un formulario HTML.
- Diferenciar las solicitudes **GET** y **POST**.
- Crear formularios HTML.
- Configurar rutas Flask para recibir formularios.
- Utilizar el objeto `request`.
- Acceder a la información enviada mediante `request.form`.
- Redireccionar al usuario utilizando `redirect()`.

---

# 🧠 Antes de comenzar...

Hasta ahora hemos trabajado únicamente con solicitudes **GET**.

Cuando escribimos una dirección como:

```
http://127.0.0.1:5000/
```

el navegador realiza automáticamente una solicitud GET.

Visualmente el proceso es el siguiente.

```text
Cliente (Navegador)

        │

        │ GET /

        ▼

Servidor Flask

        │

        │ HTML

        ▼

Cliente
```

El navegador **solicita información**.

El servidor **responde con información**.

---

# 🤔 ¿Qué ocurre cuando el usuario desea enviar información?

Imaginemos el siguiente formulario.

```
Nombre

____________________

Correo

____________________

[ Crear Usuario ]
```

Ahora el navegador ya no necesita pedir información.

Necesita **enviarla**.

El flujo cambia completamente.

```text
Usuario

      │

Escribe información

      │

      ▼

Formulario HTML

      │

      │ POST

      ▼

Servidor Flask

      │

Procesa la información

      ▼

Respuesta
```

Este tipo de comunicación recibe el nombre de **Solicitud POST**.

---

# 🌎 GET vs POST

Aunque existen muchos métodos HTTP, los dos más utilizados son:

| Método | ¿Para qué se utiliza? |
|---------|------------------------|
| GET | Solicitar información al servidor. |
| POST | Enviar información al servidor. |

Ejemplos.

### GET

```
Ver una noticia.

Abrir una página.

Mostrar un producto.

Ver un listado.
```

---

### POST

```
Crear una cuenta.

Enviar un comentario.

Registrar un estudiante.

Guardar un producto.

Iniciar sesión.
```

---

# 📌 ¿Por qué no utilizar GET para todo?

Imaginemos un formulario de registro.

```
Nombre

Correo

Contraseña
```

Si enviáramos esta información mediante GET, los datos aparecerían en la URL.

Ejemplo.

```
http://localhost:5000/crear_usuario?nombre=Juan&correo=juan@gmail.com
```

Esto no es recomendable porque:

- La información queda visible.
- Puede almacenarse en el historial del navegador.
- Puede compartirse accidentalmente.

Por ello utilizaremos **POST**, donde los datos viajan en el cuerpo de la solicitud.

---

# 📁 Estructura del proyecto

Crea una nueva carpeta llamada:

```text
formulario_prueba
```

La estructura inicial será la siguiente.

```text
formulario_prueba/

│

├── server.py

│

├── templates/

│   └── index.html

│

└── static/

    └── css/

        └── style.css
```

> Aunque en esta lección utilizaremos un diseño sencillo, mantendremos la estructura profesional utilizada durante todo el curso.

---

# 📝 Paso 1 - Crear el servidor Flask

Dentro de la carpeta principal crea el archivo:

```text
server.py
```

Agrega el siguiente código.

```python
"""
===========================================
Formulario de Prueba
===========================================

En esta aplicación aprenderemos cómo
recibir información enviada desde un
formulario HTML mediante el método POST.
"""

# ==========================================
# Importaciones
# ==========================================

# Flask:
# Framework principal.

# render_template:
# Permite mostrar plantillas HTML.

from flask import Flask, render_template

# ==========================================
# Crear aplicación Flask
# ==========================================

app = Flask(__name__)

# ==========================================
# Ruta principal
# ==========================================

@app.route("/")
def index():
    """
    Muestra el formulario al usuario.

    En esta primera parte únicamente
    renderizaremos la página HTML.
    """

    return render_template("index.html")


# ==========================================
# Ejecutar aplicación
# ==========================================

if __name__ == "__main__":

    app.run(debug=True)
```

---

# 🔍 Analizando el código

## Importación de Flask

```python
from flask import Flask, render_template
```

Importamos:

- `Flask` para crear la aplicación.
- `render_template()` para mostrar el archivo HTML.

---

## Crear la aplicación

```python
app = Flask(__name__)
```

Esta línea crea el servidor Flask.

A partir de este momento podremos comenzar a definir rutas.

---

## Crear la ruta principal

```python
@app.route("/")
```

Esta ruta responderá cuando el usuario visite:

```
http://127.0.0.1:5000/
```

---

## Mostrar el formulario

```python
return render_template("index.html")
```

Por ahora la única tarea del servidor será mostrar la página que contiene el formulario.

Todavía **no estamos recibiendo información**.

Eso lo haremos en la siguiente parte de la lección.

---

# ▶️ Ejecutar el proyecto

Abre una terminal dentro de la carpeta del proyecto.

Si utilizas **Pipenv**, activa primero el entorno virtual.

```bash
pipenv shell
```

Luego ejecuta el servidor.

### Windows

```bash
python server.py
```

### macOS / Linux

```bash
python3 server.py
```

Si todo está correcto aparecerá un mensaje similar al siguiente.

```text
* Running on http://127.0.0.1:5000
```

Si visitas la dirección anterior obtendrás un error.

Esto es completamente normal.

Todavía no existe el archivo **index.html**.

En la siguiente parte construiremos el formulario HTML, aprenderemos qué hacen los atributos `action` y `method`, y comprenderemos cómo el navegador envía información al servidor mediante una solicitud **POST**.

# 📝 Paso 2 - Crear el formulario HTML

Ahora que nuestro servidor ya está funcionando, construiremos la interfaz que permitirá al usuario ingresar información.

Dentro de la carpeta **templates**, crea el archivo:

```text
index.html
```

Este archivo contendrá nuestro primer formulario HTML.

---

# 💻 Código completo de `index.html`

```html
<!DOCTYPE html>

<html lang="es">

<head>

    <meta charset="UTF-8">

    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">

    <title>Formulario de Usuarios</title>

    <!-- Bootstrap CSS -->
    <link
    href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.7/dist/css/bootstrap.min.css"
    rel="stylesheet">

    <!-- Bootstrap Icons -->
    <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.13.1/font/bootstrap-icons.min.css">

    <!-- Hoja de estilos -->
    <link
    rel="stylesheet"
    href="{{ url_for('static', filename='css/style.css') }}">

</head>

<body>

<div class="container mt-5">

    <div class="row justify-content-center">

        <div class="col-md-6">

            <div class="card shadow">

                <div class="card-header bg-primary text-white">

                    <h3 class="text-center">

                        <i class="bi bi-person-plus-fill"></i>

                        Crear Usuario

                    </h3>

                </div>

                <div class="card-body">

                    <form
                        action="/crear_usuario"
                        method="POST">

                        <div class="mb-3">

                            <label class="form-label">

                                Nombre

                            </label>

                            <input
                                type="text"
                                name="nombre"
                                class="form-control"
                                placeholder="Ingrese su nombre"
                                required>

                        </div>

                        <div class="mb-3">

                            <label class="form-label">

                                Correo Electrónico

                            </label>

                            <input
                                type="email"
                                name="email"
                                class="form-control"
                                placeholder="correo@ejemplo.com"
                                required>

                        </div>

                        <button
                            type="submit"
                            class="btn btn-success w-100">

                            <i class="bi bi-send-fill"></i>

                            Crear Usuario

                        </button>

                    </form>

                </div>

            </div>

        </div>

    </div>

</div>

</body>

</html>
```

---

# 🔍 Analizando el formulario

El elemento más importante es:

```html
<form>

</form>
```

Todo aquello que esté dentro del formulario será enviado al servidor cuando el usuario presione el botón **Crear Usuario**.

---

# 📤 El atributo `action`

Observa la siguiente línea.

```html
<form action="/crear_usuario">
```

El atributo **action** indica la ruta que procesará la información enviada por el formulario.

Visualmente ocurre lo siguiente.

```text
Usuario

↓

Completa el formulario

↓

Presiona "Crear Usuario"

↓

POST

↓

/crear_usuario

↓

Servidor Flask
```

Es importante entender que:

👉 **La ruta indicada en `action` NO muestra el formulario.**

Su única responsabilidad será **recibir y procesar los datos enviados por el usuario**.

---

# 🔄 El atributo `method`

Observa la siguiente línea.

```html
method="POST"
```

Este atributo indica **cómo viajará la información** desde el navegador hacia el servidor.

En esta actividad utilizaremos:

```html
POST
```

porque estamos **enviando información**.

Si omitiéramos este atributo:

```html
<form action="/crear_usuario">
```

el navegador utilizaría automáticamente:

```html
GET
```

y ese no es el comportamiento que buscamos.

---

# 📝 Los controles `<input>`

Los elementos `<input>` permiten al usuario ingresar información.

Ejemplo.

```html
<input
    type="text"
    name="nombre">
```

Cada atributo cumple una función distinta.

| Atributo | Función |
|----------|----------|
| type | Tipo de dato que ingresará el usuario. |
| name | Nombre con el que Flask recibirá el dato. |
| placeholder | Texto de ayuda dentro del campo. |
| required | Obliga al usuario a completar el campo. |

---

# 🔑 El atributo `name`

Este es uno de los atributos más importantes del formulario.

```html
<input

    type="text"

    name="nombre"
>
```

Más adelante, Flask utilizará exactamente este nombre para recuperar el dato.

Por ejemplo.

```python
request.form["nombre"]
```

obtendrá el contenido escrito por el usuario.

Si cambiamos el atributo.

```html
name="usuario"
```

entonces Flask deberá utilizar.

```python
request.form["usuario"]
```

Por esta razón, **el valor del atributo `name` debe coincidir exactamente con la clave utilizada en el servidor**.

---

# 📧 Campo de correo electrónico

Observa el siguiente control.

```html
<input

    type="email"

    name="email"
>
```

A diferencia del primer campo, aquí utilizamos:

```html
type="email"
```

Esto permite que el navegador valide automáticamente si el usuario ingresó un correo electrónico con un formato válido.

Ejemplo válido.

```
usuario@gmail.com
```

Ejemplo inválido.

```
usuariogmail.com
```

---

# 🚀 El botón de envío

Para enviar el formulario utilizamos:

```html
<button

    type="submit"

>

    Crear Usuario

</button>
```

El atributo más importante es:

```html
type="submit"
```

Cuando el usuario hace clic en este botón:

1. El navegador recopila toda la información del formulario.
2. Crea una solicitud HTTP.
3. Envía los datos hacia la ruta indicada en `action`.

---

# ⚠️ ¿Por qué no usar `type="button"`?

Observa la diferencia.

Esto **NO envía** el formulario.

```html
<button type="button">

    Crear Usuario

</button>
```

Mientras que esto sí.

```html
<button type="submit">

    Crear Usuario

</button>
```

Una de las dudas más comunes al comenzar con HTML es confundir ambos tipos de botones.

Recuerda:

| Tipo | Función |
|-------|----------|
| button | Solo crea un botón. |
| submit | Envía el formulario al servidor. |

---

# 🌎 ¿Qué ocurre cuando presionamos "Crear Usuario"?

Supongamos que el usuario escribe:

```
Nombre

Juan Pérez

Correo

juan@gmail.com
```

Al hacer clic en el botón ocurre el siguiente proceso.

```text
Usuario

↓

Completa formulario

↓

Presiona "Crear Usuario"

↓

El navegador recopila los datos

↓

Nombre = Juan Pérez

Correo = juan@gmail.com

↓

POST

↓

/crear_usuario

↓

Servidor Flask
```

En este momento todavía **no existe** la ruta `/crear_usuario`, por lo tanto, si ejecutas la aplicación y presionas el botón obtendrás un error.

Esto es completamente normal.

En la siguiente parte de la lección construiremos la ruta encargada de:

- Recibir la solicitud POST.
- Acceder a los datos enviados mediante `request.form`.
- Procesar la información.
- Redireccionar nuevamente al usuario utilizando `redirect()`.

De esta manera completaremos el ciclo completo de comunicación entre el navegador y el servidor.


# 📝 Paso 3 - Procesar el formulario en Flask

Hasta este momento ya tenemos:

- ✅ Un servidor Flask funcionando.
- ✅ Un formulario HTML.
- ✅ Un botón que envía la información.

Sin embargo, todavía existe un problema.

Cuando presionamos **Crear Usuario**, el navegador intenta enviar la información hacia la siguiente ruta.

```
/crear_usuario
```

Pero esa ruta todavía no existe.

El resultado será un error **404** o **405**, dependiendo de la configuración de la aplicación.

Ahora construiremos la ruta encargada de recibir y procesar toda la información enviada por el formulario.

---

# 💻 Modificar `server.py`

Abre nuevamente el archivo **server.py** y reemplázalo por el siguiente código.

```python
"""
===========================================
Formulario de Prueba
===========================================

En esta aplicación aprenderemos cómo
recibir información enviada desde un
formulario HTML utilizando solicitudes POST.
"""

# ==========================================
# Importaciones
# ==========================================

from flask import (

    Flask,

    render_template,

    request,

    redirect

)

# ==========================================
# Crear aplicación Flask
# ==========================================

app = Flask(__name__)

# ==========================================
# Ruta principal
# ==========================================

@app.route("/")
def index():

    return render_template("index.html")


# ==========================================
# Procesar formulario
# ==========================================

@app.route("/crear_usuario", methods=["POST"])
def crear_usuario():

    print("========== NUEVO USUARIO ==========")

    print(request.form)

    print("-----------------------------------")

    print("Nombre:", request.form["nombre"])

    print("Correo:", request.form["email"])

    print("===================================")

    # Nunca renderizamos una plantilla
    # directamente desde una solicitud POST.

    return redirect("/")


# ==========================================
# Ejecutar servidor
# ==========================================

if __name__ == "__main__":

    app.run(debug=True)
```

---

# 🔍 Analizando las nuevas importaciones

Observa la siguiente línea.

```python
from flask import (

    Flask,

    render_template,

    request,

    redirect

)
```

Hemos agregado dos nuevos componentes.

| Componente | Función |
|------------|----------|
| request | Permite acceder a toda la información enviada por el navegador. |
| redirect | Redirecciona al usuario hacia otra ruta. |

Estas dos herramientas serán utilizadas constantemente durante todo el desarrollo con Flask.

---

# 📬 ¿Qué hace `request`?

Cuando el usuario envía el formulario, el navegador crea una solicitud HTTP.

Dentro de esa solicitud viaja toda la información escrita por el usuario.

Por ejemplo.

```
Nombre

Juan Pérez

Correo

juan@gmail.com
```

Visualmente ocurre lo siguiente.

```text
Formulario

↓

Nombre = Juan Pérez

Correo = juan@gmail.com

↓

Solicitud POST

↓

request

↓

Servidor Flask
```

El objeto **request** representa precisamente esa solicitud.

---

# 📥 `request.form`

Dentro del objeto request existe una propiedad llamada:

```python
request.form
```

Esta propiedad almacena todos los datos enviados por el formulario.

Visualmente podríamos representarla así.

```python
{

    "nombre":"Juan Pérez",

    "email":"juan@gmail.com"

}
```

Observa que ahora tenemos un **diccionario**.

Las claves corresponden exactamente al atributo **name** de cada `<input>`.

---

# 🔑 ¿Por qué es tan importante el atributo `name`?

Recordemos nuestro formulario.

```html
<input

    type="text"

    name="nombre"

>
```

Gracias al atributo.

```html
name="nombre"
```

Flask puede recuperar la información utilizando.

```python
request.form["nombre"]
```

Lo mismo ocurre con el correo.

```html
name="email"
```

↓

```python
request.form["email"]
```

Si ambos nombres no coinciden, Flask no podrá encontrar la información.

---

# 🖨️ Imprimiendo el formulario completo

La siguiente línea.

```python
print(request.form)
```

imprime todo el contenido recibido.

En la terminal verás algo similar a esto.

```text
ImmutableMultiDict(

[

('nombre', 'Juan Pérez'),

('email', 'juan@gmail.com')

]

)
```

Aunque el resultado parece complejo, lo importante es comprender que contiene todos los datos enviados por el formulario.

---

# 📥 Accediendo a un dato específico

Podemos recuperar un campo individual.

```python
request.form["nombre"]
```

Resultado.

```
Juan Pérez
```

Y también.

```python
request.form["email"]
```

Resultado.

```
juan@gmail.com
```

---

# 🔄 ¿Qué hace `redirect()`?

Observa la última línea de la función.

```python
return redirect("/")
```

Una vez procesada la información, Flask envía nuevamente al usuario hacia la página principal.

Visualmente ocurre el siguiente proceso.

```text
Usuario

↓

Completa formulario

↓

POST

↓

Servidor Flask

↓

Procesa información

↓

redirect("/")

↓

GET /

↓

Formulario nuevamente
```

---

# ⚠️ ¿Por qué no usar `render_template()`?

Este es uno de los errores más comunes cuando se comienza a trabajar con Flask.

Muchos desarrolladores escriben.

```python
return render_template("index.html")
```

después de procesar un formulario.

Esto **no es recomendable**.

La buena práctica consiste en seguir el patrón:

```
POST

↓

Procesar información

↓

Redirect

↓

GET

↓

Mostrar página
```

Este patrón es conocido como:

> **Post → Redirect → Get (PRG)**

Es una práctica ampliamente utilizada para evitar que el usuario envíe accidentalmente el mismo formulario varias veces al actualizar la página.

---

# ▶️ Ejecutar la aplicación

Ejecuta nuevamente el servidor.

### Windows

```bash
python server.py
```

### macOS / Linux

```bash
python3 server.py
```

Abre el navegador y visita.

```
http://127.0.0.1:5000
```

Completa el formulario.

```
Nombre

Ana Torres

Correo

ana@gmail.com
```

Presiona.

```
Crear Usuario
```

En la terminal deberías obtener un resultado similar.

```text
========== NUEVO USUARIO ==========

ImmutableMultiDict([

('nombre','Ana Torres'),

('email','ana@gmail.com')

])

-----------------------------------

Nombre: Ana Torres

Correo: ana@gmail.com

===================================
```

Finalmente Flask redireccionará nuevamente al formulario.

---

# ⚠️ Errores comunes

## Error 1

Olvidar indicar que la ruta acepta solicitudes POST.

Incorrecto.

```python
@app.route("/crear_usuario")
```

Correcto.

```python
@app.route(

    "/crear_usuario",

    methods=["POST"]

)
```

---

## Error 2

Intentar acceder a un campo cuyo atributo `name` no existe.

HTML.

```html
<input name="correo">
```

Python.

```python
request.form["email"]
```

Esto producirá un error porque el formulario envía **correo**, no **email**.

---

## Error 3

Utilizar un botón incorrecto.

Incorrecto.

```html
<button type="button">

Enviar

</button>
```

Correcto.

```html
<button type="submit">

Enviar

</button>
```

---

## Error 4

Olvidar importar `request`.

Incorrecto.

```python
from flask import Flask
```

Correcto.

```python
from flask import (

    Flask,

    request

)
```

---

# 🧪 Actividad

Amplía el formulario agregando los siguientes campos.

- Edad
- Ciudad
- Teléfono

Cada campo debe poseer su propio atributo `name`.

Posteriormente, imprime toda la información recibida utilizando `request.form`.

---

# 🚀 Desafío

Modifica el servidor para que imprima un mensaje personalizado.

Ejemplo.

```
==================================

Usuario registrado correctamente

Nombre : Ana Torres

Correo : ana@gmail.com

Edad : 25

Ciudad : Santiago

==================================
```

Investiga cómo acceder a todos los campos utilizando `request.form`.

---

# 🏁 Conclusión

En esta lección aprendiste a completar el flujo de comunicación entre el navegador y el servidor.

Ahora el usuario ya no solo puede visualizar información, sino también **enviarla** mediante formularios HTML.

Incorporaste varios conceptos fundamentales:

- Formularios HTML.
- Solicitudes HTTP de tipo **POST**.
- El objeto `request`.
- La colección `request.form`.
- La importancia del atributo `name`.
- El uso de `redirect()`.
- El patrón **Post → Redirect → Get (PRG)**.

Estos conocimientos serán la base para las próximas unidades, donde comenzaremos a almacenar la información recibida en estructuras de datos y, posteriormente, en una base de datos MySQL utilizando Flask.
Mostrando README.md 