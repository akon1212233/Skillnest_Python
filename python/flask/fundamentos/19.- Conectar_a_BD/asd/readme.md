
README.md
Página
1
de
1
100%
# 🧩 MVC y Modularización de una aplicación Flask

> **Proyecto:** `proyecto_tacos_mod`  
> **Tema:** Arquitectura MVC y modularización  
> **Tecnologías:** Python · Flask · MySQL · PyMySQL · Jinja2 · Pipenv · Bootstrap

---

# 🎯 Objetivo

En las lecciones anteriores construimos una aplicación Flask capaz de:

- crear tacos;
- listar tacos;
- consultar un taco;
- editar un taco;
- actualizar un taco;
- eliminar un taco;
- conectarse a MySQL;
- trabajar con POO;
- utilizar sentencias preparadas;
- utilizar formularios `POST`;
- utilizar `redirect()`;
- utilizar `url_for()`.

Hasta ahora, sin embargo, gran parte de la aplicación se encuentra concentrada en pocos archivos.

En esta lección transformaremos el proyecto utilizando el patrón **MVC**:

```text
M → Model
V → View
C → Controller
```

El resultado final será una aplicación organizada, modular y más fácil de mantener.

---

# 🧠 ¿Qué problema queremos solucionar?

La aplicación original funciona, pero concentra demasiadas responsabilidades.

Actualmente tenemos:

```text
proyecto_tacos/
│
├── server.py
├── taco.py
├── mysqlconnection.py
│
└── templates/
```

Y `server.py` contiene:

- creación de Flask;
- rutas;
- recepción de formularios;
- llamadas al modelo;
- renderización;
- redirecciones.

Cuando el proyecto crece, esto comienza a ser difícil de mantener.

La idea de MVC es separar estas responsabilidades.

---

# 🏗️ ¿Qué significa MVC?

MVC significa:

```text
Model
View
Controller
```

En español:

```text
Modelo
Vista
Controlador
```

Cada parte tiene una responsabilidad diferente.

---

# 🗄️ Model — Modelo

El modelo se encarga de trabajar con los datos.

En nuestra aplicación:

```text
Taco
```

será el modelo.

El modelo:

- representa un taco;
- consulta MySQL;
- inserta registros;
- actualiza registros;
- elimina registros;
- transforma resultados en objetos.

Ejemplo:

```python
Taco.get_all()
```

```python
Taco.get_one(datos)
```

```python
Taco.save(datos)
```

```python
Taco.update(datos)
```

```python
Taco.delete(datos)
```

---

# 👁️ View — Vista

La vista corresponde a lo que el usuario visualiza.

En Flask utilizamos:

```text
HTML
+
Jinja2
```

Nuestras vistas serán:

```text
index.html
resultados.html
detalle.html
editar.html
```

La vista:

- presenta información;
- muestra formularios;
- utiliza Jinja2;
- genera enlaces;
- permite interactuar con la aplicación.

La vista **no debe realizar consultas SQL**.

---

# 🎮 Controller — Controlador

El controlador recibe las solicitudes del navegador y coordina el resto de componentes.

En nuestra aplicación será:

```text
controllers/tacos.py
```

El controlador:

- recibe solicitudes;
- obtiene datos de `request.form`;
- llama al modelo;
- decide qué plantilla mostrar;
- utiliza `redirect()`.

La lógica de base de datos no debería vivir en el controlador.

---

# 🔄 Flujo MVC

Por ejemplo, cuando el usuario solicita todos los tacos:

```text
NAVEGADOR
    │
    │ GET /tacos
    ▼
CONTROLLER
tacos.py
    │
    │ Taco.get_all()
    ▼
MODEL
taco.py
    │
    ▼
MySQLConnection
    │
    ▼
MYSQL
    │
    ▼
resultado
    │
    ▼
MODEL
    │
    ▼
CONTROLLER
    │
    │ render_template()
    ▼
VIEW
resultados.html
    │
    ▼
NAVEGADOR
```

---

# 📦 ¿Qué significa modularizar?

Modularizar significa dividir nuestra aplicación en partes con responsabilidades específicas.

En lugar de:

```text
server.py
│
├── rutas
├── SQL
├── HTML
├── lógica
└── conexión
```

tendremos:

```text
config
    ↓
conexión

models
    ↓
datos

controllers
    ↓
rutas y coordinación

templates
    ↓
interfaz

server.py
    ↓
inicio de la aplicación
```

---

# 📁 Estructura inicial del proyecto

El proyecto original es:

```text
proyecto_tacos/
│
├── server.py
├── taco.py
├── mysqlconnection.py
├── esquema_tacos.sql
├── esquema_tacos_erd.mwb
│
└── templates/
    ├── index.html
    ├── resultados.html
    ├── detalle.html
    └── editar.html
```

Esta estructura funciona.

El problema no es que esté "mal".

El problema es que, a medida que agregamos funcionalidades, resulta más difícil mantenerla.

---

# 🧱 Estructura que construiremos

La estructura final será:

```text
proyecto_tacos_mod/
│
├── flask_app/
│   │
│   ├── __init__.py
│   │
│   ├── config/
│   │   └── mysqlconnection.py
│   │
│   ├── controllers/
│   │   └── tacos.py
│   │
│   ├── models/
│   │   └── taco.py
│   │
│   └── templates/
│       ├── index.html
│       ├── resultados.html
│       ├── detalle.html
│       └── editar.html
│
├── esquema_tacos.sql
├── esquema_tacos_erd.mwb
├── Pipfile
├── Pipfile.lock
└── server.py
```

