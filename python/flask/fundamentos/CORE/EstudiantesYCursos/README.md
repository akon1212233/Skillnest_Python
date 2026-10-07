# Alumnos y Talleres — Core

## Descripción
Aplicación web con **Flask + MySQL + PyMySQL + Jinja2 + Bootstrap 5** para administrar talleres y alumnos.
Implementa una relación **uno a muchos (1:N)**:

```
TALLERES
   │ 1
   │
   │ N
   ▼
ALUMNOS
```
Un taller tiene varios alumnos y cada alumno pertenece a un taller.

## Objetivo
Practicar: conexión Flask–MySQL, MVC, POO, relaciones 1:N, claves foráneas, formularios POST,
`request.form`, consultas preparadas, `LEFT JOIN`, Jinja2, `url_for()`, `redirect()` y Bootstrap.

## Modelo de datos
```
talleres                      alumnos
├── id                        ├── id
├── titulo                    ├── nombre
├── created_at                ├── apellido
└── updated_at                ├── edad
                              ├── created_at
                              ├── updated_at
                              └── taller_id → talleres.id
```

## Estructura
```
ALUMNOS_TALLERES/
├── academia/
│   ├── __init__.py
│   ├── config/conexion.py
│   ├── controllers/{talleres.py, alumnos.py}
│   ├── models/{taller.py, alumno.py}
│   ├── templates/{base, talleres, nuevo_alumno, mostrar_taller}.html
│   ├── static/css/style.css
│   └── bd/academia_talleres.sql
├── resources/            ← guarda aquí academia_talleres_erd.mwb (MySQL Workbench)
├── Pipfile
├── Pipfile.lock
├── .gitignore
└── server.py
```

## Ejecutar
```bash
cd ALUMNOS_TALLERES
pipenv shell
python server.py          # http://127.0.0.1:5000
```
Si tu MySQL usa otro usuario/contraseña, edita `academia/config/conexion.py`.

## Rutas
| Método | Ruta | Función |
|--------|------|---------|
| GET  | `/` | Redirige a `/talleres` |
| GET  | `/talleres` | Lista talleres |
| POST | `/talleres/crear` | Crea un taller |
| GET  | `/talleres/<id>` | Muestra un taller y sus alumnos |
| GET  | `/alumnos/nuevo` | Formulario de alumno |
| POST | `/alumnos/crear` | Crea un alumno |

## Flujo
```
/talleres → Agregar Alumno → /alumnos/nuevo → Taller.obtener_todos() → <select>
→ POST /alumnos/crear → request.form → Alumno.guardar() → INSERT → redirect → /talleres
```

## Por qué LEFT JOIN
Para mostrar el taller aunque todavía no tenga alumnos ("Este taller todavía no tiene alumnos").

## Datos de prueba
Talleres: Robótica, Fotografía, Python, Diseño Web.
Alumnos: Camila Vargas, Joaquín Riquelme, Fernanda Lagos, Tomás Araya (Robótica) · Isidora Muñoz (Fotografía) · Benjamín Rojas (Python).

## Errores frecuentes
- **No se crea `alumnos`**: crea primero `talleres` (la FK depende de `talleres.id`).
- **`<select>` vacío**: revisa `Taller.obtener_todos()` y el `{% for taller in talleres %}`.
- **Error en `url_for()`**: el nombre debe coincidir con la función (`mostrar_taller`, `nuevo_alumno`…).
- **No conecta a MySQL**: ajusta `user` y `password` en `config/conexion.py`.

## Código fuente completo

### `server.py`

```python
from academia import app

# Importamos los controladores para registrar las rutas.
from academia.controllers import talleres
from academia.controllers import alumnos


if __name__ == "__main__":
    app.run(debug=True)
```

### `Pipfile`

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

### `.gitignore`

```text
__pycache__/
*.pyc
.venv/
venv/
.DS_Store
```

### `academia/__init__.py`

```python
from flask import Flask

app = Flask(__name__)
```

### `academia/config/conexion.py`

```python
import pymysql
import pymysql.cursors


class MySQLConnection:
    """
    Gestiona la conexión entre Flask y MySQL.
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
        Ejecuta la consulta SQL recibida.
        """

        with self.connection.cursor() as cursor:

            try:

                cursor.execute(
                    query,
                    data or {}
                )

                tipo_consulta = query.strip().lower()


                if tipo_consulta.startswith("select"):

                    return cursor.fetchall()


                if tipo_consulta.startswith("insert"):

                    return cursor.lastrowid


                return cursor.rowcount


            except Exception as e:

                print(
                    "Error en MySQL:",
                    e
                )

                return False


            finally:

                self.connection.close()


def connectToMySQL(db):
    """
    Crea una instancia de MySQLConnection.
    """

    return MySQLConnection(db)
```

