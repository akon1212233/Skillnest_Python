# 👥 Insertar registros en una relación muchos a muchos

## Descripción

En esta actividad aprenderemos a implementar una relación **muchos a muchos (N:N)** utilizando Flask, MySQL, PyMySQL, POO y una tabla intermedia.

Trabajaremos con tres tablas:

```text
estudiantes
cursos
inscripciones
```

La tabla `inscripciones` será la encargada de relacionar a los estudiantes con los cursos.

La aplicación permitirá seleccionar un estudiante, seleccionar un curso y registrar la inscripción en la base de datos.

---

# 🎯 Objetivos

Al finalizar la actividad podrás:

- Comprender qué es una relación muchos a muchos.
- Identificar cuándo es necesario utilizar una tabla intermedia.
- Comprender el funcionamiento de una `PRIMARY KEY` compuesta.
- Utilizar dos `FOREIGN KEY` en una tabla intermedia.
- Insertar relaciones desde Flask.
- Utilizar formularios HTML con `<select>`.
- Utilizar `request.form`.
- Utilizar sentencias preparadas.
- Validar que estudiante y curso existan.
- Evitar inscripciones duplicadas.
- Utilizar POO para representar los datos.
- Aplicar MVC en una aplicación Flask.

---

# 🧠 ¿Qué es una relación muchos a muchos?

Una relación **muchos a muchos** ocurre cuando:

> Un registro de una tabla puede relacionarse con muchos registros de otra tabla y, al mismo tiempo, esos registros pueden relacionarse con muchos registros de la primera tabla.

En nuestro caso:

```text
Un estudiante
    ↓
puede estar inscrito en muchos cursos
```

y:

```text
Un curso
    ↓
puede tener muchos estudiantes
```

Por lo tanto:

```text
ESTUDIANTE N : N CURSO
```

---

# 🧩 ¿Por qué necesitamos una tabla intermedia?

No podemos solucionar esta relación colocando solamente una clave foránea en `estudiantes` o en `cursos`.

Necesitamos una tercera tabla:

```text
inscripciones
```

La estructura será:

```text
┌─────────────────────┐
│     estudiantes     │
├─────────────────────┤
│ id_estudiante PK    │
│ nombre              │
│ email               │
│ created_at          │
└──────────┬──────────┘
           │
           │ 1
           │
           │ N
┌──────────▼──────────┐
│    inscripciones    │
├─────────────────────┤
│ estudiante_id FK    │
│ curso_id FK         │
├─────────────────────┤
│ PK compuesta        │
└──────────┬──────────┘
           │
           │ N
           │
           │ 1
┌──────────▼──────────┐
│       cursos        │
├─────────────────────┤
│ id_curso PK         │
│ nombre_curso        │
│ descripcion         │
│ created_at          │
└─────────────────────┘
```

La relación:

```text
Estudiante N:N Curso
```

se transforma en:

```text
Estudiante 1:N Inscripciones N:1 Curso
```

---

# 🔑 Claves de la relación

Tenemos:

```text
estudiantes.id_estudiante
```

y:

```text
cursos.id_curso
```

Ambos son identificadores de sus respectivas tablas.

La tabla `inscripciones` almacena esos identificadores:

```text
estudiante_id
curso_id
```

Por ejemplo:

```text
estudiante_id = 1
curso_id = 3
```

significa:

```text
El estudiante 1 está inscrito en el curso 3.
```

---

# 🔐 PRIMARY KEY compuesta

En `inscripciones` utilizaremos:

```sql
PRIMARY KEY (estudiante_id, curso_id)
```

Esto significa que la combinación:

```text
(estudiante_id, curso_id)
```

debe ser única.

Por ejemplo:

```text
(1, 3)
```

puede existir una vez.

Pero no:

```text
(1, 3)
(1, 3)
```

La segunda inscripción sería duplicada.

---

# 🧠 ¿Por qué no hacemos que `estudiante_id` sea la PRIMARY KEY?

Porque entonces un estudiante solamente podría aparecer una vez.

Por ejemplo:

```text
estudiante_id
-------------
1
2
3
```

pero necesitamos permitir:

```text
1 → curso 1
1 → curso 2
1 → curso 3
```

Por eso usamos:

```text
PRIMARY KEY (estudiante_id, curso_id)
```

---

# 📁 Estructura del proyecto

