# Validación de email con base de datos

## Descripción

Esta actividad integra los contenidos de **validación de formularios, expresiones regulares, mensajes flash, sesiones, sentencias preparadas y conexión entre Flask y MySQL** dentro de una aplicación modularizada.

Se partirá de una aplicación de usuarios y se incorporará un sistema de validación para impedir que se almacenen datos incorrectos en la base de datos.

La aplicación permitirá:

- Crear usuarios.
- Visualizar los usuarios registrados.
- Validar campos obligatorios.
- Validar el formato del correo electrónico mediante una expresión regular.
- Mostrar errores mediante `flash()`.
- Redirigir nuevamente al formulario cuando existan errores.
- Guardar el usuario únicamente cuando los datos sean válidos.
- Comprobar que el email no esté registrado previamente.
- Conservar temporalmente los datos del formulario cuando ocurra un error.

---

# 🎯 Objetivos

Al finalizar esta actividad se deberá comprender:

- Por qué se validan los datos antes de almacenarlos.
- Cómo implementar validaciones mediante `if`.
- Cómo utilizar un `@staticmethod` como método auxiliar de validación.
- Cómo utilizar expresiones regulares.
- Cómo utilizar `re.compile()`.
- Cómo utilizar `.match()`.
- Cómo utilizar mensajes `flash`.
- Cómo utilizar categorías en los mensajes flash.
- Por qué `flash()` necesita `app.secret_key`.
- Cómo utilizar `session` para conservar temporalmente información.
- Cómo comprobar si un email ya existe en MySQL.
- Cómo utilizar `redirect()` después de un `POST`.
- Cómo utilizar `url_for()`.
- Cómo integrar validación, modelo, controlador y vista.

---

# 🧠 ¿Por qué validar?

Un formulario permite que el usuario envíe información al servidor.

Por ejemplo:

```text
Nombre:
Juan

Apellido:
Pérez

E-mail:
juan@email.com
```

Pero el usuario también podría enviar:

```text
Nombre:
```

o:

```text
E-mail:
correo
```

Estos datos no deberían guardarse directamente.

Por eso el flujo correcto es:

```text
Formulario
    ↓
request.form
    ↓
Validación
    ↓
┌──────────────────┐
│                  │
▼                  ▼
INVÁLIDO          VÁLIDO
│                  │
▼                  ▼
flash()           save()
│                  │
▼                  ▼
redirect()        INSERT
│                  │
▼                  ▼
Formulario        redirect()
                   │
                   ▼
                Usuarios
```

---

# 🔐 Validación frontend y backend

El HTML puede ayudar al usuario:

```html
required
```

```html
type="email"
```

Sin embargo, estas validaciones ocurren en el navegador.

La aplicación también debe validar en el servidor:

```text
HTML
 ↓
ayuda al usuario

Python / Flask
 ↓
valida en backend
```

La validación principal de esta actividad estará en Python.

---

# 🔤 Expresiones regulares

Las expresiones regulares, conocidas como **regex**, permiten comprobar si un texto cumple un determinado patrón.

En esta actividad las utilizaremos para comprobar el formato básico de un email.

Primero importamos:

```python
import re
```

Después creamos una expresión regular:

```python
EMAIL_REGEX = re.compile(
    r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
)
```

---

# 🧩 ¿Qué significa `EMAIL_REGEX`?

`EMAIL_REGEX` es un objeto de expresión regular.

Podemos utilizar:

```python
EMAIL_REGEX.match(email)
```

Si encuentra coincidencia, devuelve un objeto `Match`.

Si no coincide:

```python
None
```

Por eso podemos escribir:

```python
if not EMAIL_REGEX.match(email):
```

que significa:

> Si el email no cumple el patrón...

---

# 🔎 Algunos elementos del patrón

La expresión:

```python
r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
```

contiene diferentes partes.

```text
^
```

Indica el inicio del texto.

```text
+
```

Indica que debe existir al menos un carácter del grupo anterior.

```text
@
```

representa el símbolo `@`.

```text
\.
```

representa un punto literal.

```text
$
```

indica el final del texto.

Por ejemplo:

```text
juan@email.com
```

puede cumplir el patrón.

Mientras:

```text
juan@email
```

no lo cumple.

> Esta expresión regular busca un formato básico de email. No pretende implementar todas las posibilidades del estándar completo de correo electrónico.

---

# 🔔 Mensajes flash

`flash()` permite enviar un mensaje temporal al usuario.

Ejemplo:

```python
flash(
    "El email no tiene un formato válido.",
    "email"
)
```

Aquí existen dos elementos:

```text
Mensaje
+
Categoría
```

La categoría puede utilizarse en la plantilla para determinar el estilo o tipo de mensaje.

---

# 🔑 `secret_key`

Como `flash()` utiliza el mecanismo de sesión de Flask, se debe configurar:

```python
app.secret_key = "clave-secreta-desarrollo"
```

Esto permitirá que Flask gestione correctamente la información asociada a la sesión.

En un proyecto real, una clave sensible no debería escribirse directamente en el código.

---

# 🗃️ `session`

En esta actividad `session` será utilizada para conservar temporalmente los datos del formulario cuando ocurra un error.

Ejemplo:

```python
session["datos_formulario"] = data
```

Esto permite:

```text
POST
 ↓
error
 ↓
guardar datos temporalmente
 ↓
redirect()
 ↓
GET
 ↓
recuperar datos
 ↓
mostrar formulario nuevamente
```

---