> `Pipfile.lock` será generado automáticamente por Pipenv. No debemos escribirlo manualmente.

---

# 🐍 Pipenv

El proyecto utilizará Pipenv para administrar el entorno virtual y las dependencias.

Desde la carpeta del proyecto:

```bash
pipenv install flask
```

y:

```bash
pipenv install pymysql
```

Para activar el entorno:

```bash
pipenv shell
```

También podremos ejecutar directamente:

```bash
pipenv run python server.py
```

---

# 📄 `Pipfile`

Después de instalar las dependencias tendremos un archivo equivalente a:

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

Las versiones exactas pueden variar según la instalación.

---

# 🗃️ Base de datos

Utilizaremos el esquema:

```text
esquema_tacos
```

y la tabla:

```text
tacos
```

La estructura real es:

```text
tacos
│
├── id
├── tortilla
├── guiso
├── salsa
├── created_at
└── updated_at
```

---

# 📄 `esquema_tacos.sql`

El archivo SQL completo queda:

```sql
-- ==========================================================
-- ESQUEMA DE BASE DE DATOS
-- ==========================================================

CREATE SCHEMA IF NOT EXISTS
    `esquema_tacos`
    DEFAULT CHARACTER SET utf8;


USE `esquema_tacos`;


-- ==========================================================
-- TABLA TACOS
-- ==========================================================

CREATE TABLE IF NOT EXISTS `tacos` (

    `id` INT NOT NULL AUTO_INCREMENT,

    `tortilla` VARCHAR(45) NULL,

    `guiso` VARCHAR(45) NULL,

    `salsa` VARCHAR(45) NULL,

    `created_at`
        DATETIME NULL
        DEFAULT CURRENT_TIMESTAMP,

    `updated_at`
        DATETIME NULL
        DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (`id`)

) ENGINE = InnoDB;
```

---

# 🔍 Comprobación del esquema

Podemos comprobar la estructura utilizando:

```sql
USE esquema_tacos;

DESCRIBE tacos;
```

Y consultar los registros:

```sql
SELECT *
FROM tacos;
```

---

# 📦 PARTE 1 — Crear `flask_app`

Dentro del proyecto crearemos:

```text
flask_app/
```

Esta carpeta contendrá nuestra aplicación Flask.

La estructura inicial será:

```text
proyecto_tacos_mod/
│
├── flask_app/
│
└── server.py
```

---

# 📄 `flask_app/__init__.py`

Este archivo será responsable de crear la aplicación Flask.

```python
# ==========================================================
# INICIALIZACIÓN DE LA APLICACIÓN FLASK
# ==========================================================

from flask import Flask


# ==========================================================
# CREAR INSTANCIA DE FLASK
# ==========================================================

app = Flask(__name__)


# ==========================================================
# SECRET KEY
# ==========================================================
#
# Necesaria para funcionalidades como:
#
# - session
# - flash
#
# Aunque actualmente no necesitamos ambas obligatoriamente,
# dejamos la configuración preparada para la aplicación.
#
# En un proyecto real esta clave debería mantenerse fuera
# del código utilizando variables de entorno.
# ==========================================================

app.secret_key = "clave-secreta-desarrollo"
```

---

# 🧠 ¿Qué hace `Flask(__name__)`?

Antes teníamos:

```python
app = Flask(__name__)
```

directamente en:

```text
server.py
```

Ahora esa responsabilidad pasa a:

```text
flask_app/__init__.py
```

Por lo tanto:

```text
__init__.py
    ↓
crea app
```

y:

```text
server.py
    ↓
utiliza app
```

---

# 📄 `server.py`

Ahora `server.py` será mucho más pequeño.

```python
# ==========================================================
# PUNTO DE ENTRADA DE LA APLICACIÓN
# ==========================================================


from flask_app import app


# ==========================================================
# IMPORTAR CONTROLADORES
# ==========================================================
#
# Aunque no utilizamos directamente la variable "tacos",
# esta importación ejecuta el módulo y registra sus rutas
# utilizando la instancia "app".
# ==========================================================

from flask_app.controllers import tacos


# ==========================================================
# EJECUTAR SERVIDOR
# ==========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )
```

---

# 🧠 ¿Por qué `server.py` casi no tiene código?

Antes:

```text
server.py
│
├── app
├── rutas
├── request
├── consultas
├── render_template
└── redirect
```

Ahora:

```text
server.py
│
├── importar app
├── importar controladores
└── ejecutar app
```

Su responsabilidad es únicamente iniciar la aplicación.

---

# 🚦 PARTE 2 — Crear `config`

Ahora separaremos la configuración y conexión con MySQL.

Crearemos:

```text
flask_app/config/
```

y moveremos:

```text
mysqlconnection.py
```

desde:

```text
proyecto_tacos/mysqlconnection.py
```

hacia:

```text
flask_app/config/mysqlconnection.py
```

---

# 📄 `flask_app/config/mysqlconnection.py`

El archivo completo será:

```python
# ==========================================================
# MYSQL CONNECTION
# ==========================================================

import pymysql.cursors


# ==========================================================
# CLASE MYSQL CONNECTION
# ==========================================================

class MySQLConnection:
    """
    Administra una conexión con MySQL.
    """

    def __init__(self, db):
        """
        Recibe el nombre de la base de datos
        y establece la conexión.
        """

        connection = pymysql.connect(

            host="localhost",

            user="root",

            password="",

            database=db,

            charset="utf8mb4",

            cursorclass=pymysql.cursors.DictCursor,

            autocommit=True

        )


        self.connection = connection


    # ======================================================
    # EJECUTAR CONSULTA
    # ======================================================

    def query_db(
        self,
        query,
        data=None
    ):
        """
        Ejecuta una consulta SQL.
        """

        with self.connection.cursor() as cursor:

            try:

                # --------------------------------------------------
                # Mostrar consulta durante el desarrollo.
                # --------------------------------------------------

                query_debug = cursor.mogrify(
                    query,
                    data
                )

                print(
                    "Running Query:",
                    query_debug
                )


                # --------------------------------------------------
                # Ejecutar consulta.
                # --------------------------------------------------

                cursor.execute(
                    query,
                    data
                )


                # --------------------------------------------------
                # INSERT
                # --------------------------------------------------

                if query.lower().find("insert") >= 0:

                    self.connection.commit()

                    return cursor.lastrowid


                # --------------------------------------------------
                # SELECT
                # --------------------------------------------------

                elif query.lower().find("select") >= 0:

                    result = cursor.fetchall()

                    return result


                # --------------------------------------------------
                # UPDATE / DELETE
                # --------------------------------------------------

                else:

                    self.connection.commit()


            except Exception as e:

                print(
                    "Something went wrong:",
                    e
                )

                return False


            finally:

                # --------------------------------------------------
                # Cerrar conexión.
                # --------------------------------------------------

                self.connection.close()


# ==========================================================
# FUNCIÓN AUXILIAR
# ==========================================================

def connectToMySQL(db):
    """
    Recibe el nombre de una base de datos
    y devuelve una instancia de MySQLConnection.
    """

    return MySQLConnection(db)
```

---

# 🧠 ¿Por qué está en `config`?

Porque la conexión con MySQL es una configuración/componente de infraestructura de la aplicación.

No pertenece:

- al HTML;
- al controlador;
- al modelo específicamente.

El modelo utilizará la conexión, pero no necesita conocer todos sus detalles.

La relación será:

```text
MODEL
  ↓
connectToMySQL()
  ↓
CONFIG
  ↓
MYSQL
```

---

# 🎮 PARTE 3 — Crear `controllers`

Ahora separaremos las rutas.

Crear:

```text
flask_app/controllers/
```

Dentro:

```text
tacos.py
```

---

# 📄 `flask_app/controllers/tacos.py`

Aquí estarán todas las rutas de la aplicación.

```python
# ==========================================================
# CONTROLADOR DE TACOS
# ==========================================================

from flask_app import app


from flask import (
    render_template,
    redirect,
    request,
    url_for
)


from flask_app.models.taco import Taco


# ==========================================================
# INICIO
# ==========================================================

@app.route("/")
def index():
    """
    Muestra el formulario principal para crear un taco.
    """

    return render_template(
        "index.html"
    )


# ==========================================================
# CREATE
# CREAR TACO
# ==========================================================

@app.route(
    "/crear",
    methods=["POST"]
)
def crear():
    """
    Recibe el formulario y crea un taco.
    """

    datos = {

        "tortilla": request.form["tortilla"],

        "guiso": request.form["guiso"],

        "salsa": request.form["salsa"]

    }


    Taco.save(
        datos
    )


    return redirect(
        url_for("tacos")
    )


# ==========================================================
# READ
# LISTAR TACOS
# ==========================================================

@app.route("/tacos")
def tacos():
    """
    Recupera todos los tacos
    y los envía a la vista.
    """

    todos_los_tacos = Taco.get_all()


    return render_template(
        "resultados.html",
        todos_tacos=todos_los_tacos
    )


# ==========================================================
# READ
# VER DETALLE
# ==========================================================

@app.route(
    "/mostrar/<int:taco_id>"
)
def detalle(taco_id):
    """
    Recupera un taco específico.
    """

    datos = {
        "id": taco_id
    }


    taco = Taco.get_one(
        datos
    )


    if taco is None:

        return (
            "Taco no encontrado",
            404
        )


    return render_template(
        "detalle.html",
        taco=taco
    )


# ==========================================================
# UPDATE
# MOSTRAR FORMULARIO
# ==========================================================

@app.route(
    "/editar/<int:taco_id>"
)
def editar(taco_id):
    """
    Recupera un taco y muestra
    el formulario de edición.
    """

    datos = {
        "id": taco_id
    }


    taco = Taco.get_one(
        datos
    )


    if taco is None:

        return (
            "Taco no encontrado",
            404
        )


    return render_template(
        "editar.html",
        taco=taco
    )


# ==========================================================
# UPDATE
# PROCESAR EDICIÓN
# ==========================================================

@app.route(
    "/actualizar/<int:taco_id>",
    methods=["POST"]
)
def actualizar(taco_id):
    """
    Actualiza la información del taco.
    """

    datos = {

        "id": taco_id,

        "tortilla": request.form["tortilla"],

        "guiso": request.form["guiso"],

        "salsa": request.form["salsa"]

    }


    Taco.update(
        datos
    )


    return redirect(
        url_for(
            "detalle",
            taco_id=taco_id
        )
    )


# ==========================================================
# DELETE
# ELIMINAR TACO
# ==========================================================

@app.route(
    "/borrar/<int:taco_id>"
)
def borrar(taco_id):
    """
    Elimina un taco.
    """

    datos = {
        "id": taco_id
    }


    Taco.delete(
        datos
    )


    return redirect(
        url_for("tacos")
    )
```

