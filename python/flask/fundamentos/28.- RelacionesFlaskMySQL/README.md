
README.md
100%
# 🔗 Relaciones 1:N — Restaurante y Tacos con Flask + MySQL

> **Tema:** Relaciones entre clases y bases de datos  
> **Tipo de relación:** Uno a muchos (1:N)  
> **Tecnologías:** Python · Flask · MySQL · PyMySQL · Jinja2 · POO · Pipenv · MVC

---

## 🎯 Objetivo

Construir una aplicación Flask que permita comprender cómo trabajar con una relación de tipo **uno a muchos** entre dos tablas y dos clases relacionadas.

La aplicación representará la siguiente relación:

```text
1 Restaurante
      │
      │ tiene muchos
      ▼
N Tacos
```

Un restaurante puede tener muchos tacos, mientras que cada taco pertenece a un único restaurante.

Además, se aprenderá a convertir los resultados de una consulta `JOIN` en objetos Python relacionados.

---

# 📖 ¿Qué aprenderemos?

En esta actividad integraremos conocimientos anteriores y agregaremos un concepto nuevo:

```text
MySQL
  ↓
Relación entre tablas
  ↓
FOREIGN KEY
  ↓
JOIN / LEFT JOIN
  ↓
PyMySQL
  ↓
diccionarios
  ↓
objetos Python
  ↓
objetos relacionados
  ↓
Jinja2
  ↓
HTML
```

La parte central de la actividad será comprender cómo pasar de:

```text
Restaurante + Tacos
```

en la base de datos, a:

```python
restaurante.tacos
```

en Python.

---

# 🧠 Concepto: relación uno a muchos

Tenemos dos entidades:

```text
RESTaurante
Taco
```

La relación es:

```text
RESTAURANTE 1 ─────────── N TACOS
```

Por ejemplo:

```text
Tacos El Sol
     │
     ├── Taco de Carne
     ├── Taco de Pollo
     └── Taco de Carnitas
```

Un restaurante puede tener tres tacos.

Pero cada taco pertenece solamente a un restaurante.

---

# 🔑 Clave primaria y clave foránea

El restaurante tiene:

```text
restaurantes.id
```

Ese campo identifica al restaurante.

El taco tendrá:

```text
tacos.restaurante_id
```

Este campo será la **clave foránea**.

La relación será:

```text
restaurantes.id
       ▲
       │
       │ FOREIGN KEY
       │
tacos.restaurante_id
```

Por ejemplo:

```text
restaurantes

id = 1
nombre = Tacos El Sol
```

y:

```text
tacos

id = 1
restaurante_id = 1

id = 2
restaurante_id = 1

id = 3
restaurante_id = 1
```

Los tres tacos pertenecen al restaurante `1`.

---

# 🏗️ Arquitectura del proyecto

Utilizaremos la arquitectura MVC trabajada anteriormente.

```text
MODEL
VIEW
CONTROLLER
```

Además tendremos:

```text
CONFIG
```

para la conexión con MySQL.

---

# 📁 Estructura final del proyecto

```text
proyecto_tacos_relaciones/
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
│   │   └── tacos.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── taco.py
│   │   └── restaurante.py
│   │
│   ├── templates/
│   │   ├── index.html
│   │   ├── restaurantes.html
│   │   └── restaurante.html
│   │
│   └── static/
│       └── css/
│           └── style.css
│
├── resources/
│   └── esquema_tacos_erd.mwb
│
├── esquema_tacos.sql
├── server.py
├── Pipfile
└── Pipfile.lock
```

> La carpeta `resources/` debe contener siempre el **ERD utilizado para construir la base de datos**.

---

# 🐍 Entorno con Pipenv

Instalar las dependencias:

```bash
pipenv install flask pymysql
```

Entrar al entorno virtual:

```bash
pipenv shell
```

Ejecutar la aplicación:

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

> `Pipfile.lock` debe ser generado automáticamente por Pipenv.

---

# 🗄️ Base de datos

Utilizaremos:

```text
Base de datos:
esquema_tacos
```

y dos tablas:

```text
restaurantes
tacos
```

---

# 📄 `esquema_tacos.sql`

```sql
-- ==========================================================
-- CREAR BASE DE DATOS
-- ==========================================================

CREATE DATABASE IF NOT EXISTS esquema_tacos;

USE esquema_tacos;


-- ==========================================================
-- TABLA RESTAURANTES
-- ==========================================================

CREATE TABLE IF NOT EXISTS restaurantes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(45) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);


-- ==========================================================
-- TABLA TACOS
-- ==========================================================

CREATE TABLE IF NOT EXISTS tacos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tortilla VARCHAR(45),
    guiso VARCHAR(45),
    salsa VARCHAR(45),
    restaurante_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_tacos_restaurantes
        FOREIGN KEY (restaurante_id)
        REFERENCES restaurantes(id)
);


-- ==========================================================
-- RESTAURANTES DE PRUEBA
-- ==========================================================

INSERT INTO restaurantes
(nombre)
VALUES
("Tacos El Sol"),
("Tacos Central"),
("Tacos Don Pepe");


-- ==========================================================
-- TACOS DE PRUEBA
-- ==========================================================

INSERT INTO tacos
(
    tortilla,
    guiso,
    salsa,
    restaurante_id
)
VALUES
(
    "Maíz",
    "Carne",
    "Verde",
    1
),
(
    "Harina",
    "Pollo",
    "Roja",
    1
),
(
    "Maíz",
    "Carnitas",
    "Verde",
    2
),
(
    "Maíz",
    "Pastor",
    "Picante",
    2
),
(
    "Harina",
    "Barbacoa",
    "Roja",
    3
);
```