# 🔄 `flash()` vs `session`

| Elemento | Función |
|---|---|
| `flash()` | Transportar mensajes temporales |
| `session` | Mantener información entre solicitudes |
| `redirect()` | Redirigir hacia otra ruta |
| `request.form` | Recibir datos enviados mediante POST |

Por ejemplo:

```text
flash()
```

puede almacenar:

```text
"El email no es válido"
```

Mientras:

```text
session
```

puede almacenar:

```text
nombre = "Juan"
apellido = "Pérez"
email = "correo"
```

---

# 🗄️ Modelo de datos

La base de datos será:

```text
esquema_usuarios
```

La tabla:

```text
usuarios
```

contendrá:

```text
usuarios
│
├── id
├── nombre
├── apellido
├── email
├── created_at
└── updated_at
```

---

# 📐 Tercera Forma Normal — 3FN

La tabla está diseñada de manera que cada atributo describa directamente al usuario identificado por su clave primaria.

```text
id
↓
identifica al usuario

nombre
apellido
email
created_at
updated_at
↓
pertenecen directamente a ese usuario
```

No se crean tablas independientes innecesarias para:

```text
nombres
apellidos
emails
```

La estructura es suficiente para esta actividad.

---

# 🔐 Unicidad del email

Como extensión de la validación, el email debe ser único.

Esto se controlará en dos niveles.

### Aplicación

Python comprobará:

```text
¿Existe ya este email?
```

### Base de datos

MySQL tendrá una restricción:

```text
UNIQUE(email)
```

Por lo tanto:

```text
Python
+
MySQL
```

colaboran para mantener la integridad del dato.

---

# 📊 ERD

El ERD debe representar:

```text
┌─────────────────────────────────┐
│            usuarios             │
├─────────────────────────────────┤
│ id             PK               │
│ nombre         VARCHAR(100)     │
│ apellido       VARCHAR(100)     │
│ email          VARCHAR(100) UQ  │
│ created_at     DATETIME         │
│ updated_at     DATETIME         │
└─────────────────────────────────┘
```

El proyecto debe conservar el ERD en:

```text
resources/
```

---

# 📁 Estructura final del proyecto

```text
usuarios_validacion/
│
├── flask_app/
│   │
│   ├── __init__.py
│   │
│   ├── bd/
│   │   └── esquema_usuarios.sql
│   │
│   ├── config/
│   │   └── mysqlconnection.py
│   │
│   ├── controllers/
│   │   └── usuarios.py
│   │
│   ├── models/
│   │   └── usuario.py
│   │
│   ├── templates/
│   │   ├── usuarios.html
│   │   └── nuevo_usuario.html
│   │
│   └── static/
│       └── css/
│           └── style.css
│
├── resources/
│   └── esquema_usuarios_erd.mwb
│
├── Pipfile
├── Pipfile.lock
├── .gitignore
└── server.py
```

> Se utiliza solamente `flask_app/__init__.py`. Las carpetas `config`, `controllers`, `models`, `templates`, `static`, `bd` y `resources` no necesitan un `__init__.py` propio para este proyecto.

---

# 🐍 Pipenv

Instalar Flask y PyMySQL:

```bash
pipenv install flask pymysql
```

Ejecutar:

```bash
pipenv run python server.py
```

También se puede activar el entorno:

```bash
pipenv shell
```

y después:

```bash
python server.py
```

---

# 📄 `Pipfile`

```toml
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]
flask = "*"
pymysql = "*"

[dev-packages]

[requires]
python_version = "3"
```

---

# 🚫 `.gitignore`

```text
__pycache__/
*.pyc
.venv/
venv/
.env
```

---

# 🗄️ Base de datos

## `flask_app/bd/esquema_usuarios.sql`

```sql
-- ==========================================================
-- BASE DE DATOS
-- ==========================================================

CREATE DATABASE IF NOT EXISTS esquema_usuarios;

USE esquema_usuarios;


-- ==========================================================
-- TABLA USUARIOS
-- ==========================================================

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);


-- ==========================================================
-- DATOS DE PRUEBA
-- ==========================================================

INSERT INTO usuarios
(
    nombre,
    apellido,
    email
)
VALUES
(
    "Soraya",
    "Montenegro",
    "soraya@email.com"
),
(
    "Armando",
    "Mendoza",
    "armando@email.com"
),
(
    "Mia",
    "Colucci",
    "mia@email.com"
),
(
    "Rubi",
    "Perez",
    "rubi@email.com"
);
```

---

# 🔍 Comprobar la base

```sql
USE esquema_usuarios;
```

```sql
DESCRIBE usuarios;
```

```sql
SELECT *
FROM usuarios;
```

---

# ⚙️ Inicialización Flask

## `flask_app/__init__.py`

```python
from flask import Flask

app = Flask(__name__)

# Necesaria para utilizar flash() y session.
app.secret_key = "clave-secreta-desarrollo"
```

---

# 🔌 Conexión MySQL

## `flask_app/config/mysqlconnection.py`