---

# 🧠 ¿Qué cambió?

Las rutas anteriormente estaban en:

```text
server.py
```

Ahora están en:

```text
flask_app/controllers/tacos.py
```

Por ejemplo:

```python
@app.route("/tacos")
def tacos():
```

sigue siendo una ruta Flask.

La diferencia es que ahora está organizada dentro del Controller.

---

# 🔄 Responsabilidad del Controller

El controlador:

```text
RECIBE
  ↓
PROCESA MÍNIMAMENTE
  ↓
LLAMA AL MODELO
  ↓
RENDERIZA O REDIRECCIONA
```

No contiene consultas SQL.

---

# 🗄️ PARTE 4 — Crear `models`

Ahora moveremos el modelo.

Crear:

```text
flask_app/models/
```

y mover:

```text
taco.py
```

a:

```text
flask_app/models/taco.py
```

---

# 📄 `flask_app/models/taco.py`

El archivo completo será:

```python
# ==========================================================
# MODELO TACO
# ==========================================================

from flask_app.config.mysqlconnection import connectToMySQL


# ==========================================================
# CLASE TACO
# ==========================================================

class Taco:

    def __init__(
        self,
        data
    ):
        """
        Convierte un registro de MySQL
        en un objeto Taco.
        """

        self.id = data["id"]

        self.tortilla = data["tortilla"]

        self.guiso = data["guiso"]

        self.salsa = data["salsa"]

        self.created_at = data["created_at"]

        self.updated_at = data["updated_at"]


    # ======================================================
    # CREATE
    # ======================================================

    @classmethod
    def save(
        cls,
        datos
    ):
        """
        Crea un nuevo taco.
        """

        query = """
            INSERT INTO tacos
            (
                tortilla,
                guiso,
                salsa
            )
            VALUES
            (
                %(tortilla)s,
                %(guiso)s,
                %(salsa)s
            );
        """


        return connectToMySQL(
            "esquema_tacos"
        ).query_db(
            query,
            datos
        )


    # ======================================================
    # READ
    # OBTENER TODOS
    # ======================================================

    @classmethod
    def get_all(cls):
        """
        Recupera todos los tacos.
        """

        query = """
            SELECT
                id,
                tortilla,
                guiso,
                salsa,
                created_at,
                updated_at
            FROM tacos
            ORDER BY id;
        """


        tacos_en_bd = connectToMySQL(
            "esquema_tacos"
        ).query_db(
            query
        )


        tacos = []


        for taco in tacos_en_bd:

            tacos.append(
                cls(taco)
            )


        return tacos


    # ======================================================
    # READ
    # OBTENER UNO
    # ======================================================

    @classmethod
    def get_one(
        cls,
        datos
    ):
        """
        Recupera un taco mediante su ID.
        """

        query = """
            SELECT
                id,
                tortilla,
                guiso,
                salsa,
                created_at,
                updated_at
            FROM tacos
            WHERE id = %(id)s;
        """


        taco_en_db = connectToMySQL(
            "esquema_tacos"
        ).query_db(
            query,
            datos
        )


        if not taco_en_db:

            return None


        return cls(
            taco_en_db[0]
        )


    # ======================================================
    # UPDATE
    # ======================================================

    @classmethod
    def update(
        cls,
        datos
    ):
        """
        Actualiza un taco existente.
        """

        query = """
            UPDATE tacos
            SET
                tortilla = %(tortilla)s,
                guiso = %(guiso)s,
                salsa = %(salsa)s
            WHERE id = %(id)s;
        """


        return connectToMySQL(
            "esquema_tacos"
        ).query_db(
            query,
            datos
        )


    # ======================================================
    # DELETE
    # ======================================================

    @classmethod
    def delete(
        cls,
        datos
    ):
        """
        Elimina un taco mediante su ID.
        """

        query = """
            DELETE FROM tacos
            WHERE id = %(id)s;
        """


        return connectToMySQL(
            "esquema_tacos"
        ).query_db(
            query,
            datos
        )
```

---

# 🧠 ¿Qué cambió en el modelo?

La lógica SQL sigue perteneciendo a:

```text
Taco
```

pero ahora el modelo importa la conexión desde:

```python
from flask_app.config.mysqlconnection import connectToMySQL
```

Antes teníamos:

```python
from mysqlconnection import connectToMySQL
```

Ahora:

```text
flask_app
  ↓
config
  ↓
mysqlconnection
```

Esto refleja la nueva arquitectura.

---

# 👁️ PARTE 5 — Mover las vistas

Ahora moveremos:

```text
templates/
```

desde la raíz:

```text
proyecto_tacos/templates/
```

hacia:

```text
proyecto_tacos/flask_app/templates/
```