### `academia/models/taller.py`

```python
from academia.config.conexion import connectToMySQL
from academia.models.alumno import Alumno

BD = "academia_talleres"


class Taller:
    """Representa un registro de la tabla talleres."""

    def __init__(self, datos):
        self.id = datos["id"]
        self.titulo = datos["titulo"]
        self.created_at = datos["created_at"]
        self.updated_at = datos["updated_at"]
        self.alumnos = []

    @classmethod
    def obtener_todos(cls):
        """Obtiene todos los talleres ordenados por título."""
        consulta = """
            SELECT id, titulo, created_at, updated_at
            FROM talleres
            ORDER BY titulo;
        """
        resultados = connectToMySQL(BD).query_db(consulta) or []
        return [cls(fila) for fila in resultados]

    @classmethod
    def guardar(cls, datos):
        """Crea un nuevo taller."""
        consulta = """
            INSERT INTO talleres (titulo)
            VALUES (%(titulo)s);
        """
        return connectToMySQL(BD).query_db(consulta, datos)

    @classmethod
    def obtener_con_alumnos(cls, taller_id):
        """
        Obtiene un taller junto con sus alumnos.
        LEFT JOIN conserva el taller aunque no tenga alumnos todavía.
        """
        consulta = """
            SELECT
                t.id         AS taller_id,
                t.titulo     AS taller_titulo,
                t.created_at AS taller_created_at,
                t.updated_at AS taller_updated_at,

                a.id         AS alumno_id,
                a.nombre     AS alumno_nombre,
                a.apellido   AS alumno_apellido,
                a.edad       AS alumno_edad,
                a.created_at AS alumno_created_at,
                a.updated_at AS alumno_updated_at

            FROM talleres t
            LEFT JOIN alumnos a
                ON t.id = a.taller_id
            WHERE t.id = %(id)s;
        """
        resultados = connectToMySQL(BD).query_db(consulta, {"id": taller_id})

        if not resultados:
            return None

        taller = cls({
            "id": resultados[0]["taller_id"],
            "titulo": resultados[0]["taller_titulo"],
            "created_at": resultados[0]["taller_created_at"],
            "updated_at": resultados[0]["taller_updated_at"],
        })

        for fila in resultados:
            if fila["alumno_id"] is not None:
                taller.alumnos.append(Alumno({
                    "id": fila["alumno_id"],
                    "nombre": fila["alumno_nombre"],
                    "apellido": fila["alumno_apellido"],
                    "edad": fila["alumno_edad"],
                    "created_at": fila["alumno_created_at"],
                    "updated_at": fila["alumno_updated_at"],
                    "taller_id": taller.id,
                }))

        return taller
```

### `academia/models/alumno.py`

```python
from academia.config.conexion import connectToMySQL

BD = "academia_talleres"


class Alumno:
    """Representa un registro de la tabla alumnos."""

    def __init__(self, datos):
        self.id = datos["id"]
        self.nombre = datos["nombre"]
        self.apellido = datos["apellido"]
        self.edad = datos["edad"]
        self.created_at = datos["created_at"]
        self.updated_at = datos["updated_at"]
        self.taller_id = datos["taller_id"]

    @classmethod
    def guardar(cls, datos):
        """Crea un alumno asociado a un taller."""
        consulta = """
            INSERT INTO alumnos
                (nombre, apellido, edad, taller_id)
            VALUES
                (%(nombre)s, %(apellido)s, %(edad)s, %(taller_id)s);
        """
        return connectToMySQL(BD).query_db(consulta, datos)
```

### `academia/controllers/talleres.py`