---

# 🔍 Comprobar la relación

En MySQL Workbench podemos comprobar las tablas:

```sql
USE esquema_tacos;

SELECT *
FROM restaurantes;
```

y:

```sql
SELECT *
FROM tacos;
```

También podemos revisar la relación directamente:

```sql
SELECT
    restaurantes.id AS restaurante_id,
    restaurantes.nombre AS restaurante,
    tacos.id AS taco_id,
    tacos.tortilla,
    tacos.guiso,
    tacos.salsa
FROM restaurantes
LEFT JOIN tacos
    ON tacos.restaurante_id = restaurantes.id;
```

El resultado conceptualmente será:

```text
restaurante_id | restaurante    | taco_id | tortilla | guiso
---------------|----------------|---------|----------|---------
1              | Tacos El Sol   | 1       | Maíz     | Carne
1              | Tacos El Sol   | 2       | Harina   | Pollo
2              | Tacos Central  | 3       | Maíz     | Carnitas
2              | Tacos Central  | 4       | Maíz     | Pastor
3              | Tacos Don Pepe | 5       | Harina   | Barbacoa
```

---

# 🧩 ¿Por qué aparece más de una fila por restaurante?

Porque estamos consultando una relación 1:N.

Por ejemplo:

```text
Tacos El Sol
    │
    ├── Taco 1
    └── Taco 2
```

El `JOIN` necesita una fila para cada combinación encontrada.

Por eso:

```text
Restaurante 1
```

puede aparecer varias veces.

Posteriormente Python se encargará de convertir esas filas en:

```python
Restaurante(
    ...
)
```

que contendrá:

```python
restaurante.tacos
```

con varios objetos `Taco`.

---

# 🔌 `flask_app/config/mysqlconnection.py`

```python
# ==========================================================
# CONEXIÓN CON MYSQL
# ==========================================================

import pymysql.cursors


class MySQLConnection:
    """
    Administra una conexión con MySQL.
    """

    def __init__(self, db):
        """
        Recibe el nombre de la base de datos
        y establece la conexión.
        """

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
            devuelve el número de filas afectadas.

        Si ocurre un error:
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
    Crea una instancia de MySQLConnection.
    """

    return MySQLConnection(db)
```

> Cambia `user` y `password` según tu instalación local de MySQL.

---

# 📄 `flask_app/config/__init__.py`

```python
# Archivo utilizado para identificar config como paquete Python.
```

---

# 🍴 Modelo `Taco`

Ahora adaptaremos el modelo para que conozca el restaurante al que pertenece cada taco.

---

# 📄 `flask_app/models/taco.py`

```python
# ==========================================================
# MODELO TACO
# ==========================================================

from flask_app.config.mysqlconnection import connectToMySQL


class Taco:

    def __init__(self, data):
        """
        Convierte un registro de MySQL
        en un objeto Taco.
        """

        self.id = data["id"]
        self.tortilla = data["tortilla"]
        self.guiso = data["guiso"]
        self.salsa = data["salsa"]
        self.restaurante_id = data["restaurante_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]


    # ======================================================
    # CREATE
    # ======================================================

    @classmethod
    def save(cls, datos):
        """
        Crea un nuevo taco.

        Ahora necesitamos también el ID
        del restaurante al que pertenece.
        """

        query = """
            INSERT INTO tacos
            (
                tortilla,
                guiso,
                salsa,
                restaurante_id
            )
            VALUES
            (
                %(tortilla)s,
                %(guiso)s,
                %(salsa)s,
                %(restaurante_id)s
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
                restaurante_id,
                created_at,
                updated_at
            FROM tacos
            ORDER BY id;
        """


        resultados = connectToMySQL(
            "esquema_tacos"
        ).query_db(
            query
        )


        tacos = []


        for taco in resultados:

            tacos.append(
                cls(taco)
            )


        return tacos
```

---

# 🧠 Cambio importante en `Taco`

Antes podíamos tener:

```python
self.id
self.tortilla
self.guiso
self.salsa
```

Ahora agregamos:

```python
self.restaurante_id
```

porque necesitamos conocer la relación.

Por ejemplo:

```text
Taco #4
restaurante_id = 2
```

significa:

```text
Taco #4
   ↓
Restaurante #2
```

---

# 🍽️ Modelo `Restaurante`