```python
import pymysql.cursors


class MySQLConnection:
    """
    Administra la conexión entre Flask y MySQL.
    """

    def __init__(self, db):
        self.connection = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            database=db,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )


    def query_db(self, query, data=None):
        """
        Ejecuta una consulta SQL.

        SELECT:
            devuelve una lista de diccionarios.

        INSERT:
            devuelve el ID generado.

        UPDATE / DELETE:
            devuelve las filas afectadas.

        Error:
            devuelve False.
        """

        with self.connection.cursor() as cursor:

            try:

                cursor.execute(
                    query,
                    data
                )


                tipo_consulta = query.strip().lower()


                if tipo_consulta.startswith("select"):

                    return cursor.fetchall()


                if tipo_consulta.startswith("insert"):

                    return cursor.lastrowid


                return cursor.rowcount


            except Exception as e:

                print(
                    "Something went wrong:",
                    e
                )

                return False


            finally:

                self.connection.close()


def connectToMySQL(db):
    """
    Devuelve una instancia de conexión a MySQL.
    """

    return MySQLConnection(db)
```

> Cambia `user` y `password` según la configuración local de MySQL.

---

# 👤 Modelo Usuario

## `flask_app/models/usuario.py`

```python
import re

from flask import flash

from flask_app.config.mysqlconnection import connectToMySQL


# ==========================================================
# EXPRESIÓN REGULAR PARA EMAIL
# ==========================================================

EMAIL_REGEX = re.compile(
    r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
)


class Usuario:
    """
    Representa un registro de la tabla usuarios.
    """

    def __init__(self, data):
        self.id = data["id"]
        self.nombre = data["nombre"]
        self.apellido = data["apellido"]
        self.email = data["email"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]


    # ======================================================
    # VALIDACIÓN
    # ======================================================

    @staticmethod
    def validar_usuario(usuario):
        """
        Comprueba que los datos recibidos
        cumplan las reglas del formulario.

        Retorna:
            True  → datos válidos.
            False → existen errores.
        """

        es_valido = True


        # --------------------------------------------------
        # NOMBRE
        # --------------------------------------------------

        if not usuario["nombre"]:

            flash(
                "El nombre es obligatorio.",
                "nombre"
            )

            es_valido = False


        # --------------------------------------------------
        # APELLIDO
        # --------------------------------------------------

        if not usuario["apellido"]:

            flash(
                "El apellido es obligatorio.",
                "apellido"
            )

            es_valido = False


        # --------------------------------------------------
        # EMAIL
        # --------------------------------------------------

        if not usuario["email"]:

            flash(
                "El email es obligatorio.",
                "email"
            )

            es_valido = False

        elif not EMAIL_REGEX.match(
            usuario["email"]
        ):

            flash(
                "El email no tiene un formato válido.",
                "email"
            )

            es_valido = False


        return es_valido


    # ======================================================
    # READ — TODOS LOS USUARIOS
    # ======================================================

    @classmethod
    def get_all(cls):
        """
        Obtiene todos los usuarios.
        """

        query = """
            SELECT
                id,
                nombre,
                apellido,
                email,
                created_at,
                updated_at
            FROM usuarios
            ORDER BY id DESC;
        """


        resultados = connectToMySQL(
            "esquema_usuarios"
        ).query_db(query)


        usuarios = []


        for usuario in resultados:

            usuarios.append(
                cls(usuario)
            )


        return usuarios


    # ======================================================
    # READ — USUARIO POR ID
    # ======================================================

    @classmethod
    def get_by_id(cls, id):
        """
        Obtiene un usuario por su identificador.
        """

        query = """
            SELECT
                id,
                nombre,
                apellido,
                email,
                created_at,
                updated_at
            FROM usuarios
            WHERE id = %(id)s;
        """


        data = {
            "id": id
        }


        resultados = connectToMySQL(
            "esquema_usuarios"
        ).query_db(
            query,
            data
        )


        if resultados:

            return cls(
                resultados[0]
            )


        return None


    # ======================================================
    # BONUS — EMAIL ÚNICO
    # ======================================================

    @classmethod
    def email_existe(cls, email):
        """
        Comprueba si un email ya se encuentra
        registrado en la base de datos.
        """

        query = """
            SELECT
                id
            FROM usuarios
            WHERE email = %(email)s;
        """


        data = {
            "email": email
        }


        resultados = connectToMySQL(
            "esquema_usuarios"
        ).query_db(
            query,
            data
        )


        return bool(resultados)


    # ======================================================
    # CREATE
    # ======================================================

    @classmethod
    def save(cls, data):
        """
        Guarda un nuevo usuario.
        """

        query = """
            INSERT INTO usuarios
            (
                nombre,
                apellido,
                email
            )
            VALUES
            (
                %(nombre)s,
                %(apellido)s,
                %(email)s
            );
        """


        return connectToMySQL(
            "esquema_usuarios"
        ).query_db(
            query,
            data
        )
```

---

# 🧠 ¿Qué aprendemos en el modelo?

Aquí se concentran dos tareas diferentes:

```text
validar_usuario()
```

se encarga de:

```text
comprobar datos
```

Mientras:

```text
save()
```

se encarga de:

```text
guardar datos
```

Por lo tanto:

```text
VALIDAR
   ↓
GUARDAR
```

y no:

```text
GUARDAR
   ↓
VALIDAR
```

---

# 🧩 ¿Por qué `validar_usuario()` es `@staticmethod`?

Porque no necesitamos acceder a:

```python
self
```

ni:

```python
cls
```

El método solamente recibe información:

```python
usuario
```

Por eso puede ejecutarse así:

```python
Usuario.validar_usuario(data)
```

---

# 🎮 Controlador

## `flask_app/controllers/usuarios.py`

