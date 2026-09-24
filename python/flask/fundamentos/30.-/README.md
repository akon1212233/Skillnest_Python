# 🎵 Canciones — Relación Muchos a Muchos

## Descripción

Esta actividad integra los contenidos trabajados anteriormente sobre **Flask, MySQL, PyMySQL, POO, Jinja2, formularios, sentencias preparadas, MVC y relaciones muchos a muchos**.

Se construirá una aplicación donde los **usuarios pueden marcar canciones como favoritas** y una misma canción puede ser favorita de muchos usuarios.

La relación se resolverá mediante una tabla intermedia:

```text
usuarios
    N
    │
    │
    ▼
favoritos
    ▲
    │
    │
    N
canciones
```

La aplicación permitirá trabajar la relación desde ambos sentidos:

```text
Usuario → sus canciones favoritas

Canción → usuarios que la tienen como favorita
```

---

# 🎯 Objetivos

Al finalizar la actividad se deberá poder:

- Crear usuarios.
- Visualizar usuarios.
- Crear canciones.
- Visualizar canciones.
- Consultar un usuario.
- Consultar una canción.
- Agregar una canción a los favoritos de un usuario.
- Agregar una canción a los favoritos desde la página de la canción.
- Consultar las relaciones almacenadas en `favoritos`.
- Evitar favoritos duplicados.
- Aplicar una relación muchos a muchos mediante una tabla intermedia.
- Utilizar MVC para organizar el proyecto.

---

# 🧠 Modelo de datos

La base de datos se llamará:

```text
esquema_canciones
```

Tendrá tres tablas.

## `usuarios`

```text
usuarios
│
├── id
├── nombre
├── email
├── contrasena
├── created_at
└── updated_at
```

## `canciones`

```text
canciones
│
├── id
├── titulo
├── artista
├── created_at
└── updated_at
```

## `favoritos`

```text
favoritos
│
├── usuario_id
└── cancion_id
```

---

# 🔗 Relación muchos a muchos

La relación conceptual es:

```text
USUARIO N : N CANCIÓN
```

Pero en una base de datos relacional se implementa mediante una tabla intermedia:

```text
USUARIO
   │
   │ 1
   │
   │ N
   ▼
FAVORITOS
   ▲
   │ N
   │
   │ 1
   │
CANCIÓN
```

Por lo tanto:

```text
usuarios.id
      ↑
      │
favoritos.usuario_id
```

y:

```text
canciones.id
      ↑
      │
favoritos.cancion_id
```

---

# 🔐 Clave primaria de `favoritos`

La tabla intermedia debe utilizar una clave primaria compuesta:

```text
(usuario_id, cancion_id)
```

Esto permite que:

```text
Usuario 1 → Canción 2
Usuario 1 → Canción 5
Usuario 2 → Canción 2
```

sean relaciones diferentes.

Pero no permite:

```text
Usuario 1 → Canción 2
Usuario 1 → Canción 2
```

dos veces.

---

# 📐 Estructura SQL esperada

> En esta actividad el archivo SQL debe formar parte del proyecto, pero la estructura lógica de la base de datos es la siguiente. Los estudiantes pueden construirla en MySQL Workbench a partir del ERD proporcionado.

### `usuarios`

```text
id             INT             PK / AUTO_INCREMENT
nombre         VARCHAR(45)
email          VARCHAR(45)
contrasena     VARCHAR(45)
created_at     DATETIME
updated_at     DATETIME
```

### `canciones`

```text
id             INT             PK / AUTO_INCREMENT
titulo         VARCHAR(45)
artista        VARCHAR(45)
created_at     DATETIME
updated_at     DATETIME
```

### `favoritos`

```text
usuario_id     INT             PK / FK → usuarios.id
cancion_id     INT             PK / FK → canciones.id
```

La clave primaria de `favoritos` será:

```text
(usuario_id, cancion_id)
```

---

# 📁 Recursos

Todo proyecto que utilice una base de datos debe incluir:

```text
resources/
```

Dentro debe mantenerse el ERD utilizado.

```text
resources/
└── esquema_canciones_erd.mwb
```

También puede incluirse la imagen correspondiente:

```text
resources/
├── esquema_canciones_erd.mwb
└── esquema_canciones_erd.png
```

---

# 🏗️ Arquitectura MVC

El proyecto utilizará la arquitectura modular trabajada anteriormente.

```text
canciones_app/
│
├── flask_app/
│   │
│   ├── __init__.py
│   │
│   ├── config/
│   │   ├
│   │   └── mysqlconnection.py
│   │
│   ├── controllers/
│   │   ├
│   │   └── canciones.py
│   │
│   ├── models/
│   │   ├
│   │   ├── usuario.py
│   │   ├── cancion.py
│   │   └── favorito.py
│   │
│   ├── templates/
│   │   ├── usuarios.html
│   │   ├── canciones.html
│   │   ├── mostrar_usuario.html
│   │   └── mostrar_cancion.html
│   │
│   └── static/
│       └── css/
│           └── style.css
│
├── resources/
│   └── esquema_canciones_erd.mwb
│
├── Pipfile
├── Pipfile.lock
└── server.py
```

---

# 🐍 Pipenv

Instalar dependencias:

```bash
pipenv install flask pymysql
```

Ejecutar:

```bash
pipenv run python server.py
```

También puede activarse el entorno:

```bash
pipenv shell
```

y luego:

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

# ⚙️ `flask_app/__init__.py`

```python
from flask import Flask

app = Flask(__name__)

# Necesaria para utilizar mensajes flash.
# En un proyecto real la clave debe mantenerse fuera del código.
app.secret_key = "clave-secreta-desarrollo"
```

---

# 🔌 `flask_app/config/__init__.py`

```python
# Paquete de configuración de la aplicación.
```

---