Ahora crearemos la clase que representará el lado "uno" de la relación.

---

# 📄 `flask_app/models/restaurante.py`

```python
# ==========================================================
# MODELO RESTAURANTE
# ==========================================================

from flask_app.config.mysqlconnection import connectToMySQL

from flask_app.models.taco import Taco


class Restaurante:

    def __init__(self, data):
        """
        Convierte un registro de MySQL
        en un objeto Restaurante.
        """

        self.id = data["id"]

        self.nombre = data["nombre"]

        self.created_at = data["created_at"]

        self.updated_at = data["updated_at"]


        # --------------------------------------------------
        # Lista donde posteriormente almacenaremos
        # los objetos Taco relacionados.
        # --------------------------------------------------

        self.tacos = []


    # ======================================================
    # CREATE
    # ======================================================

    @classmethod
    def save(cls, datos):
        """
        Crea un nuevo restaurante.
        """

        query = """
            INSERT INTO restaurantes
            (
                nombre
            )
            VALUES
            (
                %(nombre)s
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
    # OBTENER TODOS LOS RESTAURANTES
    # ======================================================

    @classmethod
    def get_all(cls):
        """
        Recupera todos los restaurantes.
        """

        query = """
            SELECT
                id,
                nombre,
                created_at,
                updated_at
            FROM restaurantes
            ORDER BY id;
        """


        resultados = connectToMySQL(
            "esquema_tacos"
        ).query_db(
            query
        )


        restaurantes = []


        for restaurante in resultados:

            restaurantes.append(
                cls(restaurante)
            )


        return restaurantes


    # ======================================================
    # READ
    # RESTAURANTE + TACOS
    # ======================================================

    @classmethod
    def get_restaurante_y_tacos(cls, datos):
        """
        Recupera un restaurante junto con
        todos los tacos relacionados.
        """

        query = """
            SELECT

                restaurantes.id
                    AS restaurante_id,

                restaurantes.nombre
                    AS restaurante_nombre,

                restaurantes.created_at
                    AS restaurante_created_at,

                restaurantes.updated_at
                    AS restaurante_updated_at,

                tacos.id
                    AS taco_id,

                tacos.tortilla
                    AS taco_tortilla,

                tacos.guiso
                    AS taco_guiso,

                tacos.salsa
                    AS taco_salsa,

                tacos.restaurante_id
                    AS taco_restaurante_id,

                tacos.created_at
                    AS taco_created_at,

                tacos.updated_at
                    AS taco_updated_at

            FROM restaurantes

            LEFT JOIN tacos
                ON tacos.restaurante_id = restaurantes.id

            WHERE restaurantes.id = %(id)s;
        """


        resultados = connectToMySQL(
            "esquema_tacos"
        ).query_db(
            query,
            datos
        )


        # --------------------------------------------------
        # Si no existe el restaurante.
        # --------------------------------------------------

        if not resultados:

            return None


        # --------------------------------------------------
        # Crear objeto Restaurante.
        # --------------------------------------------------

        restaurante_data = {

            "id": resultados[0][
                "restaurante_id"
            ],

            "nombre": resultados[0][
                "restaurante_nombre"
            ],

            "created_at": resultados[0][
                "restaurante_created_at"
            ],

            "updated_at": resultados[0][
                "restaurante_updated_at"
            ]

        }


        restaurante = cls(
            restaurante_data
        )


        # --------------------------------------------------
        # Recorrer los resultados del JOIN.
        # --------------------------------------------------

        for fila_en_db in resultados:

            # --------------------------------------------------
            # Como utilizamos LEFT JOIN, el restaurante puede
            # no tener tacos.
            #
            # En ese caso taco_id será None.
            # --------------------------------------------------

            if fila_en_db["taco_id"] is not None:

                datos_taco = {

                    "id": fila_en_db[
                        "taco_id"
                    ],

                    "tortilla": fila_en_db[
                        "taco_tortilla"
                    ],

                    "guiso": fila_en_db[
                        "taco_guiso"
                    ],

                    "salsa": fila_en_db[
                        "taco_salsa"
                    ],

                    "restaurante_id": fila_en_db[
                        "taco_restaurante_id"
                    ],

                    "created_at": fila_en_db[
                        "taco_created_at"
                    ],

                    "updated_at": fila_en_db[
                        "taco_updated_at"
                    ]

                }


                # --------------------------------------------------
                # Convertimos el diccionario en un objeto Taco
                # y lo agregamos al restaurante.
                # --------------------------------------------------

                restaurante.tacos.append(
                    Taco(datos_taco)
                )


        return restaurante
```

---

# 🧠 ¿Qué está ocurriendo aquí?

Esta es la parte central de la lección.

El SQL devuelve varias filas.

Por ejemplo:

```text
[
    {
        restaurante_id: 1,
        restaurante_nombre: "Tacos El Sol",
        taco_id: 1,
        taco_tortilla: "Maíz"
    },

    {
        restaurante_id: 1,
        restaurante_nombre: "Tacos El Sol",
        taco_id: 2,
        taco_tortilla: "Harina"
    }
]
```

