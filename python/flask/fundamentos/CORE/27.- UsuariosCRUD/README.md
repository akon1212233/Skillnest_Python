# 👥 Usuarios CRUD — Modularización MVC

## Descripción

Esta actividad corresponde a la **modularización de la asignación anterior Usuarios CRUD**. El objetivo es reorganizar una aplicación Flask CRUD ya funcional para implementar una arquitectura **MVC**, separando configuración, modelos, controladores y vistas, manteniendo las operaciones de **Create, Read, Update y Delete**.

El resultado final debe ser una aplicación Flask funcional, organizada y ejecutable mediante **Pipenv**.

---

## Objetivo

Implementar la arquitectura:

```text
MODEL
VIEW
CONTROLLER
```

manteniendo el CRUD de usuarios:

```text
CREATE → Crear usuario
READ   → Listar y visualizar usuario
UPDATE → Editar usuario
DELETE → Eliminar usuario
```

---

# 🗄️ Base de datos

## Estructura

La aplicación utilizará:

```text
Base de datos: esquema_usuarios
Tabla: usuarios
```

La tabla contiene:

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

## `flask_app/bd/esquema_usuarios.sql`

```sql
CREATE DATABASE IF NOT EXISTS esquema_usuarios;

USE esquema_usuarios;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(45) NOT NULL,
    apellido VARCHAR(45) NOT NULL,
    email VARCHAR(45) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

INSERT INTO usuarios (nombre, apellido, email) VALUES
("Ricky", "Martin", "ricky@codingdojo.com"),
("Enrique", "Iglesias", "enrique@codingdojo.com"),
("Celia", "Cruz", "celia@codingdojo.com"),
("Ricardo", "Montaner", "ricardo@codingdojo.com");
```

---

# 📁 Estructura final del proyecto

```text
USUARIOS_CRUD_MVC/
│
├── flask_app/
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
│   │   ├── index.html
│   │   ├── nuevo.html
│   │   ├── detalle.html
│   │   └── editar.html
│   │
│   ├── static/
│   │   └── css/
│   │       └── style.css
│   │
│   └── __init__.py
│
├── resources/
│   └── esquema_usuarios.mwb
│
├── Pipfile
├── Pipfile.lock
└── server.py
```

> La carpeta `resources/` es obligatoria y debe contener el **ERD utilizado para construir la base de datos**.

---

# 🐍 Pipenv

Crear el entorno:

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

Al utilizar Pipenv se generarán:

```text
Pipfile
Pipfile.lock
```

`Pipfile.lock` debe ser generado por Pipenv y no escrito manualmente.

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

app.secret_key = "clave-secreta-desarrollo"
```

---

# 🔌 `flask_app/config/mysqlconnection.py`

```python
import pymysql.cursors

class MySQLConnection:
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
    return MySQLConnection(db)
```

> Configura `user` y `password` según tu instalación local de MySQL.

---

# 👤 `flask_app/models/usuario.py`

```python
from flask_app.config.mysqlconnection import connectToMySQL