```text
inscripciones_app/
│
├── flask_app/
│   │
│   ├── __init__.py
│   │
│   ├── bd/
│   │   └── esquema_educacion.sql
│   │
│   ├── config/
│   │   ├
│   │   └── mysqlconnection.py
│   │
│   ├── controllers/
│   │   ├
│   │   └── inscripciones.py
│   │
│   ├── models/
│   │   ├
│   │   ├── estudiante.py
│   │   ├── curso.py
│   │   └── inscripcion.py
│   │
│   ├── templates/
│   │   └── index.html
│   │
│   └── static/
│       └── css/
│           └── style.css
│
├── resources/
│   └── esquema_educacion_erd.mwb
│
├── Pipfile
├── Pipfile.lock
├── .gitignore
└── server.py
```

> La carpeta `resources/` debe contener siempre el **ERD correspondiente al proyecto**.

---

# 🐍 Pipenv

Instalar Flask y PyMySQL:

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

`Pipfile.lock` debe ser generado automáticamente por Pipenv:

```bash
pipenv lock
```

No es necesario escribirlo manualmente.

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

## `flask_app/bd/esquema_educacion.sql`

```sql
-- ==========================================================
-- CREAR BASE DE DATOS
-- ==========================================================

CREATE DATABASE IF NOT EXISTS esquema_educacion;

USE esquema_educacion;


-- ==========================================================
-- TABLA ESTUDIANTES
-- ==========================================================

CREATE TABLE IF NOT EXISTS estudiantes (
    id_estudiante INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ==========================================================
-- TABLA CURSOS
-- ==========================================================

CREATE TABLE IF NOT EXISTS cursos (
    id_curso INT AUTO_INCREMENT PRIMARY KEY,
    nombre_curso VARCHAR(100) NOT NULL,
    descripcion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ==========================================================
-- TABLA INTERMEDIA
-- ==========================================================

CREATE TABLE IF NOT EXISTS inscripciones (
    estudiante_id INT NOT NULL,
    curso_id INT NOT NULL,

    PRIMARY KEY (
        estudiante_id,
        curso_id
    ),

    CONSTRAINT fk_inscripcion_estudiante
        FOREIGN KEY (estudiante_id)
        REFERENCES estudiantes(id_estudiante),

    CONSTRAINT fk_inscripcion_curso
        FOREIGN KEY (curso_id)
        REFERENCES cursos(id_curso)
);


-- ==========================================================
-- ESTUDIANTES DE PRUEBA
-- ==========================================================

INSERT INTO estudiantes
(
    nombre,
    email
)
VALUES
(
    "Juan Pérez",
    "juan@email.com"
),
(
    "Ana González",
    "ana@email.com"
),
(
    "Carlos Soto",
    "carlos@email.com"
),
(
    "María López",
    "maria@email.com"
);


-- ==========================================================
-- CURSOS DE PRUEBA
-- ==========================================================

INSERT INTO cursos
(
    nombre_curso,
    descripcion
)
VALUES
(
    "MERN",
    "Desarrollo web con MongoDB, Express, React y Node.js"
),
(
    "Python",
    "Programación y desarrollo web con Python"
),
(
    "Java",
    "Desarrollo de aplicaciones utilizando Java"
),
(
    "Fundamentos de la Web",
    "HTML, CSS y conceptos fundamentales de desarrollo web"
);
```

---

# 🔍 Comprobar las tablas

```sql
USE esquema_educacion;

DESCRIBE estudiantes;
```

```sql
DESCRIBE cursos;
```

```sql
DESCRIBE inscripciones;
```

---

# 🔎 Ver los datos

```sql
SELECT *
FROM estudiantes;
```

```sql
SELECT *
FROM cursos;
```

```sql
SELECT *
FROM inscripciones;
```

---

# 🧪 Insertar directamente una relación

Antes de trabajar con Flask podemos probar directamente en MySQL:

```sql
INSERT INTO inscripciones
(
    estudiante_id,
    curso_id
)
VALUES
(
    1,
    3
);
```

Esto significa:

```text
Estudiante 1
        ↓
Curso 3
```

---

# 🔍 Comprobar la relación

```sql
SELECT
    estudiantes.id_estudiante,
    estudiantes.nombre AS estudiante,
    cursos.id_curso,
    cursos.nombre_curso
FROM inscripciones
INNER JOIN estudiantes
    ON inscripciones.estudiante_id =
       estudiantes.id_estudiante
INNER JOIN cursos
    ON inscripciones.curso_id =
       cursos.id_curso;
```

El resultado será conceptualmente:

```text
id_estudiante | estudiante | id_curso | nombre_curso
--------------|------------|----------|-------------
1             | Juan Pérez | 3        | Java
```

---

# ⚙️ Flask

## `flask_app/__init__.py`