No queremos terminar con dos restaurantes:

```text
Restaurante
Restaurante
```

Queremos:

```text
Restaurante
    │
    ├── Taco
    └── Taco
```

Por eso:

```python
restaurante = cls(restaurante_data)
```

se ejecuta una sola vez.

Después recorremos las filas:

```python
for fila_en_db in resultados:
```

y por cada taco creamos:

```python
Taco(datos_taco)
```

Finalmente:

```python
restaurante.tacos.append(
    Taco(datos_taco)
)
```

---

# 🧩 Resultado en Python

Después del proceso tendremos algo conceptualmente equivalente a:

```python
restaurante = Restaurante(...)
```

y:

```python
restaurante.tacos = [
    Taco(...),
    Taco(...),
    Taco(...)
]
```

Es decir:

```text
Restaurante
│
├── id
├── nombre
├── created_at
├── updated_at
│
└── tacos
    │
    ├── Taco
    ├── Taco
    └── Taco
```

---

# 🔍 ¿Qué significa "parsear"?

En este contexto, parsear significa transformar los resultados obtenidos desde MySQL en objetos Python que tengan sentido para nuestra aplicación.

Tenemos:

```text
MySQL
 ↓
diccionarios
```

y convertimos:

```text
diccionario restaurante
 ↓
objeto Restaurante
```

y:

```text
diccionario taco
 ↓
objeto Taco
```

Finalmente:

```text
Restaurante
   ↓
lista de objetos Taco
```

---

# ⚠️ ¿Por qué utilizamos alias?

Un `JOIN` puede traer campos con nombres repetidos:

```text
id
created_at
updated_at
```

Por ejemplo:

```text
restaurantes.id
tacos.id
```

Para evitar confusiones utilizamos:

```sql
restaurantes.id AS restaurante_id
```

y:

```sql
tacos.id AS taco_id
```

Lo mismo hacemos con:

```text
restaurante_nombre
taco_tortilla
taco_guiso
taco_salsa
```

De esta manera sabemos exactamente de qué tabla proviene cada dato.

---

# 🧠 ¿Por qué no utilizamos simplemente `SELECT *`?

Podríamos escribir:

```sql
SELECT *
FROM restaurantes
LEFT JOIN tacos
    ON tacos.restaurante_id = restaurantes.id;
```

Pero tendremos columnas repetidas como:

```text
id
created_at
updated_at
```

Esto puede generar ambigüedad al trabajar con diccionarios.

Por eso en esta actividad utilizamos:

```sql
AS restaurante_id
```

```sql
AS taco_id
```

etc.

Esto hace mucho más claro el resultado.

---

# 🎮 `flask_app/controllers/tacos.py`

El controlador se encargará de:

- mostrar el formulario;
- recibir el formulario;
- mostrar restaurantes;
- mostrar un restaurante con sus tacos.

```python
# ==========================================================
# CONTROLADOR DE TACOS
# ==========================================================

from flask_app import app

from flask import (
    render_template,
    request,
    redirect,
    url_for
)

from flask_app.models.taco import Taco

from flask_app.models.restaurante import Restaurante


# ==========================================================
# INICIO
# ==========================================================

@app.route("/")
def index():
    """
    Muestra el formulario para crear un taco.

    También recupera todos los restaurantes para que
    el usuario pueda seleccionar uno.
    """

    todos_restaurantes = Restaurante.get_all()


    return render_template(
        "index.html",
        todos_restaurantes=todos_restaurantes
    )


# ==========================================================
# CREATE
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

        "tortilla": request.form[
            "tortilla"
        ].strip(),

        "guiso": request.form[
            "guiso"
        ].strip(),

        "salsa": request.form[
            "salsa"
        ].strip(),

        "restaurante_id": request.form[
            "restaurante_id"
        ]

    }


    Taco.save(
        datos
    )


    return redirect(
        url_for("tacos")
    )


# ==========================================================
# READ
# LISTADO DE TACOS
# ==========================================================

@app.route("/tacos")
def tacos():
    """
    Muestra todos los tacos.
    """

    todos_los_tacos = Taco.get_all()


    return render_template(
        "index.html",
        tacos=todos_los_tacos
    )


# ==========================================================
# READ
# RESTAURANTE + TACOS
# ==========================================================

@app.route(
    "/restaurantes/<int:id>"
)
def restaurante(id):
    """
    Muestra un restaurante junto con
    todos sus tacos relacionados.
    """

    datos = {
        "id": id
    }


    restaurante = Restaurante.get_restaurante_y_tacos(
        datos
    )


    if restaurante is None:

        return (
            "Restaurante no encontrado",
            404
        )


    return render_template(
        "restaurante.html",
        restaurante=restaurante
    )


# ==========================================================
# LISTADO DE RESTAURANTES
# ==========================================================

@app.route("/restaurantes")
def restaurantes():
    """
    Muestra todos los restaurantes.
    """

    todos_restaurantes = Restaurante.get_all()


    return render_template(
        "restaurantes.html",
        restaurantes=todos_restaurantes
    )
```