```python
from flask import render_template, request, redirect, url_for

from academia import app
from academia.models.taller import Taller


# ---------------- PÁGINA PRINCIPAL ----------------
@app.route("/")
def inicio():
    """Redirige la raíz hacia la página de talleres."""
    return redirect(url_for("talleres"))


# ---------------- LISTAR TALLERES ----------------
@app.route("/talleres")
def talleres():
    """Obtiene y muestra todos los talleres."""
    todos = Taller.obtener_todos()
    return render_template("talleres.html", talleres=todos)


# ---------------- CREAR TALLER ----------------
@app.route("/talleres/crear", methods=["POST"])
def crear_taller():
    """Recibe el título del taller y crea el registro."""
    titulo = request.form.get("titulo", "").strip()

    if titulo:
        Taller.guardar({"titulo": titulo})

    return redirect(url_for("talleres"))


# ---------------- MOSTRAR TALLER ----------------
@app.route("/talleres/<int:id>")
def mostrar_taller(id):
    """Obtiene un taller y sus alumnos."""
    taller = Taller.obtener_con_alumnos(id)

    if taller is None:
        return redirect(url_for("talleres"))

    return render_template("mostrar_taller.html", taller=taller)
```

### `academia/controllers/alumnos.py`

```python
from flask import render_template, request, redirect, url_for

from academia import app
from academia.models.taller import Taller
from academia.models.alumno import Alumno


# ---------------- FORMULARIO NUEVO ALUMNO ----------------
@app.route("/alumnos/nuevo")
def nuevo_alumno():
    """Carga los talleres para el <select> del formulario."""
    return render_template("nuevo_alumno.html", talleres=Taller.obtener_todos())


# ---------------- CREAR ALUMNO ----------------
@app.route("/alumnos/crear", methods=["POST"])
def crear_alumno():
    """Recibe el formulario y crea un alumno."""
    nombre = request.form.get("nombre", "").strip()
    apellido = request.form.get("apellido", "").strip()
    edad = request.form.get("edad", "").strip()
    taller_id = request.form.get("taller_id", "").strip()

    if not (nombre and apellido and edad and taller_id):
        return redirect(url_for("nuevo_alumno"))

    try:
        edad = int(edad)
        taller_id = int(taller_id)
    except ValueError:
        return redirect(url_for("nuevo_alumno"))

    Alumno.guardar({
        "nombre": nombre,
        "apellido": apellido,
        "edad": edad,
        "taller_id": taller_id,
    })

    return redirect(url_for("talleres"))
```

### `academia/templates/base.html`

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Alumnos y Talleres{% endblock %}</title>

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>

<nav class="navbar navbar-dark bg-dark">
    <div class="container">
        <a class="navbar-brand" href="{{ url_for('talleres') }}">Alumnos y Talleres</a>
    </div>
</nav>

<main class="container py-5">
    {% block contenido %}{% endblock %}
</main>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

### `academia/templates/talleres.html`

```html
{% extends "base.html" %}

{% block title %}Talleres{% endblock %}

{% block contenido %}
<div class="row g-4">

    <!-- ================= NUEVO TALLER ================= -->
    <div class="col-lg-5">
        <div class="card shadow-sm h-100">
            <div class="card-body">
                <h1 class="h3 mb-4">Nuevo Taller</h1>

                <form action="{{ url_for('crear_taller') }}" method="POST">
                    <div class="mb-3">
                        <label for="titulo" class="form-label">Título</label>
                        <input type="text" id="titulo" name="titulo" class="form-control" required>
                    </div>
                    <button type="submit" class="btn btn-success">Crear</button>
                </form>
            </div>
        </div>
    </div>

    <!-- ================= TODOS LOS TALLERES ================= -->
    <div class="col-lg-7">
        <div class="card shadow-sm h-100">
            <div class="card-body">
                <h2 class="h3 mb-4">Todos los Talleres</h2>

                {% if talleres %}
                    <div class="list-group">
                        {% for taller in talleres %}
                            <a href="{{ url_for('mostrar_taller', id=taller.id) }}"
                               class="list-group-item list-group-item-action">
                                {{ taller.titulo }}
                            </a>
                        {% endfor %}
                    </div>
                {% else %}
                    <div class="alert alert-info">No hay talleres registrados.</div>
                {% endif %}

                <div class="mt-4">
                    <a href="{{ url_for('nuevo_alumno') }}" class="btn btn-primary">Agregar Alumno</a>
                </div>
            </div>
        </div>
    </div>

</div>
{% endblock %}
```

### `academia/templates/nuevo_alumno.html`

