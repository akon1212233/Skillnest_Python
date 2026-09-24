# 👥 Seguidores — Relación de auto-unión (Self Join)

## Descripción

Esta actividad integra los contenidos trabajados sobre **Flask, MySQL, PyMySQL, POO, Jinja2, formularios POST, sentencias preparadas, MVC y relaciones entre tablas**, incorporando un concepto nuevo: la **auto-relación o Self Join**.

Se construirá una aplicación donde un usuario puede estar relacionado con otros usuarios mediante una tabla intermedia llamada `seguidores`.

La relación será:

```text
USUARIO N : N USUARIO
```

y se implementará mediante:

```text
usuarios
    ↕
seguidores
    ↕
usuarios
```

La aplicación permitirá crear usuarios, registrar relaciones de seguimiento y visualizar quién sigue a quién.

---

# 🎯 Objetivos

Al finalizar la actividad podrás:

- Comprender qué es una auto-relación.
- Comprender el concepto de `SELF JOIN`.
- Utilizar una misma tabla con dos roles diferentes dentro de una consulta.
- Utilizar claves foráneas que apuntan a la misma tabla.
- Crear una tabla intermedia para representar relaciones entre usuarios.
- Utilizar dos `<select>` con los usuarios disponibles.
- Crear usuarios mediante formularios.
- Registrar relaciones mediante `POST`.
- Utilizar `request.form`.
- Utilizar sentencias preparadas.
- Utilizar `redirect()` y `url_for()`.
- Aplicar MVC.
- Evitar relaciones duplicadas.

---

# 🧠 Concepto principal: ¿qué es una auto-relación?

Una auto-relación ocurre cuando una tabla se relaciona con registros de esa misma tabla.

En nuestro caso tenemos solamente una entidad:

```text
usuarios
```

Pero un usuario puede relacionarse con otro usuario.

Por ejemplo:

```text
Soraya Montenegro
        ↓
      sigue
        ↓
Luis F. de la Vega
```

Ambos son registros de:

```text
usuarios
```

No existe una segunda tabla llamada `personas`.

La relación se guarda en:

```text
seguidores
```

---

# 🔗 Modelo conceptual

```text
┌─────────────────┐
│    usuarios     │
├─────────────────┤
│ id              │
│ nombre          │
│ apellido        │
│ email           │
└────────┬────────┘
         │
         │ usuario_id
         ▼
┌─────────────────┐
│   seguidores    │
├─────────────────┤
│ id              │
│ usuario_id      │
│ seguidor_id     │
│ created_at      │
│ updated_at      │
└────────┬────────┘
         │
         │ seguidor_id
         ▼
┌─────────────────┐
│    usuarios     │
├─────────────────┤
│ id              │
│ nombre          │
│ apellido        │
│ email           │
└─────────────────┘
```

Las dos claves foráneas apuntan a:

```text
usuarios.id
```

---

# 🔑 ¿Qué significa cada campo?

Utilizaremos esta convención durante todo el proyecto:

```text
usuario_id
=
usuario al que estamos asociando un seguidor

seguidor_id
=
usuario que sigue al usuario anterior
```

Por ejemplo:

```text
usuario_id = 1
seguidor_id = 2
```

significa:

```text
El usuario 2 sigue al usuario 1.
```

Si:

```text
1 = Soraya Montenegro
2 = Luis F. de la Vega
```

entonces:

```text
Luis F. de la Vega
        ↓
      sigue
        ↓
Soraya Montenegro
```

> Es fundamental mantener esta convención de forma consistente en el SQL, los modelos, el controlador y las vistas.

---

# 🧩 ¿Por qué es un Self Join?

En una consulta normal podríamos hacer:

```sql
usuarios
    JOIN otra_tabla
```

Pero aquí hacemos:

```sql
usuarios u
    JOIN usuarios s
```

La tabla `usuarios` aparece dos veces.

La primera representa:

```text
u = usuario
```

La segunda representa:

```text
s = seguidor
```

Esto es un:

```text
SELF JOIN
```

---

# 🧠 Visualmente

```text
                 usuarios
                    │
        ┌───────────┴───────────┐
        │                       │
        ▼                       ▼
   usuarios u              usuarios s
      usuario                seguidor
```

Ambos alias representan la misma tabla:

```text
usuarios
```

pero cumplen funciones diferentes dentro de la consulta.

---

# 🗃️ Base de datos

La base de datos se llamará:

```text
esquema_seguidores
```

Tendrá dos tablas:

```text
usuarios
seguidores
```

---

# 📐 Estructura de `usuarios`

```text
usuarios
│
├── id              INT
├── nombre          VARCHAR(45)
├── apellido        VARCHAR(45)
├── email           VARCHAR(45)
├── created_at      DATETIME
└── updated_at      DATETIME
```

---