La estructura será:

```text
flask_app/
└── templates/
    ├── index.html
    ├── resultados.html
    ├── detalle.html
    └── editar.html
```

---

# 📄 `flask_app/templates/index.html`

Esta vista mantiene el formulario de creación.

```html
<!DOCTYPE html>
<html lang="es">

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>Formulario de Taco</title>


    <link
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css"
        rel="stylesheet"
    >

</head>

<body>

<div class="container py-5">


    <!-- ==================================================
         NAVEGACIÓN
    =================================================== -->

    <div class="mb-4">

        <a
            href="{{ url_for('tacos') }}"
            class="btn btn-success"
        >

            Ver todos los tacos

        </a>

    </div>


    <!-- ==================================================
         FORMULARIO
    =================================================== -->

    <form
        action="{{ url_for('crear') }}"
        method="POST"
        class="p-4 col-12 col-md-6 mx-auto border rounded shadow-sm"
    >

        <h2 class="text-center text-primary mb-4">

            Crear Taco

        </h2>


        <!-- TORTILLA -->

        <div class="mb-3">

            <label
                for="tortilla"
                class="form-label"
            >

                Tortilla:

            </label>


            <input
                type="text"
                name="tortilla"
                id="tortilla"
                class="form-control"
                required
            >

        </div>


        <!-- GUISO -->

        <div class="mb-3">

            <label
                for="guiso"
                class="form-label"
            >

                Guiso:

            </label>


            <input
                type="text"
                name="guiso"
                id="guiso"
                class="form-control"
                required
            >

        </div>


        <!-- SALSA -->

        <div class="mb-3">

            <label
                for="salsa"
                class="form-label"
            >

                Salsa:

            </label>


            <input
                type="text"
                name="salsa"
                id="salsa"
                class="form-control"
                required
            >

        </div>


        <!-- BOTÓN -->

        <button
            type="submit"
            class="btn btn-primary"
        >

            Crear taco

        </button>


    </form>


</div>

</body>

</html>
```

---

# 📄 `flask_app/templates/resultados.html`

```html
<!DOCTYPE html>
<html lang="es">

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>Tacos</title>


    <link
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css"
        rel="stylesheet"
    >

</head>

<body>

<div class="container py-5">


    <!-- ==================================================
         NAVEGACIÓN
    =================================================== -->

    <div class="mb-4">

        <a
            href="{{ url_for('index') }}"
            class="btn btn-info"
        >

            Inicio

        </a>

    </div>


    <h1 class="mb-4">

        Todos los tacos

    </h1>


    <!-- ==================================================
         TACOS
    =================================================== -->

    <div class="row g-4">


        {% for taco in todos_tacos %}


            <div class="col-12 col-md-6 col-lg-4">


                <div class="card h-100 shadow-sm">


                    <div class="card-body">


                        <h2 class="card-title text-primary">

                            Taco {{ taco.id }}

                        </h2>


                        <p>

                            <strong>Tortilla:</strong>

                            {{ taco.tortilla }}

                            <br>

                            <strong>Guiso:</strong>

                            {{ taco.guiso }}

                            <br>

                            <strong>Salsa:</strong>

                            {{ taco.salsa }}

                        </p>


                        <a
                            href="{{ url_for('detalle', taco_id=taco.id) }}"
                            class="btn btn-primary"
                        >

                            Ver taco

                        </a>


                    </div>


                    <div class="card-footer">

                        <small>

                            Fecha de creación:

                            {{ taco.created_at.strftime(
                                "%Y-%m-%d %H:%M:%S"
                            ) }}

                        </small>

                    </div>


                </div>


            </div>


        {% endfor %}


    </div>


</div>

</body>

</html>
```

---

# 📄 `flask_app/templates/detalle.html`

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
        Detalle del taco
    </title>


    <link
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css"
        rel="stylesheet"
    >

</head>

<body>

<div class="container py-5">


    <!-- ==================================================
         NAVEGACIÓN
    =================================================== -->

    <div class="mb-4">

        <a
            href="{{ url_for('index') }}"
            class="btn btn-info"
        >

            Inicio

        </a>


        <a
            href="{{ url_for('tacos') }}"
            class="btn btn-secondary"
        >

            Todos los tacos

        </a>

    </div>


    <!-- ==================================================
         DETALLE
    =================================================== -->

    <div class="card shadow-sm col-12 col-md-6 mx-auto">

        <div class="card-body">

            <h2 class="card-title text-primary">

                Taco {{ taco.id }}

            </h2>


            <p>

                <strong>Tortilla:</strong>

                {{ taco.tortilla }}

            </p>


            <p>

                <strong>Guiso:</strong>

                {{ taco.guiso }}

            </p>


            <p>

                <strong>Salsa:</strong>

                {{ taco.salsa }}

            </p>


        </div>


        <div class="card-footer">

            <p>

                <strong>
                    Fecha de creación:
                </strong>

                {{ taco.created_at.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ) }}

            </p>


            <div class="d-flex gap-2">


                <a
                    href="{{ url_for('editar', taco_id=taco.id) }}"
                    class="btn btn-warning"
                >

                    Editar

                </a>


                <a
                    href="{{ url_for('borrar', taco_id=taco.id) }}"
                    class="btn btn-danger"
                    onclick="return confirm(
                        '¿Estás seguro de eliminar este taco?'
                    );"
                >

                    Borrar

                </a>


            </div>

        </div>

    </div>