```python
from flask_app import app

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from flask_app.models.usuario import Usuario


# ==========================================================
# INICIO
# ==========================================================

@app.route("/")
def inicio():
    """
    La raíz redirige al listado de usuarios.
    """

    return redirect(
        url_for("usuarios")
    )


# ==========================================================
# LISTADO
# ==========================================================

@app.route("/usuarios")
def usuarios():
    """
    Obtiene todos los usuarios y los envía
    a la plantilla.
    """

    todos_los_usuarios = Usuario.get_all()

    return render_template(
        "usuarios.html",
        usuarios=todos_los_usuarios
    )


# ==========================================================
# FORMULARIO NUEVO USUARIO
# ==========================================================

@app.route("/usuarios/nuevo")
def nuevo_usuario():
    """
    Muestra el formulario de creación.

    Si existen datos guardados temporalmente
    por un error anterior, los recuperamos.
    """

    datos_formulario = session.pop(
        "datos_formulario",
        {}
    )


    return render_template(
        "nuevo_usuario.html",
        datos_formulario=datos_formulario
    )


# ==========================================================
# CREAR USUARIO
# ==========================================================

@app.route(
    "/usuarios/crear",
    methods=["POST"]
)
def crear_usuario():
    """
    Recibe, valida y guarda un usuario.
    """

    # ------------------------------------------------------
    # Recuperamos los datos del formulario.
    # ------------------------------------------------------

    nombre = request.form.get(
        "nombre",
        ""
    ).strip()

    apellido = request.form.get(
        "apellido",
        ""
    ).strip()

    email = request.form.get(
        "email",
        ""
    ).strip()


    # ------------------------------------------------------
    # Diccionario que será enviado al modelo.
    # ------------------------------------------------------

    data = {
        "nombre": nombre,
        "apellido": apellido,
        "email": email
    }


    # ------------------------------------------------------
    # VALIDACIÓN BÁSICA
    # ------------------------------------------------------

    if not Usuario.validar_usuario(data):

        # Guardamos temporalmente los datos para
        # recuperarlos después del redirect.
        session["datos_formulario"] = data

        return redirect(
            url_for("nuevo_usuario")
        )


    # ------------------------------------------------------
    # BONUS — EMAIL ÚNICO
    # ------------------------------------------------------

    if Usuario.email_existe(
        data["email"]
    ):

        flash(
            "El email ingresado ya está registrado.",
            "email"
        )

        # Conservamos los datos del formulario.
        session["datos_formulario"] = data

        return redirect(
            url_for("nuevo_usuario")
        )


    # ------------------------------------------------------
    # GUARDAR
    # ------------------------------------------------------

    resultado = Usuario.save(
        data
    )


    # ------------------------------------------------------
    # Error en la base de datos.
    # ------------------------------------------------------

    if resultado is False:

        flash(
            "No fue posible crear el usuario.",
            "error"
        )

        session["datos_formulario"] = data

        return redirect(
            url_for("nuevo_usuario")
        )


    # ------------------------------------------------------
    # ÉXITO
    # ------------------------------------------------------

    # Nos aseguramos de eliminar cualquier información
    # temporal que todavía pudiera existir.
    session.pop(
        "datos_formulario",
        None
    )


    flash(
        "Usuario creado correctamente.",
        "success"
    )


    # Después de un POST exitoso:
    # POST → INSERT → redirect → GET
    return redirect(
        url_for("usuarios")
    )
```

---

# 🧠 Flujo del controlador

La ruta:

```text
POST /usuarios/crear
```

realiza:

```text
request.form
       ↓
data
       ↓
validar_usuario()
       ↓
email_existe()
       ↓
save()
```

Pero solamente cuando los datos son correctos.

---

# ❌ Si hay errores

```text
POST
 ↓
request.form
 ↓
validar_usuario()
 ↓
False
 ↓
flash()
 ↓
session["datos_formulario"]
 ↓
redirect()
 ↓
GET /usuarios/nuevo
```

---

# ✅ Si no existen errores

```text
POST
 ↓
request.form
 ↓
validar_usuario()
 ↓
True
 ↓
email_existe()
 ↓
False
 ↓
Usuario.save()
 ↓
INSERT
 ↓
flash()
 ↓
redirect()
 ↓
GET /usuarios
```

---

# 🔄 ¿Por qué usamos `redirect()`?

Después de procesar un formulario `POST`, utilizamos:

```python
redirect()
```

La idea es:

```text
POST
 ↓
procesar
 ↓
redirect()
 ↓
GET
```

Esto evita que la página quede directamente asociada al envío del formulario.

---

# 🔗 `url_for()`

En lugar de escribir manualmente:

```text
/usuarios
```

podemos utilizar:

```python
url_for("usuarios")
```

Para el formulario:

```python
url_for("crear_usuario")
```

Para el formulario de alta:

```python
url_for("nuevo_usuario")
```

Esto hace que la navegación dependa del nombre de la función Flask.

---

# 🌐 Vista Usuarios

## `flask_app/templates/usuarios.html`