# 🔌 `flask_app/config/mysqlconnection.py`

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

        SELECT  → lista de diccionarios.
        INSERT  → ID generado.
        UPDATE  → filas afectadas.
        DELETE  → filas afectadas.
        Error   → False.
        """

        with self.connection.cursor() as cursor:
            try:
                cursor.execute(query, data)

                if query.strip().lower().startswith("select"):
                    return cursor.fetchall()

                if query.strip().lower().startswith("insert"):
                    return cursor.lastrowid

                return cursor.rowcount

            except Exception as e:
                print("Something went wrong:", e)
                return False

            finally:
                self.connection.close()


def connectToMySQL(db):
    """
    Devuelve una instancia de MySQLConnection.
    """

    return MySQLConnection(db)
```

> Configura `user` y `password` según tu instalación local de MySQL.

---

# 👤 `flask_app/models/usuario.py`

```python
from flask_app.config.mysqlconnection import connectToMySQL


class Usuario:
    """
    Representa un registro de la tabla usuarios.
    """

    def __init__(self, data):
        self.id = data["id"]
        self.nombre = data["nombre"]
        self.email = data["email"]
        self.contrasena = data["contrasena"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.favoritos = []

    @classmethod
    def get_all(cls):
        """
        Obtiene todos los usuarios.
        """

        query = """
            SELECT
                id,
                nombre,
                email,
                contrasena,
                created_at,
                updated_at
            FROM usuarios
            ORDER BY id;
        """

        resultados = connectToMySQL(
            "esquema_canciones"
        ).query_db(query)

        usuarios = []

        for usuario in resultados:
            usuarios.append(cls(usuario))

        return usuarios

    @classmethod
    def get_by_id(cls, id):
        """
        Obtiene un usuario específico.
        """

        query = """
            SELECT
                id,
                nombre,
                email,
                contrasena,
                created_at,
                updated_at
            FROM usuarios
            WHERE id = %(id)s;
        """

        data = {
            "id": id
        }

        resultados = connectToMySQL(
            "esquema_canciones"
        ).query_db(query, data)

        if resultados:
            return cls(resultados[0])

        return None

    @classmethod
    def save(cls, data):
        """
        Crea un nuevo usuario.
        """

        query = """
            INSERT INTO usuarios
            (
                nombre,
                email,
                contrasena
            )
            VALUES
            (
                %(nombre)s,
                %(email)s,
                %(contrasena)s
            );
        """

        return connectToMySQL(
            "esquema_canciones"
        ).query_db(query, data)

    @classmethod
    def get_by_id_with_favorites(cls, data):
        """
        Obtiene un usuario y todas las canciones
        que tiene marcadas como favoritas.
        """

        query = """
            SELECT
                usuarios.id AS usuario_id,
                usuarios.nombre AS usuario_nombre,
                usuarios.email AS usuario_email,
                usuarios.contrasena AS usuario_contrasena,
                usuarios.created_at AS usuario_created_at,
                usuarios.updated_at AS usuario_updated_at,

                canciones.id AS cancion_id,
                canciones.titulo AS cancion_titulo,
                canciones.artista AS cancion_artista,
                canciones.created_at AS cancion_created_at,
                canciones.updated_at AS cancion_updated_at

            FROM usuarios

            LEFT JOIN favoritos
                ON favoritos.usuario_id = usuarios.id

            LEFT JOIN canciones
                ON favoritos.cancion_id = canciones.id

            WHERE usuarios.id = %(id)s;
        """

        resultados = connectToMySQL(
            "esquema_canciones"
        ).query_db(query, data)

        if not resultados:
            return None

        usuario_data = {
            "id": resultados[0]["usuario_id"],
            "nombre": resultados[0]["usuario_nombre"],
            "email": resultados[0]["usuario_email"],
            "contrasena": resultados[0]["usuario_contrasena"],
            "created_at": resultados[0]["usuario_created_at"],
            "updated_at": resultados[0]["usuario_updated_at"]
        }

        usuario = cls(usuario_data)

        for fila in resultados:

            if fila["cancion_id"] is not None:

                usuario.favoritos.append({
                    "id": fila["cancion_id"],
                    "titulo": fila["cancion_titulo"],
                    "artista": fila["cancion_artista"],
                    "created_at": fila["cancion_created_at"],
                    "updated_at": fila["cancion_updated_at"]
                })

        return usuario
```

---

# 🎵 `flask_app/models/cancion.py`

```python
from flask_app.config.mysqlconnection import connectToMySQL


class Cancion:
    """
    Representa un registro de la tabla canciones.
    """

    def __init__(self, data):
        self.id = data["id"]
        self.titulo = data["titulo"]
        self.artista = data["artista"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.usuarios = []

    @classmethod
    def get_all(cls):
        """
        Obtiene todas las canciones.
        """

        query = """
            SELECT
                id,
                titulo,
                artista,
                created_at,
                updated_at
            FROM canciones
            ORDER BY id;
        """

        resultados = connectToMySQL(
            "esquema_canciones"
        ).query_db(query)

        canciones = []

        for cancion in resultados:
            canciones.append(cls(cancion))

        return canciones

    @classmethod
    def get_by_id(cls, id):
        """
        Obtiene una canción por su ID.
        """

        query = """
            SELECT
                id,
                titulo,
                artista,
                created_at,
                updated_at
            FROM canciones
            WHERE id = %(id)s;
        """

        data = {
            "id": id
        }

        resultados = connectToMySQL(
            "esquema_canciones"
        ).query_db(query, data)

        if resultados:
            return cls(resultados[0])

        return None

    @classmethod
    def save(cls, data):
        """
        Crea una nueva canción.
        """

        query = """
            INSERT INTO canciones
            (
                titulo,
                artista
            )
            VALUES
            (
                %(titulo)s,
                %(artista)s
            );
        """

        return connectToMySQL(
            "esquema_canciones"
        ).query_db(query, data)

    @classmethod
    def get_by_id_with_users(cls, data):
        """
        Obtiene una canción y todos los usuarios
        que la tienen como favorita.
        """

        query = """
            SELECT
                canciones.id AS cancion_id,
                canciones.titulo AS cancion_titulo,
                canciones.artista AS cancion_artista,
                canciones.created_at AS cancion_created_at,
                canciones.updated_at AS cancion_updated_at,

                usuarios.id AS usuario_id,
                usuarios.nombre AS usuario_nombre,
                usuarios.email AS usuario_email,
                usuarios.contrasena AS usuario_contrasena,
                usuarios.created_at AS usuario_created_at,
                usuarios.updated_at AS usuario_updated_at

            FROM canciones

            LEFT JOIN favoritos
                ON favoritos.cancion_id = canciones.id

            LEFT JOIN usuarios
                ON favoritos.usuario_id = usuarios.id

            WHERE canciones.id = %(id)s;
        """

        resultados = connectToMySQL(
            "esquema_canciones"
        ).query_db(query, data)

        if not resultados:
            return None

        cancion_data = {
            "id": resultados[0]["cancion_id"],
            "titulo": resultados[0]["cancion_titulo"],
            "artista": resultados[0]["cancion_artista"],
            "created_at": resultados[0]["cancion_created_at"],
            "updated_at": resultados[0]["cancion_updated_at"]
        }

        cancion = cls(cancion_data)

        for fila in resultados:

            if fila["usuario_id"] is not None:

                cancion.usuarios.append({
                    "id": fila["usuario_id"],
                    "nombre": fila["usuario_nombre"],
                    "email": fila["usuario_email"],
                    "contrasena": fila["usuario_contrasena"],
                    "created_at": fila["usuario_created_at"],
                    "updated_at": fila["usuario_updated_at"]
                })

        return cancion

    @classmethod
    def get_users_not_favorited(cls, data):
        """
        Obtiene solamente los usuarios que todavía
        no han marcado la canción como favorita.
        """

        query = """
            SELECT
                usuarios.id,
                usuarios.nombre,
                usuarios.email,
                usuarios.contrasena,
                usuarios.created_at,
                usuarios.updated_at

            FROM usuarios

            LEFT JOIN favoritos
                ON favoritos.usuario_id = usuarios.id
                AND favoritos.cancion_id = %(cancion_id)s

            WHERE favoritos.usuario_id IS NULL

            ORDER BY usuarios.nombre;
        """

        return connectToMySQL(
            "esquema_canciones"
        ).query_db(query, data)
```

---

# ⭐ `flask_app/models/favorito.py`

```python
from flask_app.config.mysqlconnection import connectToMySQL


class Favorito:
    """
    Representa una relación entre un usuario y una canción.
    """

    @classmethod
    def existe(cls, data):
        """
        Comprueba si la relación ya existe.
        """

        query = """
            SELECT
                usuario_id,
                cancion_id
            FROM favoritos
            WHERE usuario_id = %(usuario_id)s
              AND cancion_id = %(cancion_id)s;
        """

        resultado = connectToMySQL(
            "esquema_canciones"
        ).query_db(query, data)

        return bool(resultado)

    @classmethod
    def agregar(cls, data):
        """
        Agrega una canción a los favoritos
        de un usuario.
        """

        query = """
            INSERT INTO favoritos
            (
                usuario_id,
                cancion_id
            )
            VALUES
            (
                %(usuario_id)s,
                %(cancion_id)s
            );
        """

        return connectToMySQL(
            "esquema_canciones"
        ).query_db(query, data)
```

---

# 🎮 Controlador

## `flask_app/controllers/__init__.py`

```python
# Paquete de controladores.
```

---

# 📄 `flask_app/controllers/canciones.py`

```python
from flask_app import app

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_app.models.usuario import Usuario
from flask_app.models.cancion import Cancion
from flask_app.models.favorito import Favorito


# ==========================================================
# USUARIOS
# ==========================================================

@app.route("/")
def inicio():
    """
    La página principal redirige a Usuarios.
    """

    return redirect(
        url_for("usuarios")
    )


@app.route("/usuarios")
def usuarios():
    """
    Muestra todos los usuarios.
    """

    lista_usuarios = Usuario.get_all()

    return render_template(
        "usuarios.html",
        usuarios=lista_usuarios
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
    Crea un nuevo usuario.
    """

    nombre = request.form.get(
        "nombre",
        ""
    ).strip()

    email = request.form.get(
        "email",
        ""
    ).strip()

    contrasena = request.form.get(
        "contrasena",
        ""
    ).strip()


    if not nombre or not email or not contrasena:

        flash(
            "Todos los campos son obligatorios.",
            "danger"
        )

        return redirect(
            url_for("usuarios")
        )


    data = {
        "nombre": nombre,
        "email": email,
        "contrasena": contrasena
    }


    resultado = Usuario.save(
        data
    )


    if resultado is False:

        flash(
            "No fue posible crear el usuario.",
            "danger"
        )

        return redirect(
            url_for("usuarios")
        )


    flash(
        "Usuario creado correctamente.",
        "success"
    )


    return redirect(
        url_for("usuarios")
    )