---

# ⚠️ Importante sobre la ruta `/`

En el controlador anterior usamos:

```python
return redirect(
    url_for("tacos")
)
```

después de crear.

Esto funciona porque:

```python
def tacos():
```

representa la ruta:

```text
/tacos
```

La página principal:

```text
/
```

muestra el formulario.

La página:

```text
/tacos
```

muestra el listado de tacos.

---

# 📄 `flask_app/templates/index.html`

Esta vista contiene el formulario.

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
        Crear Taco
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
                Crear Taco
            </h1>

            <p class="text-muted">
                Selecciona el restaurante al que pertenece.
            </p>

        </div>


        <div>

            <a
                href="{{ url_for('tacos') }}"
                class="btn btn-outline-primary"
            >
                Ver tacos
            </a>


            <a
                href="{{ url_for('restaurantes') }}"
                class="btn btn-outline-secondary"
            >
                Restaurantes
            </a>

        </div>

    </div>


    <!-- ==================================================
         FORMULARIO
    =================================================== -->

    <div class="form-card">


        <form
            action="{{ url_for('crear') }}"
            method="POST"
        >


            <!-- TORTILLA -->

            <div class="mb-3">

                <label
                    for="tortilla"
                    class="form-label"
                >

                    Tortilla

                </label>


                <input
                    type="text"
                    id="tortilla"
                    name="tortilla"
                    class="form-control"
                    maxlength="45"
                    required
                >

            </div>


            <!-- GUISO -->

            <div class="mb-3">

                <label
                    for="guiso"
                    class="form-label"
                >

                    Guiso

                </label>


                <input
                    type="text"
                    id="guiso"
                    name="guiso"
                    class="form-control"
                    maxlength="45"
                    required
                >

            </div>


            <!-- SALSA -->

            <div class="mb-3">

                <label
                    for="salsa"
                    class="form-label"
                >

                    Salsa

                </label>


                <input
                    type="text"
                    id="salsa"
                    name="salsa"
                    class="form-control"
                    maxlength="45"
                    required
                >

            </div>


            <!-- RESTAURANTE -->

            <div class="mb-4">

                <label
                    for="restaurante_id"
                    class="form-label"
                >

                    Restaurante

                </label>


                <select
                    id="restaurante_id"
                    name="restaurante_id"
                    class="form-select"
                    required
                >

                    <option value="">
                        Selecciona un restaurante
                    </option>


                    {% for restaurante in todos_restaurantes %}

                        <option
                            value="{{ restaurante.id }}"
                        >

                            {{ restaurante.nombre }}

                        </option>

                    {% endfor %}

                </select>

            </div>


            <button
                type="submit"
                class="btn btn-primary"
            >

                Crear Taco

            </button>


        </form>


    </div>


</div>

</body>

</html>
```

---

# 🔍 El `<select>` es fundamental

Tenemos:

```html
<select
    name="restaurante_id"
>
```

Luego:

```jinja
{% for restaurante in todos_restaurantes %}
```

y cada opción:

```html
<option value="{{ restaurante.id }}">
    {{ restaurante.nombre }}
</option>
```

Supongamos:

```text
id = 2
nombre = Tacos Central
```

El navegador verá:

```text
Tacos Central
```

pero cuando el usuario seleccione esa opción, enviará:

```text
restaurante_id = 2
```

Esto es muy importante.

El usuario ve:

```text
Tacos Central
```

pero la aplicación recibe:

```text
2
```

---

# 🔄 Flujo del `<select>`

```text
Restaurante
      │
      ├── id = 1
      ├── nombre = Tacos El Sol
      │
      ▼
<option value="1">
    Tacos El Sol
</option>
```

Después:

```text
Usuario selecciona Tacos El Sol
          ↓
restaurante_id = 1
          ↓
request.form["restaurante_id"]
          ↓
datos["restaurante_id"]
          ↓
INSERT
```

---

# 📄 `flask_app/templates/restaurantes.html`

Esta página muestra todos los restaurantes.

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
        Restaurantes
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
                Restaurantes
            </h1>

            <p class="text-muted">
                Selecciona un restaurante para ver sus tacos.
            </p>

        </div>


        <a
            href="{{ url_for('index') }}"
            class="btn btn-primary"
        >

            Crear Taco

        </a>

    </div>


    {% if restaurantes %}


        <div class="row g-4">


            {% for restaurante in restaurantes %}


                <div class="col-12 col-md-6 col-lg-4">


                    <div class="card h-100 shadow-sm">


                        <div class="card-body">


                            <h2 class="h4">

                                {{ restaurante.nombre }}

                            </h2>


                            <p class="text-muted">

                                ID:
                                {{ restaurante.id }}

                            </p>


                            <a
                                href="{{ url_for(
                                    'restaurante',
                                    id=restaurante.id
                                ) }}"
                                class="btn btn-success"
                            >

                                Ver tacos

                            </a>


                        </div>


                    </div>


                </div>


            {% endfor %}


        </div>


    {% else %}


        <div class="alert alert-info">

            No existen restaurantes registrados.

        </div>


    {% endif %}


</div>

</body>

</html>
```