```html
<!DOCTYPE html>
<html lang="es">

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>
        Usuarios
    </title>

    <link
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.7/dist/css/bootstrap.min.css"
        rel="stylesheet"
    >

    <link
        rel="stylesheet"
        href="{{ url_for(
            'static',
            filename='css/style.css'
        ) }}"
    >

</head>

<body>

<div class="container py-5">


    <div class="d-flex justify-content-between align-items-center mb-4">

        <div>

            <h1>
                Usuarios
            </h1>

            <p class="text-muted mb-0">
                Usuarios registrados en la base de datos.
            </p>

        </div>


        <a
            href="{{ url_for('nuevo_usuario') }}"
            class="btn btn-primary"
        >

            Nuevo Usuario

        </a>

    </div>


    <!-- ==================================================
         MENSAJES FLASH
    =================================================== -->

    {% with messages = get_flashed_messages(
        with_categories=true
    ) %}

        {% if messages %}

            {% for category, message in messages %}

                <div
                    class="alert alert-{{ category }}"
                >

                    {{ message }}

                </div>

            {% endfor %}

        {% endif %}

    {% endwith %}


    <!-- ==================================================
         TABLA
    =================================================== -->

    <div class="card shadow-sm border-0">

        <div class="card-body p-0">


            {% if usuarios %}

                <div class="table-responsive">

                    <table class="table table-hover mb-0">

                        <thead class="table-dark">

                            <tr>

                                <th>
                                    ID
                                </th>

                                <th>
                                    Nombre
                                </th>

                                <th>
                                    Apellido
                                </th>

                                <th>
                                    E-mail
                                </th>

                            </tr>

                        </thead>


                        <tbody>


                            {% for usuario in usuarios %}

                                <tr>

                                    <td>
                                        {{ usuario.id }}
                                    </td>

                                    <td>
                                        {{ usuario.nombre }}
                                    </td>

                                    <td>
                                        {{ usuario.apellido }}
                                    </td>

                                    <td>
                                        {{ usuario.email }}
                                    </td>

                                </tr>

                            {% endfor %}


                        </tbody>

                    </table>

                </div>


            {% else %}

                <div class="p-4">

                    <div class="alert alert-info mb-0">

                        No existen usuarios registrados.

                    </div>

                </div>

            {% endif %}


        </div>

    </div>


</div>

</body>

</html>
```

---

# 📝 Vista Nuevo Usuario

## `flask_app/templates/nuevo_usuario.html`

```html
<!DOCTYPE html>
<html lang="es">

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>
        Nuevo Usuario
    </title>

    <link
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.7/dist/css/bootstrap.min.css"
        rel="stylesheet"
    >

    <link
        rel="stylesheet"
        href="{{ url_for(
            'static',
            filename='css/style.css'
        ) }}"
    >

</head>

<body>

<div class="container py-5">


    <div class="row justify-content-center">

        <div class="col-lg-7">


            <div class="card shadow-sm border-0">

                <div class="card-body p-4">


                    <h1 class="mb-2">
                        Crear nuevo usuario
                    </h1>

                    <p class="text-muted mb-4">

                        Completa la información del usuario.

                    </p>


                    <!-- ==================================================
                         MENSAJES FLASH
                    =================================================== -->

                    {% with messages = get_flashed_messages(
                        with_categories=true
                    ) %}

                        {% if messages %}

                            {% for category, message in messages %}

                                <div
                                    class="alert alert-{{ category }}"
                                >

                                    {{ message }}

                                </div>

                            {% endfor %}

                        {% endif %}

                    {% endwith %}


                    <!-- ==================================================
                         FORMULARIO
                    =================================================== -->

                    <form
                        action="{{ url_for('crear_usuario') }}"
                        method="POST"
                    >


                        <!-- NOMBRE -->

                        <div class="mb-3">

                            <label
                                for="nombre"
                                class="form-label"
                            >

                                Nombre

                            </label>


                            <input
                                type="text"
                                id="nombre"
                                name="nombre"
                                class="form-control"
                                value="{{ datos_formulario.get('nombre', '') }}"
                                required
                            >

                        </div>


                        <!-- APELLIDO -->

                        <div class="mb-3">

                            <label
                                for="apellido"
                                class="form-label"
                            >

                                Apellido

                            </label>


                            <input
                                type="text"
                                id="apellido"
                                name="apellido"
                                class="form-control"
                                value="{{ datos_formulario.get('apellido', '') }}"
                                required
                            >

                        </div>


                        <!-- EMAIL -->

                        <div class="mb-4">

                            <label
                                for="email"
                                class="form-label"
                            >

                                E-mail

                            </label>


                            <input
                                type="email"
                                id="email"
                                name="email"
                                class="form-control"
                                value="{{ datos_formulario.get('email', '') }}"
                                required
                            >

                        </div>


                        <!-- BOTONES -->

                        <div class="d-flex gap-2">

                            <button
                                type="submit"
                                class="btn btn-success"
                            >

                                Crear

                            </button>


                            <a
                                href="{{ url_for('usuarios') }}"
                                class="btn btn-outline-secondary"
                            >

                                Volver

                            </a>

                        </div>


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

# 🎨 CSS

## `flask_app/static/css/style.css`

```css
body {
    background-color: #f5f6f8;
    color: #212529;
    font-family: Arial, Helvetica, sans-serif;
}

h1,
h2,
h3 {
    font-weight: 700;
}

.card {
    border-radius: 10px;
}

.form-control {
    border-radius: 7px;
}

.btn {
    border-radius: 7px;
}

.table {
    vertical-align: middle;
}

.table th {
    white-space: nowrap;
}

.alert {
    border-radius: 8px;
}
```

---

# 🚀 Punto de entrada

## `server.py`

```python
from flask_app import app

# Importamos el controlador para registrar las rutas.
from flask_app.controllers import usuarios


if __name__ == "__main__":
    app.run(debug=True)