# ==========================================================
# MOSTRAR USUARIO
# ==========================================================

@app.route(
    "/usuarios/<int:id>"
)
def mostrar_usuario(id):
    """
    Muestra un usuario y sus canciones favoritas.
    """

    data = {
        "id": id
    }


    usuario = Usuario.get_by_id_with_favorites(
        data
    )


    if usuario is None:

        return (
            "Usuario no encontrado",
            404
        )


    canciones = Cancion.get_all()


    return render_template(
        "mostrar_usuario.html",
        usuario=usuario,
        canciones=canciones
    )


# ==========================================================
# CANCIONES
# ==========================================================

@app.route("/canciones")
def canciones():
    """
    Muestra todas las canciones.
    """

    lista_canciones = Cancion.get_all()

    return render_template(
        "canciones.html",
        canciones=lista_canciones
    )


# ==========================================================
# CREAR CANCIÓN
# ==========================================================

@app.route(
    "/canciones/crear",
    methods=["POST"]
)
def crear_cancion():
    """
    Crea una nueva canción.
    """

    titulo = request.form.get(
        "titulo",
        ""
    ).strip()

    artista = request.form.get(
        "artista",
        ""
    ).strip()


    if not titulo or not artista:

        flash(
            "Título y artista son obligatorios.",
            "danger"
        )

        return redirect(
            url_for("canciones")
        )


    data = {
        "titulo": titulo,
        "artista": artista
    }


    resultado = Cancion.save(
        data
    )


    if resultado is False:

        flash(
            "No fue posible crear la canción.",
            "danger"
        )

        return redirect(
            url_for("canciones")
        )


    flash(
        "Canción creada correctamente.",
        "success"
    )


    return redirect(
        url_for("canciones")
    )


