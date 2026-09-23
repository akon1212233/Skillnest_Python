# ⭐ Extra - Mostrar la información recibida en una nueva página

> **Objetivo:**  
> Hasta ahora el servidor recibe correctamente la información del formulario utilizando `request.form`, pero únicamente la muestra en la consola. En este ejercicio construiremos una nueva plantilla HTML que permita visualizar los datos enviados por el usuario directamente en el navegador.

> **Importante:**  
> Este ejercicio tiene un propósito **didáctico**. Más adelante aprenderemos que, en aplicaciones profesionales, normalmente se utiliza el patrón **Post → Redirect → Get (PRG)** junto con **Sesiones (Session)** para mostrar mensajes de confirmación sin responder directamente a una solicitud POST.

---

# 📖 ¿Qué construiremos?

Actualmente el flujo de nuestra aplicación es el siguiente:

```text
Formulario

↓

Usuario completa los datos

↓

POST

↓

Servidor Flask

↓

print(request.form)

↓

redirect("/")
```

Los datos aparecen únicamente en la terminal del servidor.

Nuestro objetivo será modificar el flujo para visualizar también la información en una nueva página.

```text
Formulario

↓

Usuario completa los datos

↓

POST

↓

Servidor Flask

↓

Obtiene los datos

↓

Renderiza una nueva plantilla

↓

Página de confirmación

↓

Botón para volver al formulario
```

---

# 📁 Estructura del proyecto

Agregaremos una nueva plantilla llamada **usuario.html**.

```text
formulario_prueba/

│

├── server.py

│

├── templates/

│   ├── index.html
│   └── usuario.html

│

└── static/

    └── css/

        └── style.css
```

---

# 📝 Paso 1 - Modificar `server.py`

Abre nuevamente el archivo **server.py** y reemplaza únicamente la función `crear_usuario()` por el siguiente código.

```python
@app.route("/crear_usuario", methods=["POST"])
def crear_usuario():
    """
    Procesa la información enviada desde el formulario.
    """

    # ==========================================
    # Obtener la información enviada
    # ==========================================

    nombre = request.form["nombre"]

    email = request.form["email"]

    # ==========================================
    # Mostrar información en la terminal
    # ==========================================

    print("====================================")

    print("Nuevo usuario recibido")

    print(f"Nombre : {nombre}")

    print(f"Correo : {email}")

    print("====================================")

    # ==========================================
    # Enviar la información a una nueva plantilla
    # ==========================================

    return render_template(

        "usuario.html",

        nombre=nombre,

        email=email

    )
```

---

# 🔍 Analizando el código

## 1️⃣ Recuperar la información

El objeto `request.form` contiene todos los datos enviados por el formulario.

```python
nombre = request.form["nombre"]

email = request.form["email"]
```

Recordemos que las claves **nombre** y **email** corresponden exactamente al atributo `name` definido en los `<input>` del formulario.

```html
<input
    type="text"
    name="nombre">

<input
    type="email"
    name="email">
```

---

## 2️⃣ Mostrar información en la consola

Conservaremos los `print()` para comprobar que el servidor recibió correctamente los datos.

```python
print(f"Nombre : {nombre}")

print(f"Correo : {email}")
```

Resultado esperado en la terminal.

```text
====================================

Nuevo usuario recibido

Nombre : Ana Torres

Correo : ana@gmail.com

====================================
```

---

## 3️⃣ Enviar la información al HTML

Finalmente utilizaremos `render_template()` para enviar ambas variables a una nueva plantilla.

```python
return render_template(

    "usuario.html",

    nombre=nombre,

    email=email

)
```

Ahora Flask enviará dos variables hacia la página HTML.

| Variable | Contenido |
|----------|-----------|
| nombre | Nombre ingresado por el usuario |
| email | Correo ingresado por el usuario |

---

# 📝 Paso 2 - Crear la plantilla `usuario.html`

Dentro de la carpeta **templates**, crea un archivo llamado:

```text
usuario.html
```

Agrega el siguiente código.

```html
<!DOCTYPE html>

<html lang="es">

<head>

    <meta charset="UTF-8">

    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">

    <title>Usuario Registrado</title>

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

                <div class="card-header bg-success text-white">

                    <h2 class="text-center">

                        <i class="bi bi-check-circle-fill"></i>

                        Usuario registrado correctamente

                    </h2>

                </div>

                <div class="card-body">

                    <p class="lead">

                        El servidor recibió correctamente la información enviada desde el formulario.

                    </p>

                    <hr>

                    <p>

                        <strong>Nombre:</strong>

                        {{ nombre }}

                    </p>

                    <p>

                        <strong>Correo electrónico:</strong>

                        {{ email }}

                    </p>

                    <hr>

                    <div class="d-grid">

                        <a

                        href="{{ url_for('index') }}"

                        class="btn btn-primary">

                            <i class="bi bi-arrow-left-circle-fill"></i>

                            Volver al formulario

                        </a>

                    </div>

                </div>

            </div>

        </div>

    </div>

</div>

</body>

</html>
```

---

# 🔍 Analizando la plantilla

Observa estas líneas.

```jinja
{{ nombre }}
```

y

```jinja
{{ email }}
```

Estas variables provienen directamente desde Flask.

```python
return render_template(

    "usuario.html",

    nombre=nombre,

    email=email

)
```

Flask reemplaza automáticamente estas expresiones por los datos enviados por el usuario.

Por ejemplo.

```text
Nombre

Ana Torres
```

y

```text
Correo

ana@gmail.com
```

---

# 🔄 El botón "Volver al formulario"

Observa el siguiente enlace.

```html
<a

href="{{ url_for('index') }}"

class="btn btn-primary">

    Volver al formulario

</a>
```

Aquí utilizamos `url_for()` para generar automáticamente la URL correspondiente a la función `index()`.

Esto es una buena práctica, ya que evita escribir rutas manualmente.

---

# ▶️ Resultado esperado

Supongamos que el usuario completa el formulario.

| Campo | Valor |
|--------|-------|
| Nombre | Ana Torres |
| Correo | ana@gmail.com |

Al presionar **Crear Usuario**, obtendrá una página similar a la siguiente.

```text
✔ Usuario registrado correctamente


El servidor recibió correctamente la información enviada.

Nombre:
Ana Torres

Correo:
ana@gmail.com


[ Volver al formulario ]
```

Al mismo tiempo, la terminal mostrará.

```text
====================================

Nuevo usuario recibido

Nombre : Ana Torres

Correo : ana@gmail.com

====================================
```

De esta forma podremos comprobar que la información llegó correctamente tanto al servidor como a la interfaz de usuario.

---

# 💡 ¿Por qué este ejemplo es útil?

Este ejercicio permite visualizar claramente el recorrido completo de la información.

```text
Usuario

↓

Completa formulario

↓

Formulario HTML

↓

Solicitud POST

↓

Servidor Flask

↓

request.form

↓

Variables Python

↓

render_template()

↓

usuario.html

↓

Navegador
```

Comprender este flujo es fundamental antes de comenzar a trabajar con bases de datos y sesiones.

---

# ⚠️ Nota importante

En este ejemplo respondemos directamente a una solicitud **POST** utilizando `render_template()`.

Esto es perfectamente válido para aprender cómo funciona Flask y cómo viajan los datos entre el formulario y la plantilla.

Sin embargo, en aplicaciones profesionales normalmente se utiliza el patrón:

```text
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

Este patrón recibe el nombre de **Post → Redirect → Get (PRG)** y evita que el formulario pueda enviarse nuevamente al actualizar la página.

En las próximas lecciones aprenderemos cómo combinar este patrón con **Sesiones (`session`)**, permitiendo mostrar mensajes de confirmación y mantener información del usuario sin perder las ventajas del flujo profesional.
Mostrando extra.md