```

---

# 🗺️ Rutas de la aplicación

| Método | Ruta | Función |
|---|---|---|
| `GET` | `/` | Redirige a `/usuarios` |
| `GET` | `/usuarios` | Muestra usuarios |
| `GET` | `/usuarios/nuevo` | Muestra formulario |
| `POST` | `/usuarios/crear` | Valida y crea usuario |

---

# 🔄 Flujo completo

## Caso correcto

```text
GET /usuarios/nuevo
        ↓
Formulario
        ↓
POST /usuarios/crear
        ↓
request.form
        ↓
data
        ↓
validar_usuario()
        ↓
email_existe()
        ↓
Usuario.save()
        ↓
INSERT
        ↓
flash()
        ↓
redirect()
        ↓
GET /usuarios
```

---

# ❌ Caso con campos vacíos

Supongamos:

```text
Nombre:
Apellido:
Email:
```

El controlador construye:

```python
data = {
    "nombre": "",
    "apellido": "",
    "email": ""
}
```

Luego:

```python
Usuario.validar_usuario(data)
```

generará:

```text
El nombre es obligatorio.
El apellido es obligatorio.
El email es obligatorio.
```

Después:

```text
session["datos_formulario"]
```

guarda los valores.

Finalmente:

```text
redirect()
```

lleva nuevamente a:

```text
/usuarios/nuevo
```

---

# ❌ Caso email inválido

Ejemplo:

```text
Nombre:
Juan

Apellido:
Pérez

Email:
juan@email
```

La expresión:

```python
EMAIL_REGEX.match(
    usuario["email"]
)
```

no encontrará coincidencia.

Se ejecutará:

```python
flash(
    "El email no tiene un formato válido.",
    "email"
)
```

Y el formulario volverá a mostrarse.

---

# ❌ Caso email duplicado

Supongamos que ya existe:

```text
juan@email.com
```

Si se intenta registrar nuevamente:

```text
Usuario.validar_usuario()
```

puede devolver:

```text
True
```

porque el formato es correcto.

Después se ejecuta:

```python
Usuario.email_existe(
    data["email"]
)
```

La base de datos encuentra el registro.

Entonces:

```python
flash(
    "El email ingresado ya está registrado.",
    "email"
)
```

y el usuario vuelve al formulario.

---

# ⭐ BONUS — Email único

El control del email está implementado en dos niveles.

## Python

```python
Usuario.email_existe(email)
```

## MySQL

```sql
UNIQUE
```

Esto significa:

```text
Aplicación
     +
Base de datos
     ↓
Integridad del email
```

---

# 📤 BONUS — Conservar datos

Supongamos que se ingresa:

```text
Nombre:
Juan

Apellido:
Pérez

Email:
juan@
```

Existe un error de formato.

El controlador guarda:

```python
session["datos_formulario"] = data
```

Luego redirige.

La ruta:

```text
GET /usuarios/nuevo
```

recupera:

```python
datos_formulario = session.pop(
    "datos_formulario",
    {}
)
```

El HTML utiliza:

```jinja
{{ datos_formulario.get('nombre', '') }}
```

y:

```jinja
{{ datos_formulario.get('apellido', '') }}
```

y:

```jinja
{{ datos_formulario.get('email', '') }}
```

Por lo tanto, los datos permanecen en el formulario.

---

# 🧠 ¿Por qué `session.pop()`?

Utilizamos:

```python
session.pop(
    "datos_formulario",
    {}
)
```

para recuperar la información y eliminarla de la sesión.

Así los datos son temporales.

El flujo queda:

```text
session
   ↓
recuperar
   ↓
mostrar
   ↓
eliminar
```

No queremos mantener indefinidamente esos datos en la sesión.

---

# 🧠 ¿Por qué no usamos `flash()` para guardar los datos?

Porque `flash()` está pensado para mensajes.

Por ejemplo:

```text
"El email no tiene un formato válido."
```

Mientras que:

```python
session["datos_formulario"]
```

sirve para conservar información estructurada:

```python
{
    "nombre": "Juan",
    "apellido": "Pérez",
    "email": "juan@"
}
```

---

# 🔗 Relación HTML → Flask

HTML:

```html
<input
    type="text"
    name="nombre"
>
```

Flask:

```python
request.form.get("nombre")
```

HTML:

```html
<input
    type="text"
    name="apellido"
>
```

Flask:

```python
request.form.get("apellido")
```

HTML:

```html
<input
    type="email"
    name="email"
>
```

Flask:

```python
request.form.get("email")
```

Los nombres deben coincidir.

---

# 🧠 Flujo del email

```text
Usuario escribe:
juan@email.com
        ↓
HTML
        ↓
POST
        ↓
request.form["email"]
        ↓
data["email"]
        ↓
EMAIL_REGEX.match()
        ↓
¿coincide?
        │
   ┌────┴────┐
   │         │
  NO        SÍ
   │         │
 flash()   continuar
   │         │
   ▼         ▼
redirect   email_existe()
             │
        ┌────┴────┐
        │         │
       SÍ        NO
        │         │
     flash()    save()
```

---

# 🧠 Flujo MVC

```text
                 NAVEGADOR
                     │
                     ▼
                 CONTROLLER
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
        MODEL                  VIEW
          │                     │
          ▼                     ▼
        MySQL                 Jinja2
          │                     │
          └──────────┬──────────┘
                     ▼
                    HTML