# ==========================================================
# MOSTRAR CANCIÓN
# ==========================================================

@app.route(
    "/canciones/<int:id>"
)
def mostrar_cancion(id):
    """
    Muestra una canción y los usuarios
    que la marcaron como favorita.
    """

    data = {
        "id": id
    }


    cancion = Cancion.get_by_id_with_users(
        data
    )


    if cancion is None:

        return (
            "Canción no encontrada",
            404
        )


    usuarios = Cancion.get_users_not_favorited({
        "cancion_id": id
    })


    return render_template(
        "mostrar_cancion.html",
        cancion=cancion,
        usuarios=usuarios
    )


# ==========================================================
# AGREGAR FAVORITO
# ==========================================================

@app.route(
    "/favoritos/agregar",
    methods=["POST"]
)
def agregar_favorito():
    """
    Crea una relación entre un usuario y una canción.

    El formulario indica desde qué página se realizó
    la operación mediante el campo "origen".
    """

    usuario_id_texto = request.form.get(
        "usuario_id"
    )

    cancion_id_texto = request.form.get(
        "cancion_id"
    )

    origen = request.form.get(
        "origen"
    )


    if not usuario_id_texto or not cancion_id_texto:

        flash(
            "Debes seleccionar los datos necesarios.",
            "danger"
        )

        return redirect(
            url_for("usuarios")
        )


    try:

        usuario_id = int(
            usuario_id_texto
        )

        cancion_id = int(
            cancion_id_texto
        )

    except ValueError:

        flash(
            "Los identificadores no son válidos.",
            "danger"
        )

        return redirect(
            url_for("usuarios")
        )


    # ------------------------------------------------------
    # Comprobar que el usuario exista.
    # ------------------------------------------------------

    usuario = Usuario.get_by_id(
        usuario_id
    )


    if usuario is None:

        flash(
            "El usuario seleccionado no existe.",
            "danger"
        )

        return redirect(
            url_for("usuarios")
        )


    # ------------------------------------------------------
    # Comprobar que la canción exista.
    # ------------------------------------------------------

    cancion = Cancion.get_by_id(
        cancion_id
    )


    if cancion is None:

        flash(
            "La canción seleccionada no existe.",
            "danger"
        )

        return redirect(
            url_for("canciones")
        )


    data = {
        "usuario_id": usuario_id,
        "cancion_id": cancion_id
    }


    # ------------------------------------------------------
    # Evitar favoritos duplicados.
    # ------------------------------------------------------

    if Favorito.existe(data):

        flash(
            "Esta canción ya está entre los favoritos del usuario.",
            "warning"
        )

    else:

        resultado = Favorito.agregar(
            data
        )


        if resultado is False:

            flash(
                "No fue posible agregar el favorito.",
                "danger"
            )

        else:

            flash(
                "Favorito agregado correctamente.",
                "success"
            )


    # ------------------------------------------------------
    # Volver a la página desde donde se realizó la acción.
    # ------------------------------------------------------

    if origen == "usuario":

        return redirect(
            url_for(
                "mostrar_usuario",
                id=usuario_id
            )
        )


    if origen == "cancion":

        return redirect(
            url_for(
                "mostrar_cancion",
                id=cancion_id
            )
        )


    return redirect(
        url_for("usuarios")
    )
```

---

# 👁️ Vista Usuarios

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
        href="{{ url_for('static', filename='css/style.css') }}"
    >

</head>

<body>

<div class="container py-5">


    <div class="row g-4">


        <!-- ==================================================
             NUEVO USUARIO
        =================================================== -->

        <div class="col-lg-5">

            <div class="card shadow-sm border-0">

                <div class="card-body p-4">

                    <h1 class="h3 mb-4">
                        Nuevo Usuario
                    </h1>


                    {% with mensajes = get_flashed_messages(
                        with_categories=true
                    ) %}

                        {% if mensajes %}

                            {% for categoria, mensaje in mensajes %}

                                <div
                                    class="alert alert-{{ categoria }}"
                                >
                                    {{ mensaje }}
                                </div>

                            {% endfor %}

                        {% endif %}

                    {% endwith %}


                    <form
                        action="{{ url_for('crear_usuario') }}"
                        method="POST"
                    >


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
                                maxlength="45"
                                required
                            >

                        </div>


                        <div class="mb-3">

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
                                maxlength="45"
                                required
                            >

                        </div>


                        <div class="mb-4">

                            <label
                                for="contrasena"
                                class="form-label"
                            >
                                PW
                            </label>

                            <input
                                type="password"
                                id="contrasena"
                                name="contrasena"
                                class="form-control"
                                maxlength="45"
                                required
                            >

                        </div>


                        <button
                            type="submit"
                            class="btn btn-primary"
                        >
                            Crear
                        </button>

                    </form>

                </div>

            </div>

        </div>


        <!-- ==================================================
             TODOS LOS USUARIOS
        =================================================== -->

        <div class="col-lg-7">

            <div class="card shadow-sm border-0">

                <div class="card-body p-4">

                    <div class="d-flex justify-content-between align-items-center mb-4">

                        <h2 class="h3 mb-0">
                            Todos los Usuarios
                        </h2>


                        <a
                            href="{{ url_for('canciones') }}"
                            class="btn btn-outline-primary btn-sm"
                        >
                            Canciones
                        </a>

                    </div>


                    {% if usuarios %}

                        <div class="list-group">


                            {% for usuario in usuarios %}

                                <a
                                    href="{{ url_for('mostrar_usuario', id=usuario.id) }}"
                                    class="list-group-item list-group-item-action"
                                >

                                    {{ usuario.nombre }}

                                </a>

                            {% endfor %}


                        </div>


                    {% else %}

                        <div class="alert alert-info">
                            No existen usuarios registrados.
                        </div>

                    {% endif %}


                </div>

            </div>

        </div>

    </div>

</div>

</body>

</html>
```