---

# 👁️ `flask_app/templates/restaurante.html`

Esta es la vista principal de la relación.

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
        {{ restaurante.nombre }}
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

    <div class="page-header">


        <div>

            <h1>

                {{ restaurante.nombre }}

            </h1>


            <p class="text-muted">

                Tacos pertenecientes a este restaurante.

            </p>

        </div>


        <div>

            <a
                href="{{ url_for('restaurantes') }}"
                class="btn btn-outline-secondary"
            >

                Restaurantes

            </a>


            <a
                href="{{ url_for('index') }}"
                class="btn btn-primary"
            >

                Crear Taco

            </a>

        </div>


    </div>


    <!-- ==================================================
         TACOS RELACIONADOS
    =================================================== -->

    {% if restaurante.tacos %}


        <div class="row g-4">


            {% for taco in restaurante.tacos %}


                <div class="col-12 col-md-6 col-lg-4">


                    <div class="card taco-card h-100 shadow-sm">


                        <div class="card-body">


                            <h2 class="h4">

                                Taco #{{ taco.id }}

                            </h2>


                            <p>

                                <strong>
                                    Tortilla:
                                </strong>

                                {{ taco.tortilla }}

                            </p>


                            <p>

                                <strong>
                                    Guiso:
                                </strong>

                                {{ taco.guiso }}

                            </p>


                            <p>

                                <strong>
                                    Salsa:
                                </strong>

                                {{ taco.salsa }}

                            </p>


                        </div>


                    </div>


                </div>


            {% endfor %}


        </div>


    {% else %}


        <div class="alert alert-info">

            Este restaurante todavía no tiene tacos registrados.

        </div>


    {% endif %}


</div>

</body>

</html>
```

---

# 📄 `flask_app/static/css/style.css`

```css
/* ==========================================================
   ESTILOS GENERALES
========================================================== */

body {
    background-color: #f5f6f8;
    color: #212529;
    font-family: Arial, Helvetica, sans-serif;
}


h1 {
    font-weight: 700;
}


.card,
.form-card {
    border-radius: 10px;
}


.form-card {
    max-width: 650px;
    margin: 0 auto;
    padding: 35px;
    background-color: #ffffff;
    box-shadow: 0 4px 18px rgba(0, 0, 0, 0.08);
}


.page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 20px;
    margin-bottom: 30px;
}


.taco-card {
    transition:
        transform 0.2s ease,
        box-shadow 0.2s ease;
}


.taco-card:hover {
    transform: translateY(-4px);
    box-shadow:
        0 8px 20px rgba(0, 0, 0, 0.12);
}


.form-control,
.form-select {
    border-radius: 6px;
}


.btn {
    border-radius: 6px;
}


@media (max-width: 768px) {

    .page-header {
        align-items: flex-start;
        flex-direction: column;
    }

}


@media (max-width: 576px) {

    .form-card {
        padding: 20px;
    }

}
```

---

# 📄 `flask_app/__init__.py`

```python
# ==========================================================
# INICIALIZACIÓN DE FLASK
# ==========================================================

from flask import Flask


# ==========================================================
# CREAR APLICACIÓN
# ==========================================================

app = Flask(__name__)


# ==========================================================
# SECRET KEY
# ==========================================================

app.secret_key = "clave-secreta-desarrollo"
```

---

# 📄 `flask_app/controllers/__init__.py`

```python
# Controladores de la aplicación Flask.
```

---

# 📄 `flask_app/models/__init__.py`

```python
# Modelos de la aplicación.
```

---

# 📄 `server.py`

```python
# ==========================================================
# PUNTO DE ENTRADA
# ==========================================================

from flask_app import app


# ==========================================================
# IMPORTAR CONTROLADOR
# ==========================================================
#
# Esta importación carga las rutas definidas en:
#
# flask_app/controllers/tacos.py
#
# y permite que Flask las registre.
# ==========================================================

from flask_app.controllers import tacos


# ==========================================================
# EJECUTAR APLICACIÓN
# ==========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )
```

---

# 🔄 Flujo completo de la relación

El flujo más importante de esta lección es:

```text
GET /restaurantes/1
        ↓
controllers/tacos.py
        ↓
Restaurante.get_restaurante_y_tacos()
        ↓
LEFT JOIN
        ↓
MySQL
        ↓
lista de diccionarios
        ↓
crear Restaurante
        ↓
recorrer resultados
        ↓
crear objetos Taco
        ↓
restaurante.tacos
        ↓
restaurante.html
        ↓
Jinja2
        ↓