```

---

# 📚 Responsabilidad de cada archivo

| Archivo | Responsabilidad |
|---|---|
| `server.py` | Ejecuta la aplicación |
| `flask_app/__init__.py` | Inicializa Flask |
| `mysqlconnection.py` | Conecta con MySQL |
| `usuario.py` | Modelo, consultas y validación |
| `usuarios.py` | Rutas y flujo |
| `usuarios.html` | Lista usuarios |
| `nuevo_usuario.html` | Formulario |
| `style.css` | Presentación |
| `esquema_usuarios.sql` | Base de datos |
| `esquema_usuarios_erd.mwb` | ERD |

---

# 🧪 Casos de prueba

## ✅ Prueba 1 — Usuario correcto

Ingresar:

```text
Nombre:
Juan

Apellido:
Pérez

Email:
juan@email.com
```

Resultado esperado:

```text
Usuario creado correctamente.
```

Y el usuario debe aparecer en:

```text
/usuarios
```

---

## ❌ Prueba 2 — Nombre vacío

Ingresar:

```text
Nombre:
```

Resultado:

```text
El nombre es obligatorio.
```

El registro no debe guardarse.

---

## ❌ Prueba 3 — Apellido vacío

Resultado:

```text
El apellido es obligatorio.
```

El registro no debe guardarse.

---

## ❌ Prueba 4 — Email vacío

Resultado:

```text
El email es obligatorio.
```

El registro no debe guardarse.

---

## ❌ Prueba 5 — Email inválido

Ingresar:

```text
juan@
```

Resultado:

```text
El email no tiene un formato válido.
```

---

## ❌ Prueba 6 — Múltiples errores

Ingresar:

```text
Nombre:

Apellido:

Email:
correo
```

La aplicación debe mostrar:

```text
El nombre es obligatorio.
El apellido es obligatorio.
El email no tiene un formato válido.
```

---

## ⭐ Prueba 7 — Email duplicado

Primero registrar:

```text
juan@email.com
```

Después intentar registrarlo nuevamente.

Resultado:

```text
El email ingresado ya está registrado.
```

No se debe crear un segundo usuario.

---

## ⭐ Prueba 8 — Conservar información

Ingresar:

```text
Nombre:
Juan

Apellido:
Pérez

Email:
correo
```

Después de producirse el error, el formulario debe continuar mostrando:

```text
Nombre:
Juan

Apellido:
Pérez

Email:
correo
```

El usuario solo debe corregir el email.

---

# 🔎 Comprobar en MySQL

```sql
USE esquema_usuarios;
```

Consultar:

```sql
SELECT *
FROM usuarios;
```

Comprobar emails duplicados:

```sql
SELECT
    email,
    COUNT(*) AS cantidad
FROM usuarios
GROUP BY email
HAVING COUNT(*) > 1;
```

El resultado debería estar vacío.

---

# 🧪 Comprobación de la restricción UNIQUE

Intentar directamente en MySQL:

```sql
INSERT INTO usuarios
(
    nombre,
    apellido,
    email
)
VALUES
(
    "Usuario",
    "Duplicado",
    "soraya@email.com"
);
```

MySQL debería rechazar la operación porque:

```text
soraya@email.com
```

ya existe.

Esto demuestra que la base de datos también protege la integridad del email.

---

# ⚠️ Errores comunes

## Olvidar `secret_key`

Si aparece un problema al utilizar:

```python
flash()
```

comprobar:

```python
app.secret_key = "clave-secreta-desarrollo"
```

---

## Olvidar importar `flash`

En el modelo:

```python
from flask import flash
```

---

## Olvidar `re`

Debe existir:

```python
import re
```

---

## Utilizar mal la expresión regular

La expresión contiene:

```text
\.
```

para representar un punto literal.

No utilizar simplemente:

```text
.
```

cuando se quiere representar exclusivamente el punto del dominio.

---

## Guardar antes de validar

Incorrecto:

```python
Usuario.save(data)

if not Usuario.validar_usuario(data):
    ...
```

Correcto:

```python
if not Usuario.validar_usuario(data):
    ...
```

y solamente después:

```python
Usuario.save(data)
```

---

## No conservar datos

Si ocurre un error y los campos aparecen vacíos, comprobar:

```python
session["datos_formulario"] = data
```

y:

```python
session.pop(
    "datos_formulario",
    {}
)
```

---

## `request.form` no encuentra un campo

Comprobar que el HTML tenga:

```html
name="email"
```

y Python:

```python
request.form.get("email")
```

---

## `BuildError`

Comprobar que:

```jinja
url_for("nuevo_usuario")
```

corresponda a:

```python
def nuevo_usuario():
```

---

## `TemplateNotFound`

Comprobar que:

```text
templates/
```

esté dentro de:

```text
flask_app/
```

---

# 🧠 Análisis final del código

## `re`

```python
import re
```

Importa el módulo estándar de Python que permite trabajar con expresiones regulares.

---

## `re.compile()`

```python
EMAIL_REGEX = re.compile(...)
```

crea un objeto reutilizable para trabajar con el patrón.

---

## `.match()`

```python
EMAIL_REGEX.match(email)
```

intenta encontrar una coincidencia con el patrón.

Puede devolver:

```text
Match
```

o:

```text
None
```

---

## `@staticmethod`

```python
@staticmethod
def validar_usuario(usuario):
```

es apropiado porque el método necesita solamente los datos recibidos.

No necesita acceder a:

```text
self
```

ni:

```text
cls
```

---

## `flash()`

```python
flash(
    "El email no tiene un formato válido.",
    "email"
)
```

genera un mensaje temporal.

---

## `session`

```python
session["datos_formulario"] = data
```

conserva información entre solicitudes.

---

## `redirect()`

```python
return redirect(
    url_for("nuevo_usuario")
)
```

permite realizar:

```text
POST
 ↓