---

# 🎵 Vista Canciones

## `flask_app/templates/canciones.html`

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
        Canciones
    </title>


    <link
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.7/dist/css/bootstrap.min.css"
        rel="stylesheet"
    >


    <link
        rel="stylesheet"
        href="{{ url_for('static', filename='css/style.css') }}"
    >

</head>

<body>

<div class="container py-5">


    <div class="row g-4">


        <!-- ==================================================
             NUEVA CANCIÓN
        =================================================== -->

        <div class="col-lg-5">

            <div class="card shadow-sm border-0">

                <div class="card-body p-4">

                    <h1 class="h3 mb-4">
                        Nueva Canción
                    </h1>


                    {% with mensajes = get_flashed_messages(
                        with_categories=true
                    ) %}

                        {% if mensajes %}

                            {% for categoria, mensaje in mensajes %}

                                <div
                                    class="alert alert-{{ categoria }}"
                                >
                                    {{ mensaje }}
                                </div>

                            {% endfor %}

                        {% endif %}

                    {% endwith %}


                    <form
                        action="{{ url_for('crear_cancion') }}"
                        method="POST"
                    >


                        <div class="mb-3">

                            <label
                                for="titulo"
                                class="form-label"
                            >
                                Título
                            </label>

                            <input
                                type="text"
                                id="titulo"
                                name="titulo"
                                class="form-control"
                                maxlength="45"
                                required
                            >

                        </div>


                        <div class="mb-4">

                            <label
                                for="artista"
                                class="form-label"
                            >
                                Artista
                            </label>

                            <input
                                type="text"
                                id="artista"
                                name="artista"
                                class="form-control"
                                maxlength="45"
                                required
                            >

                        </div>


                        <button
                            type="submit"
                            class="btn btn-primary"
                        >
                            Crear
                        </button>

                    </form>


                    <div class="mt-4">

                        <a
                            href="{{ url_for('usuarios') }}"
                        >
                            Inicio
                        </a>

                    </div>

                </div>

            </div>

        </div>


        <!-- ==================================================
             TODAS LAS CANCIONES
        =================================================== -->

        <div class="col-lg-7">

            <div class="card shadow-sm border-0">

                <div class="card-body p-4">


                    <h2 class="h3 mb-4">
                        Todas las Canciones
                    </h2>


                    {% if canciones %}

                        <div class="list-group">


                            {% for cancion in canciones %}

                                <a
                                    href="{{ url_for('mostrar_cancion', id=cancion.id) }}"
                                    class="list-group-item list-group-item-action"
                                >

                                    <strong>
                                        {{ cancion.titulo }}
                                    </strong>

                                    <span class="text-muted">
                                        — {{ cancion.artista }}
                                    </span>

                                </a>

                            {% endfor %}


                        </div>


                    {% else %}

                        <div class="alert alert-info">
                            No existen canciones registradas.
                        </div>

                    {% endif %}


                </div>

            </div>

        </div>

    </div>

</div>

</body>