# 📐 Estructura de `seguidores`

```text
seguidores
│
├── id              INT
├── usuario_id      INT FK → usuarios.id
├── seguidor_id     INT FK → usuarios.id
├── created_at      DATETIME
└── updated_at      DATETIME
```

Para impedir relaciones duplicadas utilizaremos:

```text
UNIQUE(usuario_id, seguidor_id)
```

---

# 📁 Estructura final del proyecto

```text
seguidores_app/
│
├── flask_app/
│   │
│   ├── __init__.py
│   │
│   ├── bd/
│   │   └── esquema_seguidores.sql
│   │
│   ├── config/
│   │   └── mysqlconnection.py
│   │
│   ├── controllers/
│   │   └── usuarios.py
│   │
│   ├── models/
│   │   ├── usuario.py
│   │   └── seguidor.py
│   │
│   ├── templates/
│   │   └── usuarios.html
│   │
│   └── static/
│       └── css/
│           └── style.css
│
├── resources/
│   └── esquema_seguidores_erd.mwb
│
├── Pipfile
├── Pipfile.lock
├── .gitignore
└── server.py
```

> La carpeta `resources/` debe contener siempre el **ERD utilizado para crear la base de datos**.

---

# 🐍 Pipenv

Instalar las dependencias:

```bash
pipenv install flask pymysql
```

Activar el entorno:

```bash
pipenv shell
```

Ejecutar:

```bash
pipenv run python server.py
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

## `flask_app/bd/esquema_seguidores.sql`

```sql
-- ==========================================================
-- CREAR BASE DE DATOS
-- ==========================================================

CREATE DATABASE IF NOT EXISTS esquema_seguidores;

USE esquema_seguidores;


-- ==========================================================
-- TABLA USUARIOS
-- ==========================================================

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(45) NOT NULL,
    apellido VARCHAR(45) NOT NULL,
    email VARCHAR(45) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);


-- ==========================================================
-- TABLA SEGUIDORES
-- ==========================================================

CREATE TABLE IF NOT EXISTS seguidores (
    id INT AUTO_INCREMENT PRIMARY KEY,

    usuario_id INT NOT NULL,

    seguidor_id INT NOT NULL,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_seguidores_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id),

    CONSTRAINT fk_seguidores_seguidor
        FOREIGN KEY (seguidor_id)
        REFERENCES usuarios(id),

    CONSTRAINT uq_usuario_seguidor
        UNIQUE (usuario_id, seguidor_id)
);


-- ==========================================================
-- USUARIOS DE PRUEBA
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
    "Luis F.",
    "de la Vega",
    "luis@email.com"
),
(
    "Beatriz",
    "Pinzón",
    "beatriz@email.com"
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
    "Roberto",
    "Pardo",
    "roberto@email.com"
);


-- ==========================================================
-- RELACIONES DE PRUEBA
-- usuario_id = usuario seguido
-- seguidor_id = usuario que sigue
-- ==========================================================

INSERT INTO seguidores
(
    usuario_id,
    seguidor_id
)
VALUES
(
    1,
    2
),
(
    1,
    4
),
(
    3,
    2
),
(
    5,
    2
),
(
    2,
    3
);
```

---

# 🔍 Comprobar la estructura

```sql
USE esquema_seguidores;

DESCRIBE usuarios;
```

```sql
DESCRIBE seguidores;
```

---

# 🔎 Ver registros

```sql
SELECT *
FROM usuarios;
```

```sql
SELECT *
FROM seguidores;
```

---

# 🧪 Comprender los datos de prueba

Tenemos:

```text
1 → Soraya Montenegro
2 → Luis F. de la Vega
3 → Beatriz Pinzón
4 → Armando Mendoza
5 → Mia Colucci
6 → Roberto Pardo
```

Y:

```text
usuario_id | seguidor_id
-----------|------------
1          | 2
1          | 4
3          | 2
5          | 2
2          | 3
```

Según nuestra convención:

```text
2 sigue a 1
4 sigue a 1
2 sigue a 3
2 sigue a 5
3 sigue a 2
```

Por ejemplo:

```text
Luis F. de la Vega
        ↓
      sigue
        ↓
Soraya Montenegro
```

---

# 🔍 Consulta SELF JOIN

Esta es una de las consultas más importantes de la actividad:

```sql
SELECT
    u.id AS usuario_id,
    CONCAT(u.nombre, " ", u.apellido) AS usuario_nombre,

    s.id AS seguidor_id,
    CONCAT(s.nombre, " ", s.apellido) AS seguidor_nombre

FROM seguidores f

INNER JOIN usuarios u
    ON f.usuario_id = u.id

INNER JOIN usuarios s
    ON f.seguidor_id = s.id