```html
{% extends "base.html" %}

{% block title %}Nuevo Alumno{% endblock %}

{% block contenido %}
<div class="row justify-content-center">
    <div class="col-lg-7">
        <div class="card shadow-sm">
            <div class="card-body">
                <h1 class="h3 mb-4">Nuevo Alumno</h1>

                <form action="{{ url_for('crear_alumno') }}" method="POST">

                    <!-- TALLER -->
                    <div class="mb-3">
                        <label for="taller_id" class="form-label">Taller</label>
                        <select id="taller_id" name="taller_id" class="form-select" required>
                            <option value="">Selecciona un taller</option>
                            {% for taller in talleres %}
                                <option value="{{ taller.id }}">{{ taller.titulo }}</option>
                            {% endfor %}
                        </select>
                    </div>

                    <!-- NOMBRE -->
                    <div class="mb-3">
                        <label for="nombre" class="form-label">Nombre</label>
                        <input type="text" id="nombre" name="nombre" class="form-control" required>
                    </div>

                    <!-- APELLIDO -->
                    <div class="mb-3">
                        <label for="apellido" class="form-label">Apellido</label>
                        <input type="text" id="apellido" name="apellido" class="form-control" required>
                    </div>

                    <!-- EDAD -->
                    <div class="mb-4">
                        <label for="edad" class="form-label">Edad</label>
                        <input type="number" id="edad" name="edad" class="form-control" min="1" required>
                    </div>

                    <button type="submit" class="btn btn-success">Crear</button>
                    <a href="{{ url_for('talleres') }}" class="btn btn-outline-secondary">Inicio</a>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### `academia/templates/mostrar_taller.html`

```html
{% extends "base.html" %}

{% block title %}{{ taller.titulo }}{% endblock %}

{% block contenido %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <div>
        <h1 class="mb-1">Alumnos de {{ taller.titulo }}</h1>
        <p class="text-muted mb-0">Alumnos inscritos en el taller seleccionado.</p>
    </div>
    <a href="{{ url_for('talleres') }}" class="btn btn-outline-primary">Inicio</a>
</div>

<div class="card shadow-sm">
    <div class="card-body p-0">

        {% if taller.alumnos %}
            <div class="table-responsive">
                <table class="table table-striped table-hover mb-0">
                    <thead class="table-dark">
                        <tr>
                            <th>Nombre</th>
                            <th>Apellido</th>
                            <th>Edad</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for alumno in taller.alumnos %}
                            <tr>
                                <td>{{ alumno.nombre }}</td>
                                <td>{{ alumno.apellido }}</td>
                                <td>{{ alumno.edad }}</td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        {% else %}
            <div class="p-4">
                <div class="alert alert-info mb-0">Este taller todavía no tiene alumnos.</div>
            </div>
        {% endif %}

    </div>
</div>
{% endblock %}
```

### `academia/static/css/style.css`

```css
body {
    background-color: #f3f4f9;
    color: #212529;
    font-family: Arial, Helvetica, sans-serif;
}

.navbar-brand { font-weight: 700; }

.card { border: none; border-radius: 12px; }

.form-control,
.form-select,
.btn { border-radius: 8px; }

.list-group-item {
    border-radius: 8px !important;
    margin-bottom: 8px;
}

.table { vertical-align: middle; }

@media (max-width: 768px) {
    .container { padding-left: 16px; padding-right: 16px; }
}
```

### `academia/bd/academia_talleres.sql`

```sql
-- ==========================================================
-- CREACIÓN DE LA BASE DE DATOS
-- ==========================================================

CREATE DATABASE IF NOT EXISTS academia_talleres;

USE academia_talleres;


-- ==========================================================
-- TABLA TALLERES
-- ==========================================================

CREATE TABLE IF NOT EXISTS talleres (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(60) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);


-- ==========================================================
-- TABLA ALUMNOS
-- ==========================================================

CREATE TABLE IF NOT EXISTS alumnos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(45) NOT NULL,
    apellido VARCHAR(45) NOT NULL,
    edad INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    taller_id INT NOT NULL,

    CONSTRAINT fk_alumnos_taller
        FOREIGN KEY (taller_id)
        REFERENCES talleres(id)
);


-- ==========================================================
-- DATOS DE PRUEBA
-- ==========================================================

INSERT INTO talleres (titulo) VALUES
("Robótica"),
("Fotografía"),
("Python"),
("Diseño Web");

INSERT INTO alumnos (nombre, apellido, edad, taller_id) VALUES
("Camila",   "Vargas",   19, 1),
("Joaquín",  "Riquelme", 21, 1),
("Fernanda", "Lagos",    20, 1),
("Tomás",    "Araya",    22, 1),
("Isidora",  "Muñoz",    18, 2),
("Benjamín", "Rojas",    23, 3);
```