</html>
```

---

# 👤 Vista Mostrar Usuario

## `flask_app/templates/mostrar_usuario.html`

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
        {{ usuario.nombre }}
    </title>


    <link
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.7/dist/css/bootstrap.min.css"
        rel="stylesheet"
    >


    <link
        rel="stylesheet"
        href="{{ url_for('static', filename='css/style.css') }}"
    >

</head>

<body>

<div class="container py-5">


    <div class="d-flex justify-content-between align-items-center mb-4">

        <div>

            <h1>
                {{ usuario.nombre }}
            </h1>

            <p class="text-muted">
                {{ usuario.email }}
            </p>

        </div>


        <a
            href="{{ url_for('usuarios') }}"
            class="btn btn-outline-primary"
        >
            Inicio
        </a>

    </div>


    <div class="row g-4">


        <!-- ==================================================
             FAVORITOS
        =================================================== -->

        <div class="col-lg-7">

            <div class="card shadow-sm border-0">

                <div class="card-body p-4">


                    <h2 class="h4 mb-4">
                        Favoritos
                    </h2>


                    {% if usuario.favoritos %}


                        <div class="table-responsive">

                            <table class="table table-hover">

                                <thead class="table-dark">

                                    <tr>

                                        <th>
                                            Canción
                                        </th>

                                        <th>
                                            Artista
                                        </th>

                                    </tr>

                                </thead>


                                <tbody>


                                    {% for cancion in usuario.favoritos %}

                                        <tr>

                                            <td>
                                                {{ cancion["titulo"] }}
                                            </td>

                                            <td>
                                                {{ cancion["artista"] }}
                                            </td>

                                        </tr>

                                    {% endfor %}


                                </tbody>

                            </table>

                        </div>


                    {% else %}

                        <div class="alert alert-info">
                            Este usuario todavía no tiene canciones favoritas.
                        </div>

                    {% endif %}


                </div>

            </div>

        </div>


        <!-- ==================================================
             AGREGAR FAVORITO
        =================================================== -->

        <div class="col-lg-5">

            <div class="card shadow-sm border-0">

                <div class="card-body p-4">


                    <h2 class="h4 mb-4">
                        Agregar Favorito
                    </h2>


                    <form
                        action="{{ url_for('agregar_favorito') }}"
                        method="POST"
                    >


                        <!-- El usuario actual se envía oculto. -->

                        <input
                            type="hidden"
                            name="usuario_id"
                            value="{{ usuario.id }}"
                        >


                        <input
                            type="hidden"
                            name="origen"
                            value="usuario"
                        >


                        <div class="mb-4">

                            <label
                                for="cancion_id"
                                class="form-label"
                            >
                                Canción
                            </label>


                            <select
                                id="cancion_id"
                                name="cancion_id"
                                class="form-select"
                                required
                            >

                                <option value="">
                                    Selecciona una canción
                                </option>


                                {% for cancion in canciones %}

                                    <option
                                        value="{{ cancion.id }}"
                                    >

                                        {{ cancion.titulo }}

                                    </option>

                                {% endfor %}

                            </select>

                        </div>


                        <button
                            type="submit"
                            class="btn btn-primary"
                        >

                            Agregar

                        </button>


                    </form>


                    <div class="mt-4">

                        <a
                            href="{{ url_for('canciones') }}"
                        >
                            Agregar Canción
                        </a>

                    </div>

                </div>

            </div>

        </div>


    </div>


    {% with mensajes = get_flashed_messages(
        with_categories=true
    ) %}

        {% if mensajes %}

            <div class="mt-4">

                {% for categoria, mensaje in mensajes %}

                    <div
                        class="alert alert-{{ categoria }}"
                    >
                        {{ mensaje }}
                    </div>

                {% endfor %}

            </div>

        {% endif %}

    {% endwith %}


</div>

</body>

</html>
```

---

# 🎼 Vista Mostrar Canción

## `flask_app/templates/mostrar_cancion.html`

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
        {{ cancion.titulo }}
    </title>


    <link
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.7/dist/css/bootstrap.min.css"
        rel="stylesheet"
    >


    <link
        rel="stylesheet"
        href="{{ url_for('static', filename='css/style.css') }}"
    >

</head>

<body>

<div class="container py-5">


    <div class="d-flex justify-content-between align-items-center mb-5">

        <div>

            <h1>
                {{ cancion.titulo }}
            </h1>

            <h2 class="h4 text-muted">
                {{ cancion.artista }}
            </h2>

        </div>


        <a
            href="{{ url_for('canciones') }}"
            class="btn btn-outline-primary"
        >
            Inicio
        </a>

    </div>


    <div class="row g-4">


        <!-- ==================================================
             USUARIOS QUE LA TIENEN COMO FAVORITA
        =================================================== -->

        <div class="col-lg-7">

            <div class="card shadow-sm border-0">

                <div class="card-body p-4">


                    <h2 class="h4 mb-4">
                        En los favoritos de:
                    </h2>


                    {% if cancion.usuarios %}


                        <ul class="list-group">


                            {% for usuario in cancion.usuarios %}

                                <li
                                    class="list-group-item"
                                >

                                    {{ usuario["nombre"] }}

                                </li>

                            {% endfor %}


                        </ul>


                    {% else %}

                        <div class="alert alert-info">
                            Esta canción todavía no está en los favoritos de ningún usuario.
                        </div>

                    {% endif %}


                </div>

            </div>

        </div>


        <!-- ==================================================
             AGREGAR FAVORITO
        =================================================== -->

        <div class="col-lg-5">

            <div class="card shadow-sm border-0">

                <div class="card-body p-4">


                    <h2 class="h4 mb-4">
                        Agregar Favorito
                    </h2>


                    {% if usuarios %}


                        <form
                            action="{{ url_for('agregar_favorito') }}"
                            method="POST"
                        >


                            <input
                                type="hidden"
                                name="cancion_id"
                                value="{{ cancion.id }}"
                            >


                            <input
                                type="hidden"
                                name="origen"
                                value="cancion"
                            >


                            <div class="mb-4">

                                <label
                                    for="usuario_id"
                                    class="form-label"
                                >
                                    Usuario
                                </label>


                                <select
                                    id="usuario_id"
                                    name="usuario_id"
                                    class="form-select"
                                    required
                                >

                                    <option value="">
                                        Selecciona un usuario
                                    </option>


                                    {% for usuario in usuarios %}

                                        <option
                                            value="{{ usuario['id'] }}"
                                        >

                                            {{ usuario["nombre"] }}

                                        </option>

                                    {% endfor %}

                                </select>

                            </div>


                            <button
                                type="submit"
                                class="btn btn-primary"
                            >

                                Agregar

                            </button>


                        </form>


                    {% else %}

                        <div class="alert alert-success">

                            Todos los usuarios que existen
                            ya tienen esta canción como favorita.

                        </div>

                    {% endif %}


                </div>

            </div>

        </div>


    </div>


    {% with mensajes = get_flashed_messages(
        with_categories=true
    ) %}

        {% if mensajes %}

            <div class="mt-4">

                {% for categoria, mensaje in mensajes %}

                    <div
                        class="alert alert-{{ categoria }}"
                    >
                        {{ mensaje }}
                    </div>

                {% endfor %}

            </div>

        {% endif %}

    {% endwith %}


</div>

</body>