ORDER BY u.nombre, s.nombre;
```

---

# 🧠 Analizando el SELF JOIN

Tenemos:

```sql
INNER JOIN usuarios u
```

Aquí:

```text
u
```

representa al usuario seguido.

Después:

```sql
INNER JOIN usuarios s
```

Aquí:

```text
s
```

representa al seguidor.

Aunque ambos provienen de:

```text
usuarios
```

los usamos con roles diferentes.

---

# 📊 Resultado esperado

La consulta puede producir:

```text
Usuario                 Seguidor
------------------------------------------------
Beatriz Pinzón          Luis F. de la Vega
Luis F. de la Vega      Beatriz Pinzón
Mia Colucci             Luis F. de la Vega
Soraya Montenegro       Armando Mendoza
Soraya Montenegro       Luis F. de la Vega
```

---

# ⚙️ Inicialización Flask

## `flask_app/__init__.py`

```python
from flask import Flask

app = Flask(__name__)

app.secret_key = "clave-secreta-desarrollo"
```

---

# 🔌 Configuración

## `flask_app/config/__init__.py`

```python
# Paquete de configuración de la aplicación.
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

        Si ocurre un error:
            devuelve False.
        """

        with self.connection.cursor() as cursor:
            try:
                cursor.execute(query, data)

                query_type = query.strip().lower()

                if query_type.startswith("select"):
                    return cursor.fetchall()

                if query_type.startswith("insert"):
                    return cursor.lastrowid

                return cursor.rowcount

            except Exception as e:
                print("Something went wrong:", e)
                return False

            finally:
                self.connection.close()


def connectToMySQL(db):
    """
    Crea y devuelve una conexión con MySQL.
    """

    return MySQLConnection(db)
```

> Cambia `user` y `password` según tu instalación local.

---

# 👤 Modelo Usuario

## `flask_app/models/__init__.py`

```python
# Paquete de modelos.
```

## `flask_app/models/usuario.py`

```python
from flask_app.config.mysqlconnection import connectToMySQL


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
            ORDER BY nombre, apellido;
        """

        resultados = connectToMySQL(
            "esquema_seguidores"
        ).query_db(query)

        usuarios = []

        for usuario in resultados:
            usuarios.append(
                cls(usuario)
            )

        return usuarios

    @classmethod
    def get_by_id(cls, id):
        """
        Obtiene un usuario específico mediante su ID.
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

        resultado = connectToMySQL(
            "esquema_seguidores"
        ).query_db(
            query,
            data
        )

        if resultado:
            return cls(resultado[0])

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
            "esquema_seguidores"
        ).query_db(
            query,
            data
        )
```

---

# 👥 Modelo Seguidor

## `flask_app/models/seguidor.py`

```python
from flask_app.config.mysqlconnection import connectToMySQL


class Seguidor:
    """
    Representa una relación entre dos usuarios.
    """

    @classmethod
    def get_all(cls):
        """
        Obtiene todas las relaciones utilizando SELF JOIN.

        u = usuario seguido
        s = seguidor
        """

        query = """
            SELECT
                u.id AS usuario_id,
                CONCAT(
                    u.nombre,
                    " ",
                    u.apellido
                ) AS usuario_nombre,

                s.id AS seguidor_id,
                CONCAT(
                    s.nombre,
                    " ",
                    s.apellido
                ) AS seguidor_nombre

            FROM seguidores f

            INNER JOIN usuarios u
                ON f.usuario_id = u.id

            INNER JOIN usuarios s
                ON f.seguidor_id = s.id

            ORDER BY
                u.nombre,
                u.apellido,
                s.nombre,
                s.apellido;
        """

        return connectToMySQL(
            "esquema_seguidores"
        ).query_db(query)


    @classmethod
    def existe(cls, data):
        """
        Comprueba si ya existe una relación.
        """

        query = """
            SELECT
                id
            FROM seguidores
            WHERE usuario_id = %(usuario_id)s
              AND seguidor_id = %(seguidor_id)s;
        """

        resultado = connectToMySQL(
            "esquema_seguidores"
        ).query_db(
            query,
            data
        )

        return bool(resultado)


    @classmethod
    def seguir(cls, data):
        """
        Crea una relación de seguimiento.
        """

        query = """
            INSERT INTO seguidores
            (
                usuario_id,
                seguidor_id
            )
            VALUES
            (
                %(usuario_id)s,
                %(seguidor_id)s
            );
        """

        return connectToMySQL(
            "esquema_seguidores"
        ).query_db(
            query,
            data
        )
```

---

# 🎮 Controlador

## `flask_app/controllers/__init__.py`

```python
# Paquete de controladores.
```

---

# 📄 `flask_app/controllers/usuarios.py`

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
from flask_app.models.seguidor import Seguidor


# ==========================================================
# INICIO
# ==========================================================

@app.route("/")
def inicio():
    """
    Redirige la página principal hacia /usuarios.
    """

    return redirect(
        url_for("usuarios")
    )


# ==========================================================
# USUARIOS
# ==========================================================

@app.route("/usuarios")
def usuarios():
    """
    Obtiene todos los usuarios y todas las relaciones.
    """

    lista_usuarios = Usuario.get_all()

    relaciones = Seguidor.get_all()

    return render_template(
        "usuarios.html",
        usuarios=lista_usuarios,
        relaciones=relaciones
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
    Recibe los datos del formulario y crea un usuario.
    """

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


    if not nombre or not apellido or not email:

        flash(
            "Todos los campos son obligatorios.",
            "danger"
        )

        return redirect(
            url_for("usuarios")
        )


    data = {
        "nombre": nombre,
        "apellido": apellido,
        "email": email
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
# CREAR RELACIÓN
# ==========================================================

@app.route(
    "/seguir",
    methods=["POST"]
)
def seguir():
    """
    Registra que un usuario sigue a otro.

    usuario_id:
        usuario que está siendo seguido.

    seguidor_id:
        usuario que lo sigue.
    """

    usuario_id_texto = request.form.get(
        "usuario_id"
    )

    seguidor_id_texto = request.form.get(
        "seguidor_id"
    )


    if not usuario_id_texto or not seguidor_id_texto:

        flash(
            "Debes seleccionar un usuario y un seguidor.",
            "danger"
        )

        return redirect(
            url_for("usuarios")
        )


    try:

        usuario_id = int(
            usuario_id_texto
        )

        seguidor_id = int(
            seguidor_id_texto
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
    # Comprobar que el seguidor exista.
    # ------------------------------------------------------

    seguidor = Usuario.get_by_id(
        seguidor_id
    )


    if seguidor is None:

        flash(
            "El seguidor seleccionado no existe.",
            "danger"
        )

        return redirect(
            url_for("usuarios")
        )


    # ------------------------------------------------------
    # Crear diccionario de datos.
    # ------------------------------------------------------

    data = {
        "usuario_id": usuario_id,
        "seguidor_id": seguidor_id
    }


    # ------------------------------------------------------
    # Comprobar relación duplicada.
    # ------------------------------------------------------

    if Seguidor.existe(data):

        flash(
            "Esta relación ya existe.",
            "warning"
        )

        return redirect(
            url_for("usuarios")
        )


    # ------------------------------------------------------
    # Insertar relación.
    # ------------------------------------------------------

    resultado = Seguidor.seguir(
        data
    )


    if resultado is False:

        flash(
            "No fue posible registrar la relación.",
            "danger"
        )

        return redirect(
            url_for("usuarios")
        )


    flash(
        "Relación registrada correctamente.",
        "success"
    )


    return redirect(
        url_for("usuarios")
    )
```

---

# 🌐 Vista principal

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
        Seguidores
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


    <!-- ==================================================
         ENCABEZADO
    =================================================== -->

    <div class="text-center mb-5">

        <h1>
            Seguidores
        </h1>

        <p class="text-muted">
            Gestiona usuarios y sus relaciones de seguimiento.
        </p>

    </div>


    <!-- ==================================================
         MENSAJES
    =================================================== -->

    {% with mensajes = get_flashed_messages(
        with_categories=true
    ) %}

        {% if mensajes %}

            {% for categoria, mensaje in mensajes %}

                <div class="alert alert-{{ categoria }}">

                    {{ mensaje }}

                </div>

            {% endfor %}

        {% endif %}

    {% endwith %}


    <!-- ==================================================
         RELACIONES
    =================================================== -->

    <div class="card shadow-sm border-0 mb-5">

        <div class="card-body p-4">

            <h2 class="h3 mb-4">
                Seguidores
            </h2>


            {% if relaciones %}

                <div class="table-responsive">

                    <table class="table table-striped table-hover">

                        <thead class="table-dark">

                            <tr>

                                <th>
                                    Usuario
                                </th>

                                <th>
                                    Seguidor
                                </th>

                            </tr>

                        </thead>


                        <tbody>

                            {% for relacion in relaciones %}

                                <tr>

                                    <td>
                                        {{ relacion["usuario_nombre"] }}
                                    </td>

                                    <td>
                                        {{ relacion["seguidor_nombre"] }}
                                    </td>

                                </tr>

                            {% endfor %}

                        </tbody>

                    </table>

                </div>

            {% else %}

                <div class="alert alert-info mb-0">

                    Todavía no existen relaciones registradas.

                </div>

            {% endif %}

        </div>

    </div>


    <div class="row g-4">


        <!-- ==================================================
             NUEVO USUARIO
        =================================================== -->

        <div class="col-lg-6">

            <div class="card shadow-sm border-0 h-100">

                <div class="card-body p-4">

                    <h2 class="h3 mb-4">
                        Nuevo Usuario
                    </h2>


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
                                maxlength="45"
                                required
                            >

                        </div>


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
             SEGUIR
        =================================================== -->

        <div class="col-lg-6">

            <div class="card shadow-sm border-0 h-100">

                <div class="card-body p-4">

                    <h2 class="h3 mb-4">
                        Seguir
                    </h2>


                    <form
                        action="{{ url_for('seguir') }}"
                        method="POST"
                    >


                        <!-- USUARIO -->

                        <div class="mb-3">

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
                                        value="{{ usuario.id }}"
                                    >

                                        {{ usuario.nombre }}
                                        {{ usuario.apellido }}

                                    </option>

                                {% endfor %}

                            </select>

                        </div>


                        <!-- SEGUIDOR -->

                        <div class="mb-4">

                            <label
                                for="seguidor_id"
                                class="form-label"
                            >

                                Seguidor

                            </label>


                            <select
                                id="seguidor_id"
                                name="seguidor_id"
                                class="form-select"
                                required
                            >

                                <option value="">

                                    Selecciona un seguidor

                                </option>


                                {% for usuario in usuarios %}

                                    <option
                                        value="{{ usuario.id }}"
                                    >

                                        {{ usuario.nombre }}
                                        {{ usuario.apellido }}

                                    </option>

                                {% endfor %}

                            </select>

                        </div>


                        <button
                            type="submit"
                            class="btn btn-success"
                        >

                            Seguir

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

# 🎨 Hoja de estilos

## `flask_app/static/css/style.css`

```css
body {
    background-color: #f5f6f8;
    color: #212529;
    font-family: Arial, Helvetica, sans-serif;
}

h1,
h2 {
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

# 🔄 Flujo para crear un usuario

El formulario:

```text
Nuevo Usuario
```

envía:

```text
POST /usuarios/crear
```

El flujo es:

```text
usuarios.html
      ↓
formulario
      ↓
POST
      ↓
request.form
      ↓
data
      ↓
Usuario.save()
      ↓
INSERT
      ↓
MySQL
      ↓
redirect()
      ↓
/usuarios
```

---

# 🔄 Flujo para crear una relación

El usuario selecciona:

```text
Usuario:
Soraya Montenegro
```

y:

```text
Seguidor:
Luis F. de la Vega
```

El formulario envía:

```text
usuario_id = 1
seguidor_id = 2
```

El flujo es:

```text
Formulario
      ↓
POST /seguir
      ↓
request.form
      ↓
usuario_id
seguidor_id
      ↓
validar usuarios
      ↓
Seguidor.existe()
      ↓
Seguidor.seguir()
      ↓
INSERT
      ↓
seguidores
      ↓
redirect()
      ↓
/usuarios
```

---

# 🔍 ¿Qué se almacena realmente?

Cuando seleccionamos:

```text
Usuario:
Soraya Montenegro
```

y:

```text
Seguidor:
Luis F. de la Vega
```

no guardamos los nombres.

Guardamos:

```text
usuario_id = 1
seguidor_id = 2
```

La tabla queda:

```text
usuario_id | seguidor_id
-----------|------------
1          | 2
```

Esto permite que MySQL mantenga la relación mediante IDs.

---

# 🧠 ¿Por qué usamos IDs y no nombres?

Los nombres pueden repetirse.

Por ejemplo:

```text
Juan Pérez
Juan Pérez
```

El `id` permite identificar un registro de forma única.

Por eso la relación utiliza:

```text
usuario_id
seguidor_id
```

y no:

```text
usuario_nombre
seguidor_nombre
```

---

# 🔍 Self Join explicado paso a paso

Tenemos:

```text
seguidores
```

con:

```text
usuario_id
seguidor_id
```

Supongamos:

```text
1 | 2
```

La consulta necesita encontrar:

```text
usuarios.id = 1
```

para obtener:

```text
Soraya
```

y también:

```text
usuarios.id = 2
```

para obtener:

```text
Luis
```

Por eso utilizamos dos alias:

```sql
usuarios u
usuarios s
```

Tenemos:

```text
u.id = usuario_id
```

y:

```text
s.id = seguidor_id
```

---

# 🧠 Visualización del SELF JOIN

```text
seguidores

usuario_id = 1
seguidor_id = 2

        ↓

usuarios u
id = 1
Soraya Montenegro

        +

usuarios s
id = 2
Luis F. de la Vega

        ↓

Resultado

Soraya Montenegro | Luis F. de la Vega
```

---

# 🧩 ¿Por qué dos `<select>`?

Porque necesitamos representar dos roles diferentes.

```text
<select name="usuario_id">
```

representa:

```text
Usuario
```

Mientras:

```text
<select name="seguidor_id">
```

representa:

```text
Seguidor
```

Ambos utilizan la misma lista:

```text
usuarios
```

pero representan funciones diferentes.

---

# 🔄 Flujo de los `<select>`

El usuario ve:

```text
Soraya Montenegro
```

pero el HTML contiene:

```html
<option value="1">
    Soraya Montenegro
</option>
```

Por lo tanto:

```text
Usuario visualiza:
Soraya Montenegro

Flask recibe:
usuario_id = 1
```

Lo mismo ocurre con el segundo select:

```text
Luis F. de la Vega
```

Flask recibe:

```text
seguidor_id = 2
```

---

# 🔐 BONUS — Evitar duplicados

Supongamos que ya tenemos:

```text
usuario_id = 1
seguidor_id = 2
```

Si intentamos registrar nuevamente:

```text
usuario_id = 1
seguidor_id = 2
```

la aplicación ejecuta:

```python
Seguidor.existe(data)
```

y comprueba si la relación ya existe.

Si existe:

```text
Esta relación ya existe.
```

No se realiza otro `INSERT`.

Además, la base de datos posee:

```sql
UNIQUE (
    usuario_id,
    seguidor_id
)
```

por lo que MySQL también evita duplicaciones.

---

# 🛡️ Protección en dos niveles

Tenemos:

```text
CONTROLADOR
    ↓
Seguidor.existe()
```

y:

```text
BASE DE DATOS
    ↓
UNIQUE(usuario_id, seguidor_id)
```

Esto permite que tanto la aplicación como la base de datos colaboren en la integridad de la relación.

---

# 🧪 Prueba funcional

## 1. Ejecutar

```bash
pipenv run python server.py
```

---

## 2. Abrir

```text
http://127.0.0.1:5000/usuarios
```

---

## 3. Crear un usuario

Completar:

```text
Nombre:
Pedro

Apellido:
Pérez

E-mail:
pedro@email.com
```

Presionar:

```text
Crear
```

El usuario debe aparecer dentro de la base de datos.

---

## 4. Crear una relación

Seleccionar:

```text
Usuario:
Soraya Montenegro
```

y:

```text
Seguidor:
Pedro Pérez
```

Presionar:

```text
Seguir
```

Debe aparecer:

```text
Usuario                  Seguidor
-----------------------------------------------
Soraya Montenegro        Pedro Pérez
```

---

# 🧪 Probar varias relaciones

Crear:

```text
Soraya ← Luis
Soraya ← Armando
Beatriz ← Luis
Mia ← Luis
Luis ← Beatriz
```

La tabla debería mostrar relaciones equivalentes a:

```text
Usuario              Seguidor

Soraya Montenegro    Luis F. de la Vega
Soraya Montenegro    Armando Mendoza
Beatriz Pinzón       Luis F. de la Vega
Mia Colucci          Luis F. de la Vega
Luis F. de la Vega   Beatriz Pinzón
```

---

# 🧪 Probar el BONUS

Intentar nuevamente:

```text
Usuario:
Soraya Montenegro

Seguidor:
Luis F. de la Vega
```

La aplicación debe responder:

```text
Esta relación ya existe.
```

y no agregar otra fila.

---

# 🔎 Comprobar en MySQL

```sql
USE esquema_seguidores;

SELECT *
FROM seguidores;
```

También podemos consultar la relación completa:

```sql
SELECT
    u.nombre AS usuario,
    u.apellido AS apellido_usuario,
    s.nombre AS seguidor,
    s.apellido AS apellido_seguidor
FROM seguidores f
INNER JOIN usuarios u
    ON f.usuario_id = u.id
INNER JOIN usuarios s
    ON f.seguidor_id = s.id;
```

---

# 📊 Diferencia entre las tablas

| Tabla | Responsabilidad |
|---|---|
| `usuarios` | Almacena las entidades |
| `seguidores` | Almacena las relaciones |
| `usuario_id` | Identifica al usuario seguido |
| `seguidor_id` | Identifica al usuario que sigue |
| `usuarios u` | Rol usuario en el `SELF JOIN` |
| `usuarios s` | Rol seguidor en el `SELF JOIN` |

---

# 🧠 Diferencia con relaciones anteriores

## Relación 1:N

Ejemplo:

```text
Curso
  ↓
Estudiantes
```

Son entidades diferentes.

---

## N:N entre entidades diferentes

Ejemplo:

```text
Usuarios
   ↕
Favoritos
   ↕
Canciones
```

Tenemos:

```text
Usuario
```

y:

```text
Canción
```

como entidades diferentes.

---

## Auto-relación

Aquí tenemos:

```text
Usuarios
   ↕
Seguidores
   ↕
Usuarios
```

La misma entidad aparece en ambos lados.

Ese es el punto central:

```text
USUARIO N : N USUARIO
```

---

# 🧠 Modelo mental

Al observar:

```text
usuarios
    ↕
seguidores
    ↕
usuarios
```

debemos pensar:

```text
SELF RELATION
```

y al escribir:

```sql
usuarios u
JOIN usuarios s
```

debemos pensar:

```text
u = usuario

s = seguidor
```

---

# 🔄 Flujo completo de la aplicación

```text
                    NAVEGADOR
                        │
                        ▼
                  /usuarios
                        │
                        ▼
                 usuarios.html
                        │
          ┌─────────────┴─────────────┐
          │                           │
          ▼                           ▼
     Nuevo Usuario                  Seguir
          │                           │
          ▼                           ▼
      POST crear                  POST seguir
          │                           │
          ▼                           ▼
      Usuario.save()          Seguidor.existe()
          │                           │
          ▼                           ▼
        MySQL                Seguidor.seguir()
                                      │
                                      ▼
                                    MySQL
                                      │
                                      ▼
                                  redirect()
                                      │
                                      ▼
                                  /usuarios
```

---

# 🧩 Arquitectura MVC

```text
flask_app/
│
├── config/
│   └── mysqlconnection.py
│       → conexión MySQL
│
├── models/
│   ├── usuario.py
│   │   → usuarios
│   │
│   └── seguidor.py
│       → relaciones
│
├── controllers/
│   └── usuarios.py
│       → rutas y coordinación
│
├── templates/
│   └── usuarios.html
│       → interfaz
│
└── __init__.py
    → inicialización Flask
```

---

# 🧪 Consultas de comprobación

## Todos los usuarios

```sql
SELECT
    id,
    nombre,
    apellido,
    email
FROM usuarios;
```

## Todas las relaciones

```sql
SELECT
    usuario_id,
    seguidor_id
FROM seguidores;
```

## Relaciones con nombres

```sql
SELECT
    CONCAT(
        u.nombre,
        " ",
        u.apellido
    ) AS usuario,

    CONCAT(
        s.nombre,
        " ",
        s.apellido
    ) AS seguidor

FROM seguidores f

INNER JOIN usuarios u
    ON f.usuario_id = u.id

INNER JOIN usuarios s
    ON f.seguidor_id = s.id;
```

---

# 🧠 Consideración opcional: auto-seguimiento

La actividad original no exige impedir:

```text
usuario_id == seguidor_id
```

Por ejemplo:

```text
1 → 1
```

podría representar que un usuario se sigue a sí mismo.

Como mejora opcional se podría validar:

```python
if usuario_id == seguidor_id:
```

y mostrar:

```text
Un usuario no puede seguirse a sí mismo.
```

No es requisito obligatorio de esta actividad.

---

# ⚠️ Errores comunes

## `FOREIGN KEY` incorrecta

Las dos claves foráneas deben apuntar a:

```text
usuarios.id
```

No deben apuntar a tablas diferentes.

---

## Confundir los IDs

Debe existir:

```text
usuario_id
```

y:

```text
seguidor_id
```

No:

```text
usuario
seguidor
```

---

## `<select>` sin `name`

Debe existir:

```html
<select name="usuario_id">
```

y:

```html
<select name="seguidor_id">
```

---

## Enviar nombres en lugar de IDs

No hacer:

```text
usuario_nombre = "Soraya"
```

La relación debe almacenar:

```text
usuario_id = 1
```

---

## No utilizar alias en el SELF JOIN

Incorrecto conceptualmente:

```sql
JOIN usuarios
JOIN usuarios
```

Es mucho más claro:

```sql
JOIN usuarios u
JOIN usuarios s
```

---

## No validar duplicados

Una relación:

```text
(1,2)
```

no debería aparecer dos veces.

---

## `BuildError`

Revisa que el nombre utilizado en:

```jinja
url_for("usuarios")
```

coincida con:

```python
def usuarios():
```

---

# ✅ Checklist

```text
[ ] Pipenv configurado
[ ] Flask instalado
[ ] PyMySQL instalado
[ ] Pipfile creado
[ ] Pipfile.lock generado

[ ] Base de datos creada
[ ] Tabla usuarios creada
[ ] Tabla seguidores creada
[ ] FOREIGN KEY usuario creada
[ ] FOREIGN KEY seguidor creada
[ ] UNIQUE(usuario_id, seguidor_id) creada

[ ] Datos de prueba insertados
[ ] ERD guardado en resources/

[ ] flask_app creado
[ ] __init__.py creado
[ ] config creado
[ ] mysqlconnection.py funciona
[ ] controllers creado
[ ] usuarios.py funciona
[ ] models creado
[ ] usuario.py funciona
[ ] seguidor.py funciona

[ ] / funciona
[ ] /usuarios funciona
[ ] Crear usuario funciona
[ ] Formulario Seguir funciona
[ ] Select Usuario funciona
[ ] Select Seguidor funciona
[ ] request.form funciona
[ ] POST funciona
[ ] SELF JOIN funciona
[ ] Relaciones aparecen en la tabla
[ ] redirect() funciona
[ ] url_for() funciona
[ ] Sentencias preparadas funcionan

[ ] BONUS: duplicados controlados
```

---

# 🏁 Resultado esperado

La aplicación debe terminar mostrando una interfaz equivalente a:

```text
┌──────────────────────────────────────────────────────────┐
│                      Seguidores                          │
├────────────────────────────┬─────────────────────────────┤
│ Usuario                    │ Seguidor                    │
├────────────────────────────┼─────────────────────────────┤
│ Soraya Montenegro          │ Luis F. de la Vega          │
│ Beatriz Pinzón             │ Armando Mendoza             │
│ Mia Colucci                │ Luis F. de la Vega          │
│ Luis F. de la Vega         │ Beatriz Pinzón              │
└────────────────────────────┴─────────────────────────────┘


┌──────────────────────────┐  ┌──────────────────────────┐
│      Nuevo Usuario       │  │         Seguir            │
│                          │  │                          │
│ Nombre:                  │  │ Usuario:                 │
│ [______________]        │  │ [ Soraya Montenegro ▼ ] │
│                          │  │                          │
│ Apellido:                │  │ Seguidor:                │
│ [______________]        │  │ [ Luis F. ▼ ]           │
│                          │  │                          │
│ E-mail:                  │  │ [ Seguir ]               │
│ [______________]        │  │                          │
│                          │  │                          │
│ [ Crear ]                │  │                          │
└──────────────────────────┘  └──────────────────────────┘
```

---

# 🧠 Concepto central de la actividad

La idea fundamental que debe quedar comprendida es:

```text
USUARIO
    │
    │ usuario_id
    ▼
SEGUIDORES
    ▲
    │ seguidor_id
    │
USUARIO
```

Una misma tabla:

```text
usuarios
```

aparece dos veces en la consulta:

```sql
usuarios u
```

y:

```sql
usuarios s
```

porque estamos utilizando dos roles diferentes:

```text
u → usuario
s → seguidor
```

Por eso hablamos de:

```text
SELF JOIN
```

---

# 📚 Resumen final

```text
usuario_id
    ↓
identifica al usuario seguido

seguidor_id
    ↓
identifica al usuario que sigue

        ↓

seguidores

        ↓

SELF JOIN

        ↓

usuarios u
usuarios s

        ↓

Usuario + Seguidor

        ↓

Jinja2

        ↓

HTML
```

La aplicación permite representar:

```text
Luis F. de la Vega
        ↓
      sigue
        ↓
Soraya Montenegro
```

y también:

```text
Soraya Montenegro
        ↓
es seguida por
        ↓
Luis F. de la Vega
```

La tabla `seguidores` es la que almacena la relación, mientras que `usuarios` contiene las entidades relacionadas.

---

# 📦 Entregables

## GitHub

Entregar el enlace al repositorio completo:

```text
seguidores_app/
```

Debe incluir:

```text
flask_app/
resources/
Pipfile
Pipfile.lock
server.py
```

## Evidencia

Entregar una imagen de la aplicación funcionando donde se pueda observar:

```text
Seguidores
+
Nuevo Usuario
+
Seguir
```

y algunas relaciones registradas.

## ERD

Debe existir obligatoriamente:

```text
resources/
└── esquema_seguidores_erd.mwb
```

---

# 🎓 Resultado pedagógico

Al finalizar esta práctica debes poder responder:

### ¿Qué es un Self Join?

Una consulta que utiliza una misma tabla más de una vez, utilizando alias para representar roles diferentes dentro de una relación.

### ¿Por qué `seguidores` tiene dos FK hacia `usuarios`?

Porque ambas partes de la relación corresponden a registros de la misma entidad:

```text
usuario
seguidor
```

### ¿Qué guarda realmente `seguidores`?

No guarda nombres.

Guarda:

```text
usuario_id
seguidor_id
```

es decir, la relación entre dos usuarios.

### ¿Qué convierte esta estructura en una auto-relación?

Que:

```text
usuario_id
```

y:

```text
seguidor_id
```

referencian la misma tabla:

```text
usuarios
```

---

# 🏆 Flujo de aprendizaje

```text
RELACIÓN
   ↓
AUTO-RELACIÓN
   ↓
TABLA INTERMEDIA
   ↓
DOS FOREIGN KEY
   ↓
SELF JOIN
   ↓
ALIAS
   ↓
RESULTADO SQL
   ↓
PYTHON / MVC
   ↓
JINJA2
   ↓
HTML
```

La aplicación final demuestra cómo representar una relación:

```text
USUARIO N : N USUARIO
```

mediante una tabla intermedia y una consulta `SELF JOIN`.
Mostrando README.md