HTML
```

---

# 🧠 ¿Qué contiene `restaurante.tacos`?

Después del `JOIN`:

```python
restaurante.tacos
```

puede contener:

```python
[
    Taco(...),
    Taco(...),
    Taco(...)
]
```

Por eso en Jinja2 podemos utilizar:

```jinja
{% for taco in restaurante.tacos %}
```

y acceder a:

```jinja
{{ taco.tortilla }}
```

```jinja
{{ taco.guiso }}
```

```jinja
{{ taco.salsa }}
```

---

# 🧩 Caso sin tacos

Imaginemos:

```text
Restaurante #4
Tacos La Plaza
```

pero no existen filas en `tacos` con:

```text
restaurante_id = 4
```

Debido al:

```sql
LEFT JOIN
```

el restaurante seguirá apareciendo.

Pero:

```text
taco_id
```

será:

```text
NULL
```

Por eso tenemos:

```python
if fila_en_db["taco_id"] is not None:
```

Solamente si existe un taco creamos:

```python
Taco(...)
```

De lo contrario:

```python
restaurante.tacos
```

queda:

```python
[]
```

---

# 🔍 Comparación conceptual

## Sin relación

Podríamos tener:

```text
Restaurante
```

por un lado:

```text
Taco
```

por otro.

No sabemos directamente qué taco pertenece a qué restaurante.

---

## Con relación

Tenemos:

```text
Restaurante
     │
     ▼
lista de Tacos
```

En Python:

```python
restaurante.tacos
```

Esto representa la relación de una manera natural.

---

# 🍽️ Ejemplo completo

Supongamos:

```text
Restaurante:
Tacos El Sol
ID:
1
```

y:

```text
Taco #1
restaurante_id = 1

Taco #2
restaurante_id = 1
```

La consulta devuelve:

```text
Restaurante 1 + Taco 1
Restaurante 1 + Taco 2
```

Python lo convierte en:

```python
restaurante = Restaurante(...)
```

y:

```python
restaurante.tacos = [
    Taco(...),
    Taco(...)
]
```

La vista puede simplemente hacer:

```jinja
<h1>
    {{ restaurante.nombre }}
</h1>
```

y:

```jinja
{% for taco in restaurante.tacos %}
```

---

# 🧪 Prueba de funcionamiento

## 1. Ejecutar

Desde la raíz:

```bash
pipenv run python server.py
```

---

## 2. Abrir formulario

```text
http://127.0.0.1:5000/
```

Seleccionar:

```text
Tacos El Sol
```

Crear un nuevo taco.

---

## 3. Ver restaurantes

Abrir:

```text
http://127.0.0.1:5000/restaurantes
```

Deberán aparecer:

```text
Tacos El Sol
Tacos Central
Tacos Don Pepe
```

---

## 4. Ver tacos de un restaurante

Presionar:

```text
Ver tacos
```

para:

```text
Tacos El Sol
```

La URL será:

```text
/restaurantes/1
```

y deberán aparecer sus tacos relacionados.

---

# 🧪 Comprobación directa en MySQL

Después de crear un taco:

```sql
USE esquema_tacos;

SELECT *
FROM tacos;
```

Comprueba también:

```sql
SELECT *
FROM tacos
WHERE restaurante_id = 1;
```

Esto permite verificar que el nuevo taco esté asociado correctamente.

---

# 🧠 Relación entre formulario y base de datos

Cuando el usuario selecciona:

```text
Tacos Central
```

el formulario envía:

```text
restaurante_id = 2
```

Flask recibe:

```python
request.form["restaurante_id"]
```

Luego:

```python
datos = {
    "tortilla": ...,
    "guiso": ...,
    "salsa": ...,
    "restaurante_id": 2
}
```

Después:

```python
Taco.save(datos)
```

y finalmente:

```sql
INSERT INTO tacos
(
    tortilla,
    guiso,
    salsa,
    restaurante_id
)
VALUES
(
    %(tortilla)s,
    %(guiso)s,
    %(salsa)s,
    %(restaurante_id)s
);
```

---

# 🔐 Sentencia preparada

Observa:

```sql
%(restaurante_id)s
```

y:

```python
"restaurante_id": 2
```

La relación entre ambos es:

```text
%(restaurante_id)s
        ↓
datos["restaurante_id"]
        ↓
2
        ↓
tacos.restaurante_id
```

---

# 🧠 Conceptos fundamentales

| Concepto | Función |
|---|---|
| `PRIMARY KEY` | Identifica un registro |
| `FOREIGN KEY` | Relaciona tablas |
| `restaurante_id` | Identifica el restaurante del taco |
| Relación 1:N | Un restaurante puede tener muchos tacos |
| `JOIN` | Combina información de tablas |
| `LEFT JOIN` | Mantiene el registro principal aunque no tenga relacionados |
| `AS` | Crea alias para evitar ambigüedad |
| `self.tacos = []` | Lista de tacos relacionados |
| `Taco(...)` | Crea un objeto Taco |
| `append()` | Agrega el taco a la lista |
| Parsear | Transformar resultados en objetos |
| Jinja2 | Mostrar objetos relacionados |

---

# 🧠 Modelo mental

Cuando encuentres una relación:

```text
1 Restaurante
N Tacos
```

piensa:

```text
BASE DE DATOS