</html>
```

---

# 🎨 `flask_app/static/css/style.css`

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

.form-control,
.form-select {
    border-radius: 7px;
}

.btn {
    border-radius: 7px;
}

.list-group-item {
    padding: 14px 16px;
}

.table {
    vertical-align: middle;
}

.alert {
    border-radius: 8px;
}
```

---

# 📄 `server.py`

```python
from flask_app import app

# Importamos el controlador para registrar todas las rutas.
from flask_app.controllers import canciones


if __name__ == "__main__":
    app.run(debug=True)
```

---

# 🔄 Flujo de creación de un usuario

```text
usuarios.html
      ↓
Formulario
      ↓
POST /usuarios/crear
      ↓
request.form
      ↓
data
      ↓
Usuario.save()
      ↓
INSERT INTO usuarios
      ↓
MySQL
      ↓
redirect()
      ↓
/usuarios
```

---

# 🔄 Flujo de creación de una canción

```text
canciones.html
      ↓
Formulario
      ↓
POST /canciones/crear
      ↓
request.form
      ↓
data
      ↓
Cancion.save()
      ↓
INSERT INTO canciones
      ↓
MySQL
      ↓
redirect()
      ↓
/canciones
```

---

# ⭐ Flujo de agregar un favorito

## Desde un usuario

```text
Mostrar Usuario
      ↓
seleccionar canción
      ↓
POST /favoritos/agregar
      ↓
usuario_id
cancion_id
      ↓
Favorito.existe()
      ↓
Favorito.agregar()
      ↓
INSERT INTO favoritos
      ↓
redirect()
      ↓
Mostrar Usuario
```

---

## Desde una canción

```text
Mostrar Canción
      ↓
seleccionar usuario
      ↓
POST /favoritos/agregar
      ↓
usuario_id
cancion_id
      ↓
Favorito.existe()
      ↓
Favorito.agregar()
      ↓
INSERT INTO favoritos
      ↓
redirect()
      ↓
Mostrar Canción
```

---

# 🧠 La tabla `favoritos`

Supongamos:

```text
Usuario 1 = Soraya
Usuario 2 = Armando

Canción 1 = La Bamba
Canción 2 = Macarena
Canción 3 = De Música Ligera
```

Podemos registrar:

```text
usuario_id | cancion_id
-----------|-----------
1          | 1
1          | 3
2          | 1
2          | 2
```

Esto significa:

```text
Soraya
 ├── La Bamba
 └── De Música Ligera

Armando
 ├── La Bamba
 └── Macarena
```

Desde el otro lado:

```text
La Bamba
 ├── Soraya
 └── Armando

Macarena
 └── Armando

De Música Ligera
 └── Soraya
```

Esto demuestra la relación:

```text
USUARIO N : N CANCIÓN
```

---

# 🔎 Consultar la relación completa

En MySQL se puede comprobar mediante una consulta que una:

```text
usuarios
favoritos
canciones
```

conceptualmente:

```text
usuarios
    ↓
favoritos
    ↓
canciones
```

El resultado debe permitir identificar:

```text
Usuario
Canción
Artista
```

para cada relación registrada.

---

# 🧠 ¿Qué representa cada modelo?

```text
Usuario
   ↓
Representa una entidad de usuarios.

Cancion
   ↓
Representa una entidad de canciones.

Favorito
   ↓
Representa una relación entre ambas.
```

Es importante diferenciar:

```text
Usuario ≠ Favorito

Canción ≠ Favorito
```

`Favorito` no representa una persona ni una canción.

Representa:

```text
Usuario + Canción
```

---

# 🧩 ¿Por qué hay una tabla intermedia?

Sin una tabla intermedia sería difícil representar correctamente:

```text
Usuario 1
 ├── Canción 1
 ├── Canción 2
 └── Canción 3
```

y simultáneamente:

```text
Canción 1
 ├── Usuario 1
 ├── Usuario 2
 └── Usuario 3
```

La tabla:

```text
favoritos
```

resuelve ambas direcciones.

---

# 🧠 Bonus

En la página:

```text
/canciones/<id>
```

el `<select>` no debe mostrar usuarios que ya tengan esa canción como favorita.

Para eso utilizamos:

```python
Cancion.get_users_not_favorited(...)
```

La consulta utiliza el principio:

```text
TODOS LOS USUARIOS
        ↓
EXCLUIR LOS QUE YA ESTÁN EN FAVORITOS
        ↓
USUARIOS DISPONIBLES
```

Por eso, en la interfaz:

```text
Usuario A → ya tiene la canción
```

no aparecerá.

Mientras:

```text
Usuario B → todavía no la tiene
```

sí aparecerá.

---

# 🧠 Flujo del BONUS

```text
Mostrar Canción
       ↓
cancion_id
       ↓
buscar usuarios
       ↓
comparar con favoritos
       ↓
excluir usuarios existentes
       ↓
<select>
       ↓
mostrar solamente disponibles
```

---

# 🧪 Prueba funcional

## 1. Crear usuarios

Entrar en:

```text
http://127.0.0.1:5000/usuarios
```

Crear:

```text
Soraya Montenegro
```

```text
Armando Mendoza
```

---

## 2. Crear canciones

Entrar en:

```text
http://127.0.0.1:5000/canciones
```

Crear:

```text
La Bamba
```

```text
Macarena
```

```text
De Música Ligera
```

---

## 3. Agregar favorito desde usuario

Abrir:

```text
/usuarios/1
```

Seleccionar:

```text
La Bamba
```

Presionar:

```text
Agregar
```

La canción debe aparecer en:

```text
Favoritos
```

---

## 4. Agregar otro favorito

Desde el mismo usuario:

```text
De Música Ligera
```

Resultado:

```text
Soraya
 ├── La Bamba
 └── De Música Ligera
```

---

## 5. Ver canción

Abrir:

```text
/canciones/1
```

Debería aparecer:

```text
La Bamba
```

y:

```text
En los favoritos de:

Soraya
```