class Usuario:
    def __init__(self, data):
        self.id = data["id"]
        self.nombre = data["nombre"]
        self.apellido = data["apellido"]
        self.email = data["email"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def get_all(cls):
        query = """
            SELECT id, nombre, apellido, email, created_at, updated_at
            FROM usuarios
            ORDER BY id;
        """

        resultados = connectToMySQL("esquema_usuarios").query_db(query)

        usuarios = []

        for usuario in resultados:
            usuarios.append(cls(usuario))

        return usuarios

    @classmethod
    def get_by_id(cls, id):
        query = """
            SELECT id, nombre, apellido, email, created_at, updated_at
            FROM usuarios
            WHERE id = %(id)s;
        """

        data = {
            "id": id
        }

        resultados = connectToMySQL("esquema_usuarios").query_db(query, data)

        if resultados:
            return cls(resultados[0])

        return None

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO usuarios
            (nombre, apellido, email, created_at, updated_at)
            VALUES
            (%(nombre)s, %(apellido)s, %(email)s, NOW(), NOW());
        """

        return connectToMySQL("esquema_usuarios").query_db(query, data)

    @classmethod
    def update(cls, data):
        query = """
            UPDATE usuarios
            SET
                nombre = %(nombre)s,
                apellido = %(apellido)s,
                email = %(email)s,
                updated_at = NOW()
            WHERE id = %(id)s;
        """

        return connectToMySQL("esquema_usuarios").query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = """
            DELETE FROM usuarios
            WHERE id = %(id)s;
        """

        return connectToMySQL("esquema_usuarios").query_db(query, data)
```

---

# 🎮 `flask_app/controllers/usuarios.py`

```python
from flask_app import app

from flask import render_template, request, redirect, url_for

from flask_app.models.usuario import Usuario


@app.route("/usuarios")
def usuarios():
    lista_usuarios = Usuario.get_all()

    return render_template(
        "index.html",
        usuarios=lista_usuarios
    )


@app.route("/usuarios/nuevo")
def nuevo():
    return render_template("nuevo.html")


@app.route("/usuarios/crear", methods=["POST"])
def crear():
    data = {
        "nombre": request.form["nombre"].strip(),
        "apellido": request.form["apellido"].strip(),
        "email": request.form["email"].strip()
    }

    if not data["nombre"] or not data["apellido"] or not data["email"]:
        return render_template(
            "nuevo.html",
            error="Todos los campos son obligatorios.",
            datos=data
        )

    resultado = Usuario.save(data)

    if resultado is False:
        return render_template(
            "nuevo.html",
            error="No fue posible crear el usuario.",
            datos=data
        )

    return redirect(url_for("usuarios"))


@app.route("/usuarios/<int:id>")
def detalle(id):
    usuario = Usuario.get_by_id(id)

    if usuario is None:
        return "Usuario no encontrado", 404

    return render_template(
        "detalle.html",
        usuario=usuario
    )


@app.route("/usuarios/editar/<int:id>")
def editar(id):
    usuario = Usuario.get_by_id(id)

    if usuario is None:
        return "Usuario no encontrado", 404

    return render_template(
        "editar.html",
        usuario=usuario
    )


@app.route("/usuarios/<int:id>/actualizar", methods=["POST"])
def actualizar(id):
    data = {
        "id": id,
        "nombre": request.form["nombre"].strip(),
        "apellido": request.form["apellido"].strip(),
        "email": request.form["email"].strip()
    }

    if not data["nombre"] or not data["apellido"] or not data["email"]:
        usuario = Usuario.get_by_id(id)

        return render_template(
            "editar.html",
            usuario=usuario,
            error="Todos los campos son obligatorios."
        )

    resultado = Usuario.update(data)

    if resultado is False:
        usuario = Usuario.get_by_id(id)

        return render_template(
            "editar.html",
            usuario=usuario,
            error="No fue posible actualizar el usuario."
        )

    return redirect(url_for("usuarios"))


@app.route("/usuarios/borrar/<int:id>")
def borrar(id):
    data = {
        "id": id
    }

    resultado = Usuario.delete(data)

    if resultado is False:
        return "No fue posible eliminar el usuario.", 500

    return redirect(url_for("usuarios"))
```

---

# 🌐 `server.py`

Este archivo será únicamente el punto de entrada de la aplicación.

```python
from flask_app import app

from flask_app.controllers import usuarios


if __name__ == "__main__":
    app.run(debug=True)
```

---

# 👁️ `flask_app/templates/index.html`

```html
<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Usuarios</title>

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
            <h1 class="mb-1">Usuarios</h1>
            <p class="text-muted mb-0">
                Usuarios registrados en el sistema.
            </p>
        </div>

        <a
            href="{{ url_for('nuevo') }}"
            class="btn btn-primary"
        >
            Nuevo Usuario
        </a>

    </div>


    <div class="card shadow-sm border-0">

        <div class="card-body p-0">

            {% if usuarios %}

                <div class="table-responsive">

                    <table class="table table-hover align-middle mb-0">

                        <thead class="table-dark">

                            <tr>
                                <th>Id</th>
                                <th>Nombre Completo</th>
                                <th>E-mail</th>
                                <th>Fecha Creación</th>
                                <th>Acciones</th>
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
                                        {{ usuario.apellido }}
                                    </td>

                                    <td>
                                        {{ usuario.email }}
                                    </td>

                                    <td>
                                        {% if usuario.created_at %}
                                            {{ usuario.created_at.strftime("%Y-%m-%d") }}
                                        {% endif %}
                                    </td>

                                    <td>

                                        <div class="acciones">

                                            <a
                                                href="{{ url_for('detalle', id=usuario.id) }}"
                                                class="btn btn-sm btn-outline-primary"
                                            >
                                                Ver
                                            </a>

                                            <a
                                                href="{{ url_for('editar', id=usuario.id) }}"
                                                class="btn btn-sm btn-outline-warning"
                                            >
                                                Editar
                                            </a>

                                            <a
                                                href="{{ url_for('borrar', id=usuario.id) }}"
                                                class="btn btn-sm btn-outline-danger"
                                                onclick="return confirm('¿Estás seguro de eliminar este usuario?');"
                                            >
                                                Borrar
                                            </a>

                                        </div>

                                    </td>

                                </tr>

                            {% endfor %}

                        </tbody>

                    </table>

                </div>

            {% else %}

                <div class="empty-state">

                    <h3>
                        No hay usuarios registrados.
                    </h3>

                    <p class="text-muted">
                        Crea el primer usuario.
                    </p>

                    <a
                        href="{{ url_for('nuevo') }}"
                        class="btn btn-primary"
                    >
                        Crear Usuario
                    </a>

                </div>

            {% endif %}

        </div>

    </div>

</div>

</body>

</html>
```

---

# 📝 `flask_app/templates/nuevo.html`

```html
<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Nuevo Usuario</title>

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

    <div class="form-card">

        <div class="mb-4">

            <h1>
                Crear nuevo usuario
            </h1>

            <p class="text-muted">
                Ingresa los datos del usuario.
            </p>

        </div>


        {% if error %}

            <div class="alert alert-danger">
                {{ error }}
            </div>

        {% endif %}


        <form
            action="{{ url_for('crear') }}"
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
                    value="{{ datos.nombre if datos else '' }}"
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
                    value="{{ datos.apellido if datos else '' }}"
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
                    value="{{ datos.email if datos else '' }}"
                    required
                >

            </div>


            <div class="d-flex gap-2">

                <button
                    type="submit"
                    class="btn btn-primary"
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

</body>

</html>
```

---

# 🔎 `flask_app/templates/detalle.html`

```html
<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>
        Usuario {{ usuario.id }}
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

    <div class="detail-card">

        <h1>
            Usuario {{ usuario.id }}
        </h1>

        <p class="text-muted">
            Información completa del usuario.
        </p>

        <hr>


        <div class="detail-info">

            <p>
                <strong>Nombre:</strong>
                {{ usuario.nombre }}
            </p>

            <p>
                <strong>Apellido:</strong>
                {{ usuario.apellido }}
            </p>

            <p>
                <strong>Nombre Completo:</strong>
                {{ usuario.nombre }} {{ usuario.apellido }}
            </p>

            <p>
                <strong>E-mail:</strong>
                {{ usuario.email }}
            </p>

            <p>
                <strong>Fecha Creación:</strong>
                {{ usuario.created_at }}
            </p>

            <p>
                <strong>Fecha Actualización:</strong>
                {{ usuario.updated_at }}
            </p>

        </div>


        <div class="d-flex gap-2 mt-4">

            <a
                href="{{ url_for('editar', id=usuario.id) }}"
                class="btn btn-warning"
            >
                Editar
            </a>

            <a
                href="{{ url_for('borrar', id=usuario.id) }}"
                class="btn btn-danger"
                onclick="return confirm('¿Estás seguro de eliminar este usuario?');"
            >
                Borrar
            </a>

            <a
                href="{{ url_for('usuarios') }}"
                class="btn btn-outline-secondary"
            >
                Volver
            </a>

        </div>

    </div>

</div>

</body>

</html>
```

---

# ✏️ `flask_app/templates/editar.html`

```html
<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>
        Editar Usuario {{ usuario.id }}
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

    <div class="form-card">

        <div class="mb-4">

            <h1>
                Editar Usuario {{ usuario.id }}
            </h1>

            <p class="text-muted">
                Modifica los datos del usuario.
            </p>

        </div>


        {% if error %}

            <div class="alert alert-danger">
                {{ error }}
            </div>

        {% endif %}


        <form
            action="{{ url_for('actualizar', id=usuario.id) }}"
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
                    value="{{ usuario.nombre }}"
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
                    value="{{ usuario.apellido }}"
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
                    value="{{ usuario.email }}"
                    required
                >

            </div>


            <div class="d-flex gap-2">

                <button
                    type="submit"
                    class="btn btn-success"
                >
                    Actualizar
                </button>

                <a
                    href="{{ url_for('detalle', id=usuario.id) }}"
                    class="btn btn-outline-secondary"
                >
                    Cancelar
                </a>

            </div>

        </form>

    </div>

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

h1 {
    font-weight: 700;
}

.card,
.form-card,
.detail-card {
    border-radius: 10px;
}

.form-card,
.detail-card {
    max-width: 700px;
    margin: 0 auto;
    padding: 35px;
    background-color: #ffffff;
    box-shadow: 0 4px 18px rgba(0, 0, 0, 0.08);
}

.table {
    vertical-align: middle;
}

.table th {
    white-space: nowrap;
}

.table td {
    padding-top: 14px;
    padding-bottom: 14px;
}

.acciones {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
}

.detail-info {
    padding: 25px;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    background-color: #fafafa;
}

.detail-info p {
    margin-bottom: 15px;
}

.empty-state {
    padding: 60px 30px;
    text-align: center;
}

.form-control {
    border-radius: 6px;
}

.btn {
    border-radius: 6px;
}

@media (max-width: 768px) {
    .acciones {
        flex-direction: column;
    }

    .acciones .btn {
        width: 100%;
    }
}

@media (max-width: 576px) {
    .form-card,
    .detail-card {
        padding: 20px;
    }
}
```

---

# 🔄 Flujo MVC

## READ — Listado

```text
GET /usuarios
      ↓
controllers/usuarios.py
      ↓
Usuario.get_all()
      ↓
models/usuario.py
      ↓
mysqlconnection.py
      ↓
MySQL
      ↓
objetos Usuario
      ↓
index.html
```

## CREATE

```text
Formulario
      ↓
POST /usuarios/crear
      ↓
request.form
      ↓
Usuario.save()
      ↓
INSERT
      ↓
MySQL
      ↓
redirect()
      ↓
GET /usuarios
```

## READ — Detalle

```text
GET /usuarios/3
      ↓
Usuario.get_by_id(3)
      ↓
SELECT ... WHERE id = 3
      ↓
detalle.html
```

## UPDATE

```text
GET /usuarios/editar/3
      ↓
Usuario.get_by_id(3)
      ↓
editar.html
      ↓
POST /usuarios/3/actualizar
      ↓
request.form
      ↓
Usuario.update()
      ↓
UPDATE
      ↓
redirect()
      ↓
GET /usuarios
```

## DELETE

```text
Borrar
      ↓
confirm()
      ↓
/usuarios/borrar/3
      ↓
Usuario.delete()
      ↓
DELETE
      ↓
redirect()
      ↓
GET /usuarios
```

---

# 🧩 Responsabilidades

```text
flask_app/
│
├── config/
│   └── mysqlconnection.py
│       → conexión con MySQL
│
├── models/
│   └── usuario.py
│       → datos y SQL
│
├── controllers/
│   └── usuarios.py
│       → rutas y coordinación
│
├── templates/
│   → HTML + Jinja2
│
└── __init__.py
    → inicialización de Flask
```

---

# ✅ Resultado esperado

La aplicación debe permitir:

```text
http://127.0.0.1:5000/usuarios
```

y mostrar:

```text
Usuarios                                  Nuevo Usuario

┌────┬────────────────────┬────────────────────┬──────────────┬─────────────────────────┐
│ Id │ Nombre Completo    │ E-mail             │ Fecha        │ Acciones                │
├────┼────────────────────┼────────────────────┼──────────────┼─────────────────────────┤
│ 1  │ Ricky Martin       │ ricky@...          │ 2024-04-30   │ Ver Editar Borrar       │
│ 2  │ Enrique Iglesias   │ enrique@...        │ 2024-04-30   │ Ver Editar Borrar       │
│ 3  │ Celia Cruz         │ celia@...          │ 2024-04-30   │ Ver Editar Borrar       │
│ 4  │ Ricardo Montaner   │ ricardo@...        │ 2024-04-30   │ Ver Editar Borrar       │
└────┴────────────────────┴────────────────────┴──────────────┴─────────────────────────┘
```

La aplicación debe permitir navegar entre:

```text
/usuarios
/usuarios/nuevo
/usuarios/<id>
/usuarios/editar/<id>
/usuarios/<id>/actualizar
/usuarios/borrar/<id>
```

---

# 🚀 Ejecución

Desde la raíz del proyecto:

```bash
pipenv install
```

Luego:

```bash
pipenv run python server.py
```

Abrir:

```text
http://127.0.0.1:5000/usuarios
```

---

# 📦 Estructura MVC definitiva

```text
USUARIOS_CRUD_MVC/
│
├── flask_app/
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
│   │   ├── index.html
│   │   ├── nuevo.html
│   │   ├── detalle.html
│   │   └── editar.html
│   │
│   ├── static/
│   │   └── css/
│   │       └── style.css
│   │
│   └── __init__.py
│
├── resources/
│   └── esquema_usuarios.mwb
│
├── Pipfile
├── Pipfile.lock
└── server.py
```

---

# ✅ Checklist

```text
[ ] Pipenv configurado
[ ] Pipfile creado
[ ] Pipfile.lock generado
[ ] Base de datos creada
[ ] Tabla usuarios creada
[ ] ERD guardado en resources/
[ ] flask_app creado
[ ] __init__.py creado
[ ] config creado
[ ] mysqlconnection.py dentro de config
[ ] controllers creado
[ ] usuarios.py dentro de controllers
[ ] models creado
[ ] usuario.py dentro de models
[ ] templates dentro de flask_app
[ ] CREATE funcionando
[ ] READ funcionando
[ ] UPDATE funcionando
[ ] DELETE funcionando
[ ] url_for() funcionando
[ ] redirect() funcionando
[ ] Sentencias preparadas funcionando
[ ] Proyecto ejecutándose desde server.py
[ ] CRUD completo funcionando
```

---

# 📤 Entregables

### 1. Repositorio de GitHub

El repositorio debe contener el proyecto completo:

```text
USUARIOS_CRUD_MVC/
```

incluyendo:

```text
resources/
└── esquema_usuarios.mwb
```

### 2. Imagen del resultado

Incluir una captura de pantalla donde se evidencie la aplicación funcionando, idealmente mostrando:

```text
Usuarios
+
Listado
+
Acciones
```

La evidencia debe permitir comprobar visualmente que la aplicación modularizada funciona correctamente.