redirect()
 ↓
GET
```

---

## `url_for()`

```python
url_for("usuarios")
```

genera la URL asociada con la función:

```python
def usuarios():
```

---

## `email_existe()`

```python
Usuario.email_existe(email)
```

consulta MySQL para determinar si el correo ya está registrado.

---

## `UNIQUE(email)`

La base de datos evita que existan dos registros con el mismo email.

---

# 🧠 El flujo completo de la práctica

```text
                  FORMULARIO
                       │
                       ▼
                     POST
                       │
                       ▼
                 request.form
                       │
                       ▼
                     data
                       │
                       ▼
              validar_usuario()
                       │
                ┌──────┴──────┐
                │             │
             INVÁLIDO        VÁLIDO
                │             │
                ▼             ▼
             flash()      email_existe()
                │             │
            session      ┌────┴────┐
                │        │         │
                │       SÍ        NO
                │        │         │
                │        ▼         ▼
                │      flash()   save()
                │        │         │
                └────┬───┘         ▼
                     │            INSERT
                     │              │
                     ▼              ▼
                  redirect()     redirect()
                     │              │
                     ▼              ▼
              formulario       /usuarios
```

---

# 🏁 Resultado esperado

La página principal debe permitir visualizar:

```text
Usuarios

┌────┬───────────────┬──────────────┬──────────────────────┐
│ ID │ Nombre        │ Apellido     │ E-mail               │
├────┼───────────────┼──────────────┼──────────────────────┤
│ 4  │ Rubi          │ Perez        │ rubi@email.com       │
│ 3  │ Mia           │ Colucci      │ mia@email.com        │
│ 2  │ Armando       │ Mendoza      │ armando@email.com    │
│ 1  │ Soraya        │ Montenegro   │ soraya@email.com     │
└────┴───────────────┴──────────────┴──────────────────────┘

[Nuevo Usuario]
```

La página:

```text
/usuarios/nuevo
```

debe mostrar:

```text
Crear nuevo usuario

Nombre:
[________________________]

Apellido:
[________________________]

E-mail:
[________________________]

[Crear] [Volver]
```

Cuando existe un error:

```text
┌─────────────────────────────────────────────┐
│ El email no tiene un formato válido.       │
└─────────────────────────────────────────────┘
```

y los datos ingresados deben mantenerse cuando se implemente el BONUS.

---

# ✅ Checklist final

```text
[ ] Pipenv configurado
[ ] Flask instalado
[ ] PyMySQL instalado
[ ] Pipfile creado
[ ] Pipfile.lock generado

[ ] Base de datos creada
[ ] Tabla usuarios creada
[ ] Tabla correctamente normalizada
[ ] UNIQUE(email) creado
[ ] Datos de prueba insertados
[ ] ERD creado
[ ] ERD guardado en resources/

[ ] flask_app creado
[ ] __init__.py creado
[ ] secret_key configurada

[ ] mysqlconnection.py funciona
[ ] usuario.py funciona
[ ] usuarios.py funciona
[ ] usuarios.html funciona
[ ] nuevo_usuario.html funciona
[ ] style.css funciona
[ ] server.py funciona

[ ] GET / funciona
[ ] GET /usuarios funciona
[ ] GET /usuarios/nuevo funciona
[ ] POST /usuarios/crear funciona

[ ] Crear usuario funciona
[ ] Mostrar usuarios funciona

[ ] Validación de nombre funciona
[ ] Validación de apellido funciona
[ ] Validación de email obligatorio funciona
[ ] Regex de email funciona

[ ] @staticmethod funciona
[ ] re.compile() funciona
[ ] .match() funciona

[ ] flash() funciona
[ ] Categorías de flash funcionan
[ ] secret_key funciona

[ ] redirect() funciona
[ ] url_for() funciona
[ ] request.form funciona

[ ] BONUS: email único
[ ] BONUS: datos conservados mediante session

[ ] Datos válidos se guardan
[ ] Datos inválidos NO se guardan
[ ] Múltiples errores pueden mostrarse
```

---

# 📦 Entregables

## GitHub

Entregar el enlace al repositorio que contenga el proyecto completo:

```text
usuarios_validacion/
│
├── flask_app/
├── resources/
├── Pipfile
├── Pipfile.lock
├── .gitignore
└── server.py
```

---

## Evidencia

Entregar una captura de pantalla donde se observe:

```text
Listado de usuarios
```

y otra evidencia donde se pueda observar:

```text
Formulario de creación
+
mensaje de validación
```

---

## ERD

El repositorio debe contener obligatoriamente:

```text
resources/
└── esquema_usuarios_erd.mwb
```

---

# 🎓 Aprendizaje final

Al terminar esta práctica, el estudiante debe poder explicar:

```text
request.form
      ↓
recibe información

validar_usuario()
      ↓
comprueba información

EMAIL_REGEX
      ↓
comprueba patrón del email

flash()
      ↓
informa errores

session
      ↓
conserva temporalmente datos

email_existe()
      ↓
consulta si el email ya existe

save()
      ↓
guarda información

redirect()
      ↓
realiza el siguiente GET
```

El principio fundamental es:

> **Nunca debemos guardar directamente la información recibida desde un formulario sin validarla previamente. La aplicación debe comprobar los datos en el backend, informar al usuario cuando existe un error y almacenar el registro solamente cuando la información cumple las reglas establecidas.**