</div>

</body>

</html>
```

---

# 📄 `flask_app/templates/editar.html`

En la versión original existían:

```text
complemento_1
complemento_2
```

pero esos campos **no existen en la tabla `tacos`**.

Por eso deben eliminarse.

La plantilla correcta es:

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
        Editar Taco
    </title>


    <link
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css"
        rel="stylesheet"
    >

</head>

<body>

<div class="container py-5">


    <form
        action="{{ url_for(
            'actualizar',
            taco_id=taco.id
        ) }}"
        method="POST"
        class="p-4 col-12 col-md-6 mx-auto border rounded shadow-sm"
    >


        <h2 class="text-center text-primary mb-4">

            Editar taco {{ taco.id }}

        </h2>


        <!-- ==================================================
             TORTILLA
        =================================================== -->

        <div class="mb-3">

            <label
                for="tortilla"
                class="form-label"
            >

                Tortilla:

            </label>


            <input
                type="text"
                name="tortilla"
                id="tortilla"
                class="form-control"
                value="{{ taco.tortilla }}"
                required
            >

        </div>


        <!-- ==================================================
             GUISO
        =================================================== -->

        <div class="mb-3">

            <label
                for="guiso"
                class="form-label"
            >

                Guiso:

            </label>


            <input
                type="text"
                name="guiso"
                id="guiso"
                class="form-control"
                value="{{ taco.guiso }}"
                required
            >

        </div>


        <!-- ==================================================
             SALSA
        =================================================== -->

        <div class="mb-4">

            <label
                for="salsa"
                class="form-label"
            >

                Salsa:

            </label>


            <input
                type="text"
                name="salsa"
                id="salsa"
                class="form-control"
                value="{{ taco.salsa }}"
                required
            >

        </div>


        <!-- ==================================================
             BOTONES
        =================================================== -->

        <div class="d-flex gap-2">


            <button
                type="submit"
                class="btn btn-primary"
            >

                Actualizar Taco

            </button>


            <a
                href="{{ url_for(
                    'detalle',
                    taco_id=taco.id
                ) }}"
                class="btn btn-secondary"
            >

                Cancelar

            </a>


        </div>


    </form>


</div>

</body>

</html>
```

---

# 🧠 ¿Qué corregimos en `editar.html`?

La versión original tenía:

```jinja
{{ taco['complemento_1'] }}
```

y:

```jinja
{{ taco['complemento_2'] }}
```

Pero la tabla real únicamente tiene:

```text
id
tortilla
guiso
salsa
created_at
updated_at
```

Por lo tanto, esos campos provocarían errores o información inexistente.

Ahora el formulario trabaja únicamente con:

```text
tortilla
guiso
salsa
```

Esto es un ejemplo muy importante de una regla fundamental:

> **La vista debe trabajar con datos que realmente existen en el modelo y en la base de datos.**

---

# 🧩 PARTE 6 — ¿Qué pasó con `server.py`?

Antes:

```text
server.py
│
├── Flask
├── rutas
├── request
├── render_template
├── redirect
└── lógica
```

Ahora:

```text
server.py
│
└── inicia aplicación
```

Las rutas viven en:

```text
flask_app/controllers/tacos.py
```

---

# 🧩 ¿Qué pasó con `taco.py`?

Antes:

```text
proyecto_tacos/taco.py
```

Ahora:

```text
flask_app/models/taco.py
```

El modelo contiene las operaciones:

```text
save()
get_all()
get_one()
update()
delete()
```

---

# 🧩 ¿Qué pasó con `mysqlconnection.py`?

Antes:

```text
proyecto_tacos/mysqlconnection.py
```

Ahora:

```text
flask_app/config/mysqlconnection.py
```

---

# 🧩 ¿Qué pasó con `templates/`?

Antes:

```text
proyecto_tacos/templates/
```

Ahora:

```text
flask_app/templates/
```

---

# 🏗️ Estructura final

```text
proyecto_tacos_mod/
│
├── flask_app/
│   │
│   ├── __init__.py
│   │
│   ├── config/
│   │   └── mysqlconnection.py
│   │
│   ├── controllers/
│   │   └── tacos.py
│   │
│   ├── models/
│   │   └── taco.py
│   │
│   └── templates/
│       ├── index.html
│       ├── resultados.html
│       ├── detalle.html
│       └── editar.html
│
├── esquema_tacos.sql
├── esquema_tacos_erd.mwb
├── Pipfile
├── Pipfile.lock
└── server.py
```

---

# 🔄 MVC en nuestra aplicación

## Model

```text
flask_app/models/taco.py
```

Responsable de:

```text
CREATE
READ
UPDATE
DELETE
```

mediante consultas SQL.

---

## View

```text
flask_app/templates/
```

Responsable de:

```text
HTML
Jinja2
Bootstrap
presentación
```

---

## Controller

```text
flask_app/controllers/tacos.py
```

Responsable de:

```text
rutas
request
render_template
redirect
llamadas al modelo
```

---

## Config

```text
flask_app/config/mysqlconnection.py
```

Responsable de:

```text
conexión con MySQL
```

---

# 🔄 Flujo: listar tacos

Cuando abrimos:

```text
/tacos
```

ocurre:

```text
Navegador
    ↓
GET /tacos
    ↓
controllers/tacos.py
    ↓
Taco.get_all()
    ↓
models/taco.py
    ↓
connectToMySQL()
    ↓
config/mysqlconnection.py
    ↓
MySQL
    ↓
lista de registros
    ↓
objetos Taco
    ↓
controllers/tacos.py
    ↓
resultados.html
    ↓
Navegador
```

---

# ✍️ Flujo: crear taco

```text
index.html
    ↓
form
    ↓
POST /crear
    ↓
controllers/tacos.py
    ↓
request.form
    ↓
Taco.save(datos)
    ↓
models/taco.py
    ↓
INSERT
    ↓
MySQL
    ↓
redirect()
    ↓
/tacos
```

---

# ✏️ Flujo: editar taco

```text
/editar/3
    ↓
Controller
    ↓
Taco.get_one()
    ↓
Model
    ↓
MySQL
    ↓
editar.html
    ↓
formulario
    ↓
POST /actualizar/3
    ↓
Taco.update()
    ↓
UPDATE
    ↓
MySQL
    ↓
redirect()
```

---

# 🗑️ Flujo: eliminar taco

```text
/borrar/3
    ↓
Controller
    ↓
Taco.delete()
    ↓
Model
    ↓
DELETE
    ↓
MySQL
    ↓
redirect()
    ↓
/tacos
```

---

# 🧠 Una regla muy importante

En MVC:

```text
Controller
→ coordina

Model
→ trabaja con datos

View
→ muestra datos

Config
→ administra conexión
```

No debemos mezclar responsabilidades.

---

# ❌ ¿Qué NO debería hacer el Controller?

No deberíamos escribir:

```python
@app.route("/tacos")
def tacos():

    query = """
        SELECT *
        FROM tacos;
    """

    resultados = ...

```

Eso pertenece al modelo.

El controlador debe hacer:

```python
tacos = Taco.get_all()
```

y luego:

```python
return render_template(...)
```

---

# ❌ ¿Qué NO debería hacer la View?

No debemos colocar SQL dentro de:

```text
HTML
```

Incorrecto:

```html
SELECT * FROM tacos;
```

La vista solamente recibe:

```jinja
{{ taco.nombre }}
```

---

# ❌ ¿Qué NO debería hacer el Model?

El modelo no debería hacer:

```python
render_template()
```

ni decidir qué HTML mostrar.

Su responsabilidad son los datos.

---

# 🧪 Comprobación del proyecto

Desde la raíz:

```text
proyecto_tacos_mod/
```

ejecutar:

```bash
pipenv run python server.py
```

Flask debería iniciar el servidor.

Abrir:

```text
http://127.0.0.1:5000/
```

---

# 🧪 Probar CREATE

En:

```text
/
```

completar:

```text
Tortilla: Maíz
Guiso: Carne
Salsa: Verde
```

Presionar:

```text
Crear taco
```

Deberíamos ser redirigidos a:

```text
/tacos
```

---

# 🧪 Probar READ

Abrir:

```text
/tacos
```

Deberán aparecer los tacos existentes.

Seleccionar:

```text
Ver taco
```

---

# 🧪 Probar UPDATE

Desde el detalle:

```text
Editar
```

Modificar:

```text
Tortilla
Guiso
Salsa
```

Enviar:

```text
Actualizar Taco
```

La aplicación debe volver al detalle.

---

# 🧪 Probar DELETE

Desde el detalle:

```text
Borrar
```

Debe aparecer:

```text
¿Estás seguro de eliminar este taco?
```

Aceptar.

El sistema debe:

```text
DELETE
   ↓
redirect()
   ↓
/tacos
```

---

# 🐞 Errores comunes durante la modularización

## `ModuleNotFoundError`

Por ejemplo:

```text
No module named 'flask_app'
```

Comprueba que estás ejecutando:

```bash
pipenv run python server.py
```

desde la raíz:

```text
proyecto_tacos_mod/
```

---

# ❌ `ModuleNotFoundError: mysqlconnection`

Si aparece:

```text
No module named 'mysqlconnection'
```

revisa el modelo.

Antes:

```python
from mysqlconnection import connectToMySQL
```

Ahora:

```python
from flask_app.config.mysqlconnection import connectToMySQL
```

---

# ❌ Error importando `Taco`

En el controlador debe ser:

```python
from flask_app.models.taco import Taco
```

No:

```python
from taco import Taco
```

---

# ❌ Template no encontrado

Si aparece:

```text
TemplateNotFound
```

comprueba que:

```text
templates/
```

esté dentro de:

```text
flask_app/
```

La estructura debe ser:

```text
flask_app/
└── templates/
    ├── index.html
    ├── resultados.html
    ├── detalle.html
    └── editar.html
```

---

# ❌ Las rutas no funcionan

Si las rutas no están registradas, comprueba que `server.py` tenga:

```python
from flask_app.controllers import tacos
```

Esta importación es importante porque carga el controlador y registra las rutas.

---

# 🧠 ¿Por qué importar `tacos` si no usamos la variable?

Esta línea:

```python
from flask_app.controllers import tacos
```

ejecuta el módulo:

```text
flask_app/controllers/tacos.py
```

Durante su carga se ejecutan:

```python
@app.route(...)
```

y Flask registra las rutas.

Por eso necesitamos importarlo.

---

# 🧩 `__init__.py`

Otro error frecuente es olvidar:

```text
__init__.py
```

dentro de:

```text
flask_app/
```

Debe existir:

```text
flask_app/
└── __init__.py
```

Este archivo inicializa el paquete y crea:

```python
app = Flask(__name__)
```

---

# 🔗 `url_for()`

La modularización es una buena oportunidad para dejar de escribir rutas manualmente.

En vez de:

```html
<a href="/tacos">
```

utilizamos:

```jinja
<a href="{{ url_for('tacos') }}">
```

En vez de:

```html
<a href="/mostrar/3">
```

utilizamos:

```jinja
<a href="{{ url_for('detalle', taco_id=taco.id) }}">
```

Esto hace que las vistas dependan menos de URLs escritas manualmente.

---

# 📊 Antes y después

## Antes

```text
proyecto_tacos/
│
├── server.py
│
├── taco.py
│
├── mysqlconnection.py
│
└── templates/
```

Funciona, pero a medida que el proyecto crece:

```text
server.py
      ↓
muchas responsabilidades
      ↓
difícil mantenimiento
```

---

# ✅ Después

```text
proyecto_tacos_mod/
│
├── flask_app/
│   │
│   ├── config/
│   │   └── mysqlconnection.py
│   │
│   ├── controllers/
│   │   └── tacos.py
│   │
│   ├── models/
│   │   └── taco.py
│   │
│   └── templates/
│       ├── index.html
│       ├── resultados.html
│       ├── detalle.html
│       └── editar.html
│
└── server.py
```

Ahora cada parte tiene una responsabilidad clara.

---

# 🚀 ¿Por qué esta estructura es mejor para proyectos grandes?

Supongamos que mañana agregamos:

```text
usuarios
productos
pedidos
clientes
```

Con una arquitectura modular podríamos tener:

```text
controllers/
├── tacos.py
├── usuarios.py
├── productos.py
└── pedidos.py

models/
├── taco.py
├── usuario.py
├── producto.py
└── pedido.py
```

La organización permite que cada componente tenga un lugar claro.

---

# 🧠 MVC aplicado a futuros proyectos

Por ejemplo:

```text
usuarios
│
├── controllers/usuarios.py
├── models/usuario.py
└── templates/usuarios/
```

y:

```text
productos
│
├── controllers/productos.py
├── models/producto.py
└── templates/productos/
```

La estructura puede crecer sin convertir `server.py` en un archivo gigante.

---

# ✅ Checklist final

```text
[ ] Crear flask_app
[ ] Crear __init__.py
[ ] Crear la instancia Flask en __init__.py
[ ] Configurar secret_key
[ ] Simplificar server.py
[ ] Crear config
[ ] Mover mysqlconnection.py
[ ] Actualizar import de conexión
[ ] Crear controllers
[ ] Mover las rutas a tacos.py
[ ] Crear models
[ ] Mover taco.py
[ ] Actualizar import de Taco
[ ] Mover templates
[ ] Corregir enlaces con url_for()
[ ] Corregir editar.html
[ ] Eliminar campos inexistentes
[ ] Mantener CREATE funcionando
[ ] Mantener READ funcionando
[ ] Mantener UPDATE funcionando
[ ] Mantener DELETE funcionando
[ ] Probar todas las rutas
[ ] Ejecutar mediante Pipenv
```

---

# 🏁 Resultado final

La aplicación ha pasado de una estructura sencilla pero poco modular a una estructura MVC:

```text
                      FLASK
                        │
                        ▼
                   CONTROLLER
                        │
                        ▼
                     MODEL
                        │
                        ▼
                      MYSQL
                        │
                        ▼
                     MODEL
                        │
                        ▼
                   CONTROLLER
                        │
                        ▼
                      VIEW
                        │
                        ▼
                    NAVEGADOR
```

Y la estructura física del proyecto queda:

```text
proyecto_tacos_mod/
│
├── flask_app/
│   │
│   ├── __init__.py
│   │
│   ├── config/
│   │   └── mysqlconnection.py
│   │
│   ├── controllers/
│   │   └── tacos.py
│   │
│   ├── models/
│   │   └── taco.py
│   │
│   └── templates/
│       ├── index.html
│       ├── resultados.html
│       ├── detalle.html
│       └── editar.html
│
├── esquema_tacos.sql
├── esquema_tacos_erd.mwb
├── Pipfile
├── Pipfile.lock
└── server.py
```

---

# 🎓 Conclusión

La modularización no consiste simplemente en mover archivos.

Consiste en asignar una **responsabilidad clara** a cada parte de la aplicación.

```text
MODEL
→ trabaja con los datos

VIEW
→ presenta los datos

CONTROLLER
→ coordina la aplicación

CONFIG
→ administra la conexión

SERVER
→ inicia la aplicación
```

A partir de ahora, cuando una aplicación Flask crezca, la pregunta ya no será:

> "¿En qué parte de `server.py` agrego esto?"

sino:

> "¿Esta funcionalidad pertenece al modelo, al controlador, a la vista o a la configuración?"

Ese cambio de mentalidad es precisamente uno de los objetivos principales de trabajar con **MVC y modularización**.
Mostrando README.md