```python
from flask import Flask

app = Flask(__name__)

# Necesaria para utilizar mensajes flash.
app.secret_key = "clave-secreta-desarrollo"
```

---

# 🔌 Configuración MySQL

## `flask_app/config/__init__.py`

```python
# Paquete de configuración.
```

---

# 📄 `flask_app/config/mysqlconnection.py`

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
            devuelve el ID generado o las filas afectadas.

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


                if query.strip().lower().startswith("select"):

                    return cursor.fetchall()


                if query.strip().lower().startswith("insert"):

                    return cursor.lastrowid or cursor.rowcount


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
    Recibe el nombre de la base de datos
    y devuelve una conexión.
    """

    return MySQLConnection(db)
```

> Cambia `user` y `password` según tu instalación local de MySQL.

---

# 👨‍🎓 Modelo Estudiante

## `flask_app/models/__init__.py`

```python
# Paquete de modelos.
```

## `flask_app/models/estudiante.py`

```python
from flask_app.config.mysqlconnection import connectToMySQL


class Estudiante:
    """
    Representa un registro de la tabla estudiantes.
    """

    def __init__(self, data):
        self.id_estudiante = data["id_estudiante"]
        self.nombre = data["nombre"]
        self.email = data["email"]
        self.created_at = data["created_at"]


    @classmethod
    def get_all(cls):
        """
        Obtiene todos los estudiantes.
        """

        query = """
            SELECT
                id_estudiante,
                nombre,
                email,
                created_at
            FROM estudiantes
            ORDER BY id_estudiante;
        """


        resultados = connectToMySQL(
            "esquema_educacion"
        ).query_db(query)


        estudiantes = []


        for estudiante in resultados:

            estudiantes.append(
                cls(estudiante)
            )


        return estudiantes


    @classmethod
    def get_by_id(cls, id_estudiante):
        """
        Busca un estudiante específico por su ID.
        """

        query = """
            SELECT
                id_estudiante,
                nombre,
                email,
                created_at
            FROM estudiantes
            WHERE id_estudiante = %(id_estudiante)s;
        """


        data = {
            "id_estudiante": id_estudiante
        }


        resultados = connectToMySQL(
            "esquema_educacion"
        ).query_db(
            query,
            data
        )


        if resultados:

            return cls(
                resultados[0]
            )


        return None
```

---

# 📚 Modelo Curso

## `flask_app/models/curso.py`

```python
from flask_app.config.mysqlconnection import connectToMySQL


class Curso:
    """
    Representa un registro de la tabla cursos.
    """

    def __init__(self, data):
        self.id_curso = data["id_curso"]
        self.nombre_curso = data["nombre_curso"]
        self.descripcion = data["descripcion"]
        self.created_at = data["created_at"]


    @classmethod
    def get_all(cls):
        """
        Obtiene todos los cursos.
        """

        query = """
            SELECT
                id_curso,
                nombre_curso,
                descripcion,
                created_at
            FROM cursos
            ORDER BY id_curso;
        """


        resultados = connectToMySQL(
            "esquema_educacion"
        ).query_db(query)


        cursos = []


        for curso in resultados:

            cursos.append(
                cls(curso)
            )


        return cursos


    @classmethod
    def get_by_id(cls, id_curso):
        """
        Busca un curso específico por su ID.
        """

        query = """
            SELECT
                id_curso,
                nombre_curso,
                descripcion,
                created_at
            FROM cursos
            WHERE id_curso = %(id_curso)s;
        """


        data = {
            "id_curso": id_curso
        }


        resultados = connectToMySQL(
            "esquema_educacion"
        ).query_db(
            query,
            data
        )


        if resultados:

            return cls(
                resultados[0]
            )


        return None
```

---

# 🔗 Modelo Inscripción

Este modelo representa la tabla intermedia.

No representa un estudiante ni un curso.

Representa:

```text
la relación entre ambos
```

---

# 📄 `flask_app/models/inscripcion.py`

```python
from flask_app.config.mysqlconnection import connectToMySQL


class Inscripcion:
    """
    Representa una relación entre un estudiante y un curso.
    """

    @classmethod
    def existe(cls, data):
        """
        Comprueba si la relación ya existe.
        """

        query = """
            SELECT
                estudiante_id,
                curso_id
            FROM inscripciones
            WHERE estudiante_id = %(estudiante_id)s
              AND curso_id = %(curso_id)s;
        """


        resultado = connectToMySQL(
            "esquema_educacion"
        ).query_db(
            query,
            data
        )


        return bool(resultado)


    @classmethod
    def inscribir_estudiante_en_curso(cls, data):
        """
        Crea una relación entre un estudiante y un curso.
        """

        query = """
            INSERT INTO inscripciones
            (
                estudiante_id,
                curso_id
            )
            VALUES
            (
                %(estudiante_id)s,
                %(curso_id)s
            );
        """


        return connectToMySQL(
            "esquema_educacion"
        ).query_db(
            query,
            data
        )


    @classmethod
    def get_all(cls):
        """
        Obtiene todas las inscripciones mostrando
        los nombres del estudiante y del curso.
        """

        query = """
            SELECT
                estudiantes.id_estudiante,
                estudiantes.nombre AS estudiante,
                estudiantes.email,
                cursos.id_curso,
                cursos.nombre_curso

            FROM inscripciones

            INNER JOIN estudiantes
                ON inscripciones.estudiante_id =
                   estudiantes.id_estudiante

            INNER JOIN cursos
                ON inscripciones.curso_id =
                   cursos.id_curso

            ORDER BY
                estudiantes.id_estudiante,
                cursos.id_curso;
        """


        return connectToMySQL(
            "esquema_educacion"
        ).query_db(query)
```

---

# 🧠 ¿Qué diferencia existe entre los modelos?

Tenemos:

```text
Estudiante
    ↓
representa estudiantes

Curso
    ↓
representa cursos

Inscripcion
    ↓
representa relaciones
```

Por eso:

```python
Estudiante(...)
```

representa una persona.

```python
Curso(...)
```

representa un curso.

Mientras:

```python
Inscripcion
```

representa:

```text
Estudiante + Curso
```

---

# 🎮 Controlador

## `flask_app/controllers/__init__.py`

```python
# Paquete de controladores.
```

---

# 📄 `flask_app/controllers/inscripciones.py`

```python
from flask_app import app

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_app.models.estudiante import Estudiante
from flask_app.models.curso import Curso
from flask_app.models.inscripcion import Inscripcion


# ==========================================================
# RUTA PRINCIPAL
# ==========================================================

@app.route("/")
def index():
    """
    Muestra el formulario de inscripción.

    También obtiene estudiantes, cursos e inscripciones
    para mostrar información dinámica.
    """

    estudiantes = Estudiante.get_all()

    cursos = Curso.get_all()

    inscripciones = Inscripcion.get_all()


    return render_template(
        "index.html",
        estudiantes=estudiantes,
        cursos=cursos,
        inscripciones=inscripciones
    )


# ==========================================================
# CREAR INSCRIPCIÓN
# ==========================================================

@app.route(
    "/inscribir",
    methods=["POST"]
)
def inscribir():
    """
    Recibe estudiante_id y curso_id y crea
    una relación en la tabla inscripciones.
    """

    estudiante_id_texto = request.form.get(
        "estudiante_id"
    )

    curso_id_texto = request.form.get(
        "curso_id"
    )


    # ------------------------------------------------------
    # Comprobar que ambos valores fueron enviados.
    # ------------------------------------------------------

    if not estudiante_id_texto or not curso_id_texto:

        flash(
            "Debes seleccionar un estudiante y un curso.",
            "danger"
        )

        return redirect(
            url_for("index")
        )


    # ------------------------------------------------------
    # Convertir IDs a enteros.
    # ------------------------------------------------------

    try:

        estudiante_id = int(
            estudiante_id_texto
        )

        curso_id = int(
            curso_id_texto
        )

    except ValueError:

        flash(
            "Los identificadores no son válidos.",
            "danger"
        )

        return redirect(
            url_for("index")
        )


    # ------------------------------------------------------
    # Comprobar que el estudiante exista.
    # ------------------------------------------------------

    estudiante = Estudiante.get_by_id(
        estudiante_id
    )


    if estudiante is None:

        flash(
            "El estudiante seleccionado no existe.",
            "danger"
        )

        return redirect(
            url_for("index")
        )


    # ------------------------------------------------------
    # Comprobar que el curso exista.
    # ------------------------------------------------------

    curso = Curso.get_by_id(
        curso_id
    )


    if curso is None:

        flash(
            "El curso seleccionado no existe.",
            "danger"
        )

        return redirect(
            url_for("index")
        )


    # ------------------------------------------------------
    # Crear diccionario para la relación.
    # ------------------------------------------------------

    data = {

        "estudiante_id": estudiante_id,

        "curso_id": curso_id

    }


    # ------------------------------------------------------
    # Evitar una inscripción duplicada.
    # ------------------------------------------------------

    if Inscripcion.existe(data):

        flash(
            "El estudiante ya está inscrito en este curso.",
            "warning"
        )

        return redirect(
            url_for("index")
        )


    # ------------------------------------------------------
    # Insertar relación.
    # ------------------------------------------------------

    resultado = Inscripcion.inscribir_estudiante_en_curso(
        data
    )


    if resultado is False:

        flash(
            "No fue posible crear la inscripción.",
            "danger"
        )

        return redirect(
            url_for("index")
        )


    # ------------------------------------------------------
    # Inscripción exitosa.
    # ------------------------------------------------------

    flash(
        "Inscripción realizada correctamente.",
        "success"
    )


    return redirect(
        url_for("index")
    )
```

---

# 🧠 Analizando el Controller

El controlador recibe:

```text
estudiante_id
curso_id
```

y construye:

```python
data = {
    "estudiante_id": estudiante_id,
    "curso_id": curso_id
}
```

Este diccionario representa la relación que queremos guardar.

---

# 🔄 Flujo completo

```text
Formulario
     ↓
POST /inscribir
     ↓
request.form
     ↓
estudiante_id
curso_id
     ↓
validar estudiante
     ↓
validar curso
     ↓
comprobar duplicado
     ↓
Inscripcion.inscribir_estudiante_en_curso()
     ↓
INSERT
     ↓
inscripciones
     ↓
redirect()
     ↓
GET /
```

---

# 🌐 Vista

## `flask_app/templates/index.html`

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
        Inscripciones
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


    <!-- ==================================================
         ENCABEZADO
    =================================================== -->

    <div class="text-center mb-5">

        <h1>
            Inscribir estudiante
        </h1>

        <p class="text-muted">
            Relación muchos a muchos entre estudiantes y cursos.
        </p>

    </div>


    <!-- ==================================================
         MENSAJES
    =================================================== -->

    {% with mensajes = get_flashed_messages(with_categories=true) %}

        {% if mensajes %}

            {% for categoria, mensaje in mensajes %}

                <div class="alert alert-{{ categoria }}">

                    {{ mensaje }}

                </div>

            {% endfor %}

        {% endif %}

    {% endwith %}


    <!-- ==================================================
         FORMULARIO
    =================================================== -->

    <div class="card shadow-sm border-0 mb-5">

        <div class="card-body p-4">

            <h2 class="h4 mb-4">
                Nueva inscripción
            </h2>


            <form
                action="{{ url_for('inscribir') }}"
                method="POST"
            >


                <!-- ESTUDIANTE -->

                <div class="mb-3">

                    <label
                        for="estudiante_id"
                        class="form-label"
                    >
                        Estudiante
                    </label>


                    <select
                        id="estudiante_id"
                        name="estudiante_id"
                        class="form-select"
                        required
                    >

                        <option value="">
                            Selecciona un estudiante
                        </option>


                        {% for estudiante in estudiantes %}

                            <option
                                value="{{ estudiante.id_estudiante }}"
                            >

                                {{ estudiante.nombre }}
                                — {{ estudiante.email }}

                            </option>

                        {% endfor %}

                    </select>

                </div>


                <!-- CURSO -->

                <div class="mb-4">

                    <label
                        for="curso_id"
                        class="form-label"
                    >
                        Curso
                    </label>


                    <select
                        id="curso_id"
                        name="curso_id"
                        class="form-select"
                        required
                    >

                        <option value="">
                            Selecciona un curso
                        </option>


                        {% for curso in cursos %}

                            <option
                                value="{{ curso.id_curso }}"
                            >

                                {{ curso.nombre_curso }}

                            </option>

                        {% endfor %}

                    </select>

                </div>


                <button
                    type="submit"
                    class="btn btn-primary"
                >

                    Inscribir

                </button>


            </form>

        </div>

    </div>


    <!-- ==================================================
         INSCRIPCIONES REGISTRADAS
    =================================================== -->

    <div class="card shadow-sm border-0">

        <div class="card-body p-4">

            <h2 class="h4 mb-4">
                Inscripciones registradas
            </h2>


            {% if inscripciones %}


                <div class="table-responsive">

                    <table class="table table-hover align-middle">

                        <thead class="table-dark">

                            <tr>

                                <th>
                                    Estudiante
                                </th>

                                <th>
                                    Email
                                </th>

                                <th>
                                    Curso
                                </th>

                            </tr>

                        </thead>


                        <tbody>

                            {% for inscripcion in inscripciones %}

                                <tr>

                                    <td>

                                        {{ inscripcion.estudiante }}

                                    </td>


                                    <td>

                                        {{ inscripcion.email }}

                                    </td>


                                    <td>

                                        {{ inscripcion.nombre_curso }}

                                    </td>

                                </tr>

                            {% endfor %}

                        </tbody>

                    </table>

                </div>


            {% else %}


                <div class="alert alert-info mb-0">

                    Todavía no existen inscripciones.

                </div>


            {% endif %}


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
from flask_app.controllers import inscripciones


if __name__ == "__main__":
    app.run(debug=True)
```

---

# 🧠 ¿Por qué necesitamos importar el controlador?

En:

```python
from flask_app.controllers import inscripciones
```

no estamos utilizando directamente una variable llamada `inscripciones`.

La importación hace que Python cargue:

```text
flask_app/controllers/inscripciones.py
```

y Flask registre las rutas decoradas con:

```python
@app.route(...)
```

---

# 🔗 El `<select>` y la relación

Este elemento:

```html
<select name="estudiante_id">
```

permite enviar el ID del estudiante.

Cada opción:

```jinja
<option value="{{ estudiante.id_estudiante }}">
    {{ estudiante.nombre }}
</option>
```

tiene dos partes.

El usuario ve:

```text
Juan Pérez
```

pero Flask recibe:

```text
estudiante_id = 1
```

Lo mismo ocurre con el curso:

```jinja
<option value="{{ curso.id_curso }}">
    {{ curso.nombre_curso }}
</option>
```

El usuario ve:

```text
Java
```

pero Flask recibe:

```text
curso_id = 3
```

---

# 🔄 Flujo del `<select>`

```text
USUARIO VE:

Juan Pérez
      ↓
MERN

        ↓

FORMULARIO ENVÍA:

estudiante_id = 1
curso_id = 1

        ↓

Flask recibe:

request.form

        ↓

data = {
    "estudiante_id": 1,
    "curso_id": 1
}

        ↓

INSERT INTO inscripciones

        ↓

(1, 1)
```

---

# 🧠 Diferencia entre crear entidades y crear relaciones

Este concepto es fundamental.

## Crear estudiante

```sql
INSERT INTO estudiantes
```

crea:

```text
un estudiante
```

## Crear curso

```sql
INSERT INTO cursos
```

crea:

```text
un curso
```

## Crear inscripción

```sql
INSERT INTO inscripciones
```

NO crea un estudiante.

NO crea un curso.

Crea:

```text
una relación
```

entre ambos.

---

# 📊 Ejemplo

Tenemos:

```text
Estudiantes

1 → Juan
2 → Ana
```

y:

```text
Cursos

1 → MERN
2 → Python
3 → Java
```

Podemos tener:

```text
inscripciones

estudiante_id | curso_id
--------------|---------
1             | 1
1             | 2
2             | 1
2             | 3
```

Esto significa:

```text
Juan
 ├── MERN
 └── Python

Ana
 ├── MERN
 └── Java
```

Ahora sí tenemos una verdadera relación muchos a muchos.

---

# 🔗 La tabla intermedia

Visualmente:

```text
                  INSCRIPCIONES

               ┌─────────────────┐
               │ estudiante_id   │
               │ curso_id        │
               └─────────────────┘
                       ▲
                       │
          ┌────────────┴────────────┐
          │                         │
          │                         │
          │                         │
    ESTUDIANTES                  CURSOS
```

La tabla intermedia funciona como un puente.

```text
Estudiante
    ↓
Inscripción
    ↓
Curso
```

---

# 🔐 Primary Key compuesta

Supongamos que tenemos:

```text
estudiante_id = 1
curso_id = 2
```

La combinación:

```text
(1, 2)
```

es única.

Podemos tener:

```text
(1, 1)
(1, 2)
(1, 3)
```

porque son relaciones diferentes.

Pero no:

```text
(1, 2)
(1, 2)
```

porque sería la misma relación.

---

# 🛡️ Control de duplicados

La aplicación primero verifica:

```python
Inscripcion.existe(data)
```

La consulta utiliza:

```sql
WHERE estudiante_id = %(estudiante_id)s
  AND curso_id = %(curso_id)s
```

Si encuentra el registro:

```text
El estudiante ya está inscrito en este curso.
```

Además, la base de datos tiene:

```sql
PRIMARY KEY (
    estudiante_id,
    curso_id
)
```

por lo que MySQL también protege la integridad de la relación.

---

# 🔍 Consulta para visualizar todas las relaciones

La aplicación utiliza:

```sql
SELECT
    estudiantes.id_estudiante,
    estudiantes.nombre AS estudiante,
    estudiantes.email,
    cursos.id_curso,
    cursos.nombre_curso
FROM inscripciones
INNER JOIN estudiantes
    ON inscripciones.estudiante_id =
       estudiantes.id_estudiante
INNER JOIN cursos
    ON inscripciones.curso_id =
       cursos.id_curso;
```

Aquí la tabla `inscripciones` conecta:

```text
estudiantes
      ↕
inscripciones
      ↕
cursos
```

---

# 🧠 ¿Por qué usamos `INNER JOIN` para mostrar las inscripciones?

En este caso queremos mostrar solamente relaciones que realmente existen.

Si existe:

```text
inscripcion
```

entonces existe:

```text
estudiante
```

y:

```text
curso
```

Por eso:

```sql
INNER JOIN
```

es apropiado para consultar las relaciones registradas.

---

# 🧪 Prueba funcional

## 1. Ejecutar la aplicación

```bash
pipenv run python server.py
```

---

## 2. Abrir

```text
http://127.0.0.1:5000/
```

---

## 3. Seleccionar estudiante

Por ejemplo:

```text
Juan Pérez
```

---

## 4. Seleccionar curso

Por ejemplo:

```text
MERN
```

---

## 5. Inscribir

Presionar:

```text
Inscribir
```

Debería aparecer:

```text
Inscripción realizada correctamente.
```

y la relación debería aparecer en:

```text
Inscripciones registradas
```

---

# 🔎 Comprobar directamente en MySQL

Ejecutar:

```sql
USE esquema_educacion;

SELECT *
FROM inscripciones;
```

Debería aparecer:

```text
estudiante_id | curso_id
--------------|---------
1             | 1
```

También podemos verificar la relación completa:

```sql
SELECT
    estudiantes.nombre AS estudiante,
    cursos.nombre_curso AS curso
FROM inscripciones
INNER JOIN estudiantes
    ON inscripciones.estudiante_id =
       estudiantes.id_estudiante
INNER JOIN cursos
    ON inscripciones.curso_id =
       cursos.id_curso;
```

---

# 🧪 Probar una segunda inscripción

Seleccionar nuevamente:

```text
Juan Pérez
```

pero ahora:

```text
Python
```

Resultado:

```text
Juan Pérez
 ├── MERN
 └── Python
```

Esto demuestra que un estudiante puede pertenecer a varios cursos.

---

# 🧪 Probar el otro sentido de la relación

Seleccionar:

```text
Ana González
```

y:

```text
MERN
```

Ahora:

```text
MERN
 ├── Juan Pérez
 └── Ana González
```

Esto demuestra que un curso puede tener varios estudiantes.

---

# 🎯 Demostración de N:N

Después de varias inscripciones podríamos tener:

```text
Juan
 ├── MERN
 ├── Python
 └── Java

Ana
 ├── MERN
 └── Java

Carlos
 ├── Python
 └── MERN
```

La misma información puede representarse desde el punto de vista de los cursos:

```text
MERN
 ├── Juan
 ├── Ana
 └── Carlos

Python
 ├── Juan
 └── Carlos

Java
 ├── Juan
 └── Ana
```

Por eso es una relación:

```text
N : N
```

---

# ⚠️ Errores comunes

## `Cannot add or update a child row`

Puede significar que estás intentando insertar:

```text
estudiante_id
```

o:

```text
curso_id
```

que no existe en la tabla correspondiente.

Comprueba:

```sql
SELECT *
FROM estudiantes;
```

y:

```sql
SELECT *
FROM cursos;
```

---

## `Duplicate entry`

Significa que ya existe la combinación:

```text
estudiante_id + curso_id
```

Por ejemplo:

```text
(1, 2)
```

no puede registrarse nuevamente.

---

## `<select>` no envía el valor esperado

Comprueba:

```html
<select name="curso_id">
```

y:

```html
<option value="{{ curso.id_curso }}">
```

---

## `request.form["curso_id"]` genera error

El formulario debe tener exactamente:

```html
name="curso_id"
```

---

## El usuario ve el nombre pero Flask recibe un número

Eso es correcto.

Por ejemplo:

```html
<option value="3">
    Java
</option>
```

El usuario ve:

```text
Java
```

pero Flask recibe:

```text
curso_id = 3
```

---

## Se crea la inscripción pero no aparece

Revisa la consulta:

```python
Inscripcion.get_all()
```

y la consulta con:

```sql
INNER JOIN
```

También revisa:

```sql
SELECT *
FROM inscripciones;
```

---

## El estudiante o curso no existe

El controlador valida:

```python
Estudiante.get_by_id()
```

y:

```python
Curso.get_by_id()
```

antes de insertar la relación.

---

# 🧠 Flujo MVC

```text
                    NAVEGADOR
                        │
                        ▼
                  index.html
                        │
                        │ POST
                        ▼
              controllers/inscripciones.py
                        │
             ┌──────────┴──────────┐
             │                     │
             ▼                     ▼
      Estudiante.get_by_id()  Curso.get_by_id()
             │                     │
             └──────────┬──────────┘
                        │
                        ▼
              Inscripcion.existe()
                        │
                        ▼
         Inscripcion.inscribir_estudiante_en_curso()
                        │
                        ▼
              mysqlconnection.py
                        │
                        ▼
                      MySQL
                        │
                        ▼
                 inscripciones
                        │
                        ▼
                    redirect
                        │
                        ▼
                         /
```

---

# 🧩 Arquitectura del proyecto

```text
MODEL
│
├── estudiante.py
├── curso.py
└── inscripcion.py
       │
       ▼
    MySQL


VIEW
│
└── templates/index.html
       │
       ▼
     HTML


CONTROLLER
│
└── controllers/inscripciones.py
       │
       ├── request.form
       ├── render_template()
       ├── redirect()
       └── url_for()


CONFIG
│
└── mysqlconnection.py
       │
       ▼
     PyMySQL
```

---

# 🧠 Concepto central

La parte más importante de esta lección puede resumirse así:

```text
ESTUDIANTE
    │
    │ N
    ▼
INSCRIPCIONES
    ▲
    │ N
    │
 CURSO
```

La tabla:

```text
inscripciones
```

actúa como puente.

Contiene:

```text
estudiante_id
curso_id
```

y su combinación:

```text
(estudiante_id, curso_id)
```

identifica una relación única.

---

# 📚 Resumen

| Elemento | Función |
|---|---|
| `estudiantes` | Información de los estudiantes |
| `cursos` | Información de los cursos |
| `inscripciones` | Relación entre estudiantes y cursos |
| `estudiante_id` | FK hacia estudiantes |
| `curso_id` | FK hacia cursos |
| PK compuesta | Evita relaciones duplicadas |
| `<select>` | Permite seleccionar entidades |
| `request.form` | Recupera los IDs enviados |
| `INSERT` | Crea la relación |
| `INNER JOIN` | Permite consultar las relaciones |

---

# ✅ Checklist

```text
[ ] Pipenv configurado
[ ] Flask instalado
[ ] PyMySQL instalado

[ ] Base de datos creada
[ ] Tabla estudiantes creada
[ ] Tabla cursos creada
[ ] Tabla inscripciones creada

[ ] PRIMARY KEY compuesta creada
[ ] FOREIGN KEY estudiante creada
[ ] FOREIGN KEY curso creada

[ ] Estudiantes de prueba insertados
[ ] Cursos de prueba insertados
[ ] ERD almacenado en resources/

[ ] Modelo Estudiante funciona
[ ] Modelo Curso funciona
[ ] Modelo Inscripcion funciona

[ ] Formulario funciona
[ ] Select de estudiantes funciona
[ ] Select de cursos funciona
[ ] request.form funciona

[ ] Inscripción funciona
[ ] Validación de estudiante funciona
[ ] Validación de curso funciona
[ ] Duplicados controlados
[ ] redirect() funciona
[ ] url_for() funciona
[ ] Relaciones aparecen en pantalla
[ ] Relaciones comprobables en MySQL
```

---

# 🏁 Resultado final

Al finalizar la actividad tendrás una aplicación donde:

```text
                   ESTUDIANTES
                        N
                        │
                        │
                        ▼
                ┌──────────────┐
                │ INSCRIPCIONES│
                └──────┬───────┘
                       │
                       │
                       N
                        │
                        ▼
                      CURSOS
```

El flujo de creación será:

```text
Seleccionar estudiante
        +
Seleccionar curso
        ↓
POST /inscribir
        ↓
request.form
        ↓
{
    estudiante_id,
    curso_id
}
        ↓
validar
        ↓
INSERT INTO inscripciones
        ↓
MySQL
        ↓
redirect()
        ↓
GET /
```

La idea fundamental es:

> **En una relación muchos a muchos no duplicamos las entidades. Creamos una tabla intermedia que almacena las relaciones entre ellas.**

En este proyecto:

```text
estudiantes
      ↕
inscripciones
      ↕
cursos
```

y esto permite que:

```text
un estudiante tenga muchos cursos
```

y:

```text
un curso tenga muchos estudiantes.
```
Mostrando README.md