---

## 6. Agregar otro usuario desde la canción

Seleccionar:

```text
Armando Mendoza
```

Resultado:

```text
La Bamba

En los favoritos de:

Soraya
Armando
```

Esto demuestra que una canción puede pertenecer a varios favoritos.

---

# 🛡️ Probar duplicación

Intentar nuevamente:

```text
Soraya → La Bamba
```

La aplicación debe indicar:

```text
Esta canción ya está entre los favoritos del usuario.
```

y no crear otro registro.

---

# 🔎 Comprobación en MySQL

Consultar:

```text
usuarios
```

y comprobar que existan los usuarios.

Consultar:

```text
canciones
```

y comprobar que existan las canciones.

Finalmente consultar:

```text
favoritos
```

para verificar las relaciones.

Por ejemplo:

```text
usuario_id | cancion_id
-----------|-----------
1          | 1
1          | 3
2          | 1
```

---

# 🧠 Arquitectura final

```text
                         FLASK
                           │
                           ▼
                     CONTROLLER
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
           Usuario       Cancion      Favorito
              │            │            │
              └────────────┼────────────┘
                           │
                           ▼
                         MYSQL
```

---

# 📁 Estructura definitiva

```text
canciones_app/
│
├── flask_app/
│   │
│   ├── __init__.py
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   └── mysqlconnection.py
│   │
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── canciones.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── usuario.py
│   │   ├── cancion.py
│   │   └── favorito.py
│   │
│   ├── templates/
│   │   ├── usuarios.html
│   │   ├── canciones.html
│   │   ├── mostrar_usuario.html
│   │   └── mostrar_cancion.html
│   │
│   └── static/
│       └── css/
│           └── style.css
│
├── resources/
│   └── esquema_canciones_erd.mwb
│
├── Pipfile
├── Pipfile.lock
└── server.py
```

---

# 🧠 Conceptos fundamentales

| Concepto | Función |
|---|---|
| `usuarios` | Guarda usuarios |
| `canciones` | Guarda canciones |
| `favoritos` | Relaciona usuarios y canciones |
| `usuario_id` | FK hacia `usuarios.id` |
| `cancion_id` | FK hacia `canciones.id` |
| PK compuesta | Evita relaciones duplicadas |
| `<select>` | Permite seleccionar entidades |
| `request.form` | Recupera los IDs enviados |
| `INSERT` | Crea la relación |
| `JOIN` | Consulta relaciones entre tablas |
| `url_for()` | Genera URLs Flask |
| `redirect()` | Redirige después de un POST |
| `LEFT JOIN` | Permite conservar la entidad principal aunque no tenga relaciones |

---

# ✅ Checklist

```text
[ ] Pipenv configurado
[ ] Flask instalado
[ ] PyMySQL instalado
[ ] Pipfile creado
[ ] Pipfile.lock generado

[ ] Base de datos esquema_canciones creada
[ ] Tabla usuarios creada
[ ] Tabla canciones creada
[ ] Tabla favoritos creada
[ ] PRIMARY KEY compuesta creada
[ ] FOREIGN KEY usuario creada
[ ] FOREIGN KEY canción creada
[ ] ERD guardado en resources/

[ ] mysqlconnection.py funciona

[ ] Modelo Usuario funciona
[ ] Modelo Cancion funciona
[ ] Modelo Favorito funciona

[ ] /usuarios funciona
[ ] /canciones funciona
[ ] /usuarios/<id> funciona
[ ] /canciones/<id> funciona

[ ] Crear usuario funciona
[ ] Crear canción funciona

[ ] Select de canciones funciona
[ ] Select de usuarios funciona

[ ] Agregar favorito desde Usuario funciona
[ ] Agregar favorito desde Canción funciona

[ ] Favoritos aparecen en Mostrar Usuario
[ ] Usuarios aparecen en Mostrar Canción

[ ] Duplicados controlados
[ ] redirect() funciona
[ ] url_for() funciona
[ ] request.form funciona
[ ] Jinja2 funciona
[ ] Sentencias preparadas funcionan

[ ] BONUS implementado
```

---

# 📤 Entregables

## GitHub

Entregar el enlace al repositorio que contenga:

```text
canciones_app/
```

con:

```text
flask_app/
resources/
Pipfile
Pipfile.lock
server.py
```

## Evidencia

Entregar una captura del proyecto funcionando.

La evidencia debería mostrar, idealmente:

```text
Usuarios
        ↓
Mostrar Usuario
        ↓
Favoritos
```

y/o:

```text
Canciones
        ↓
Mostrar Canción
        ↓
Usuarios que la tienen como favorita
```

## ERD

El repositorio debe contener obligatoriamente:

```text
resources/
└── esquema_canciones_erd.mwb
```

---

# 🏁 Resultado final

La aplicación implementa una relación:

```text
USUARIO N : N CANCIÓN
```

utilizando:

```text
favoritos
```

como tabla intermedia.

El flujo completo es:

```text
Usuario
   │
   ▼
selecciona Canción
   │
   ▼
POST
   │
   ▼
request.form
   │
   ├── usuario_id
   └── cancion_id
   │
   ▼
Favorito.agregar()
   │
   ▼
favoritos
   │
   ▼
MySQL
```

Y la relación puede consultarse desde ambos sentidos:

```text
Usuario
   ↓
Favoritos
   ↓
Canciones
```

o:

```text
Canción
   ↓
Favoritos
   ↓
Usuarios
```

El concepto central es:

> **En una relación muchos a muchos, las entidades permanecen en sus propias tablas y una tabla intermedia almacena las relaciones entre ellas.**

En este proyecto:

```text
usuarios
     ↕
favoritos
     ↕
canciones
```

permite que un usuario tenga muchas canciones favoritas y que una canción pueda pertenecer a los favoritos de muchos usuarios.
Mostrando README.md