restaurantes.id
      ↑
      │
tacos.restaurante_id
```

y en Python:

```text
Restaurante
      │
      ▼
restaurante.tacos
      │
      ├── Taco
      ├── Taco
      └── Taco
```

---

# ⚠️ Errores comunes

## `Unknown column 'restaurante_id'`

La tabla `tacos` todavía no tiene la clave foránea.

Comprueba:

```sql
DESCRIBE tacos;
```

Debe existir:

```text
restaurante_id
```

---

## `Unknown column 'taco_id'`

Esto normalmente ocurre cuando el `SELECT` no utiliza:

```sql
tacos.id AS taco_id
```

Revisa los alias del `JOIN`.

---

## Todos los restaurantes aparecen sin tacos

Comprueba:

```sql
tacos.restaurante_id
```

y:

```sql
restaurantes.id
```

Los valores deben coincidir.

---

## El `<select>` aparece vacío

Comprueba:

```python
todos_restaurantes = Restaurante.get_all()
```

y que la plantilla utilice:

```jinja
{% for restaurante in todos_restaurantes %}
```

---

## `request.form["restaurante_id"]` genera error

Revisa que el HTML tenga:

```html
<select name="restaurante_id">
```

---

## No aparece un restaurante sin tacos

Verifica que estés utilizando:

```sql
LEFT JOIN
```

y no:

```sql
INNER JOIN
```

---

## Se crean tacos pero no están asociados

Comprueba que el `INSERT` incluya:

```text
restaurante_id
```

---

# ✅ Checklist

```text
[ ] Pipenv configurado
[ ] Flask instalado
[ ] PyMySQL instalado
[ ] Base de datos creada
[ ] Tabla restaurantes creada
[ ] Tabla tacos creada
[ ] FOREIGN KEY creada
[ ] Datos de prueba insertados
[ ] ERD guardado en resources/
[ ] mysqlconnection.py funciona
[ ] modelo Taco creado
[ ] modelo Restaurante creado
[ ] restaurante.tacos inicializado
[ ] get_all() funciona
[ ] get_restaurante_y_tacos() funciona
[ ] LEFT JOIN funciona
[ ] Aliases del JOIN funcionan
[ ] objetos Taco se crean correctamente
[ ] objetos Taco se agregan a restaurante.tacos
[ ] formulario con select funciona
[ ] restaurante_id llega a Flask
[ ] INSERT funciona
[ ] /restaurantes funciona
[ ] /restaurantes/<id> funciona
[ ] Jinja2 recorre restaurante.tacos
[ ] caso sin tacos funciona
```

---

# 🏁 Resultado esperado

La aplicación debe permitir:

```text
                   RESTAURANTES
                         │
              ┌──────────┼──────────┐
              │          │          │
              ▼          ▼          ▼
          El Sol      Central     Don Pepe
              │          │
              │          │
              ▼          ▼
           tacos       tacos
              │          │
              ├── Taco   ├── Taco
              └── Taco   └── Taco
```

Y en Python:

```python
restaurante.tacos
```

representará una:

```text
lista de objetos Taco
```

---

# 🔗 Flujo final

```text
                 MYSQL
                   │
                   ▼
          ┌─────────────────┐
          │  restaurantes   │
          └────────┬────────┘
                   │
                   │ 1:N
                   ▼
          ┌─────────────────┐
          │     tacos       │
          └────────┬────────┘
                   │
                   ▼
                LEFT JOIN
                   │
                   ▼
          lista de diccionarios
                   │
                   ▼
             Restaurante
                   │
                   └──────► tacos = [
                                  Taco(),
                                  Taco(),
                                  Taco()
                              ]
                   │
                   ▼
                Jinja2
                   │
                   ▼
                  HTML
```

---

# 🎓 Conclusión

La idea central de esta lección es comprender que una relación de base de datos también puede representarse como una relación entre objetos.

En MySQL tenemos:

```text
restaurantes
     │
     │ 1:N
     ▼
tacos
```

La relación se establece mediante:

```text
tacos.restaurante_id
```

En Python podemos representarla mediante:

```python
restaurante.tacos
```

El proceso completo es:

```text
FOREIGN KEY
      ↓
JOIN
      ↓
resultado SQL
      ↓
diccionarios
      ↓
objetos Restaurante y Taco
      ↓
lista de objetos relacionados
      ↓
Jinja2
      ↓
HTML
```

Este patrón puede reutilizarse posteriormente en relaciones como:

```text
Cliente → Pedidos

Categoría → Productos

Curso → Estudiantes

Autor → Libros

Usuario → Publicaciones
```

La aplicación final demuestra cómo **MySQL, Flask, POO, PyMySQL, MVC y Jinja2 pueden trabajar conjuntamente para representar relaciones uno a muchos**.
Mostrando README.md 