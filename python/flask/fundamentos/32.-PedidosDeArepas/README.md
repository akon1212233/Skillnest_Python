# 🫓 Pedidos de Arepas — Flask + MySQL + MVC + Validación

## 📌 Descripción

En esta actividad se construirá una aplicación web modularizada con **Flask y MySQL** para administrar pedidos de arepas.

La práctica integra contenidos trabajados anteriormente sobre:

- Flask
- MySQL
- PyMySQL
- Programación Orientada a Objetos
- Arquitectura MVC
- Formularios HTML
- Métodos `GET` y `POST`
- `request.form`
- `render_template()`
- `redirect()`
- `url_for()`
- Sentencias preparadas
- Validación de formularios
- `@staticmethod`
- Mensajes `flash()`
- Jinja2
- Pipenv

La aplicación permitirá:

```text
Crear un pedido
        ↓
Validar los datos
        ↓
Si existen errores
        ↓
Mostrar mensajes flash
        ↓
Volver al formulario

Si los datos son correctos
        ↓
Guardar en MySQL
        ↓
Redirigir al listado
        ↓
Mostrar el nuevo pedido
```

---

# 🎯 Objetivos

Al finalizar la actividad se deberá poder:

- Crear una aplicación CR modularizada.
- Crear registros de pedidos.
- Recuperar y mostrar pedidos desde MySQL.
- Validar información antes de guardarla.
- Utilizar un método `@staticmethod` para validar.
- Utilizar `flash()` para comunicar errores.
- Utilizar `secret_key` para trabajar con mensajes flash.
- Utilizar formularios mediante `POST`.
- Utilizar sentencias preparadas.
- Aplicar arquitectura MVC.

---

# 🧠 ¿Por qué debemos validar los formularios?

Los datos ingresados por un usuario no deben guardarse directamente sin comprobar que cumplen las reglas de la aplicación.

Por ejemplo, no debería ser posible registrar:

```text
Nombre:
```

o:

```text
Cantidad:
0
```

o:

```text
Nombre:
A
```

La validación permite comprobar que la información cumple nuestras reglas antes de ejecutar el `INSERT`.

El flujo será:

```text
Formulario
    ↓
request.form
    ↓
Diccionario de datos
    ↓
validar_pedido()
    ↓
┌───────────────────────┐
│                       │
▼                       ▼
INVÁLIDO               VÁLIDO
│                       │
▼                       ▼
flash()                save()
│                       │
▼                       ▼
redirect()             INSERT
│                       │
▼                       ▼
Formulario             redirect()
                         │
                         ▼
                       Listado
```

---

# 📐 Reglas de validación

La actividad exige las siguientes reglas:

## Regla 1 — Todos los campos son obligatorios

Se deben completar:

```text
Nombre
Tipo de Arepa
Cantidad
```

---

## Regla 2 — Nombre mínimo

El nombre debe tener:

```text
mínimo 2 caracteres
```

Por ejemplo:

```text
A
```

es inválido.

Mientras:

```text
Ana
```

es válido.

---

## Regla 3 — Cantidad

La cantidad debe ser:

```text
mayor que 0
```

Por ejemplo:

```text
0
```

es inválido.

También:

```text
-2
```

es inválido.

Mientras:

```text
1
2
5
10
```

son valores válidos.

---

# 🗃️ Modelo de datos

La base de datos se llamará:

```text
esquema_arepas
```

Tendrá una tabla:

```text
pedidos
```

---

## Tabla `pedidos`

```text
pedidos
│
├── id
├── nombre
├── tipo_arepa
├── cantidad
├── created_at
└── updated_at
```

---

# 🧩 Estructura del ERD

El ERD debe representar:

```text
┌────────────────────────────────┐
│            pedidos             │
├────────────────────────────────┤
│ id             INT PK          │
│ nombre         VARCHAR(100)    │
│ tipo_arepa     VARCHAR(100)    │
│ cantidad       INT             │
│ created_at     DATETIME        │
│ updated_at     DATETIME        │
└────────────────────────────────┘
```

No existe ninguna relación entre tablas en esta actividad.

Es una sola entidad:

```text
Pedido
```

---

# 🛠️ MySQL Workbench

El ERD debe crearse en **MySQL Workbench**.

La tabla `pedidos` debe representar los campos indicados anteriormente.

Después de crear el ERD se puede utilizar:

```text
Database
   ↓
Forward Engineer
```

para generar el esquema de la base de datos.

---

# 📁 Recursos

Todo proyecto con base de datos debe conservar su ERD.

La carpeta:

```text
resources/
```

debe contener:

```text
resources/
└── esquema_arepas_erd.mwb
```

Opcionalmente puede incluirse:

```text
resources/
├── esquema_arepas_erd.mwb
└── esquema_arepas_erd.png
```

---

# 📁 Estructura final del proyecto

La aplicación utilizará MVC.

```text
pedidos_arepas/
│
├── flask_app/
│   │
│   ├── __init__.py
│   │
│   ├── bd/
│   │   └── esquema_arepas.sql
│   │
│   ├── config/
│   │   └── mysqlconnection.py
│   │
│   ├── controllers/
│   │   └── pedidos.py
│   │
│   ├── models/
│   │   └── pedido.py
│   │
│   ├── templates/
│   │   ├── pedidos.html
│   │   └── nuevo_pedido.html
│   │
│   └── static/
│       └── css/
│           └── style.css
│
├── resources/
│   └── esquema_arepas_erd.mwb
│
├── Pipfile
├── Pipfile.lock
├── .gitignore
└── server.py
```

> En esta estructura se utiliza solamente `flask_app/__init__.py`. Las carpetas `config`, `controllers`, `models`, `templates`, `static`, `bd` y `resources` no necesitan tener su propio `__init__.py` para este proyecto.

---

# 🏗️ Arquitectura MVC

## Model

```text
flask_app/models/pedido.py
```

Responsable de:

- representar los pedidos;
- consultar MySQL;
- insertar registros;
- validar los datos.

---

## View

```text
flask_app/templates/
```

Responsable de:

- HTML;
- formularios;
- Jinja2;
- mensajes flash;
- presentación de los pedidos.

---

## Controller

```text
flask_app/controllers/pedidos.py
```

Responsable de:

- recibir solicitudes;
- utilizar `request.form`;
- llamar al modelo;
- decidir si continúa o redirige;
- renderizar las vistas.

---

## Config

```text
flask_app/config/mysqlconnection.py
```

Responsable de:

```text
Conexión Flask
      ↓
PyMySQL
      ↓
MySQL
```

---

# 🐍 Configuración con Pipenv

Instalar las dependencias:

```bash
pipenv install flask pymysql
```

Ejecutar la aplicación:

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

## `flask_app/bd/esquema_arepas.sql`

```sql
-- ==========================================================
-- BASE DE DATOS
-- ==========================================================

CREATE DATABASE IF NOT EXISTS esquema_arepas;

USE esquema_arepas;


-- ==========================================================
-- TABLA PEDIDOS
-- ==========================================================

CREATE TABLE IF NOT EXISTS pedidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    tipo_arepa VARCHAR(100) NOT NULL,
    cantidad INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);


-- ==========================================================
-- DATOS DE PRUEBA
-- ==========================================================

INSERT INTO pedidos
(
    nombre,
    tipo_arepa,
    cantidad
)
VALUES
(
    "María",
    "Arepa de queso",
    2
),
(
    "Carlos",
    "Arepa de carne",
    3
),
(
    "Ana",
    "Arepa de pollo",
    1
);
```

---

# 🔍 Comprobar la base de datos

Después de ejecutar el SQL:

```sql
USE esquema_arepas;
```

Consultar la tabla:

```sql
SELECT *
FROM pedidos;
```

Deberían aparecer los registros de prueba:

```text
María  | Arepa de queso | 2
Carlos | Arepa de carne | 3
Ana    | Arepa de pollo | 1
```

---

# ⚙️ Inicialización de Flask

## `flask_app/__init__.py`

```python
from flask import Flask

app = Flask(__name__)

# Necesaria para que Flask pueda utilizar flash().
app.secret_key = "clave-secreta-desarrollo"
```

---

# 🔑 ¿Por qué necesitamos `secret_key`?

Los mensajes:

```python
flash()
```

utilizan el sistema de sesión de Flask.

Por eso necesitamos configurar:

```python
app.secret_key
```

La clave permite a Flask proteger la información asociada a la sesión.

En este proyecto utilizaremos:

```python
app.secret_key = "clave-secreta-desarrollo"
```

Para un proyecto real, una clave sensible no debería escribirse directamente en el código fuente.

---

# 🔌 Conexión con MySQL

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
            devuelve la cantidad de filas afectadas.

        En caso de error:
            devuelve False.
        """

        with self.connection.cursor() as cursor:
            try:
                cursor.execute(query, data)

                tipo_consulta = query.strip().lower()

                if tipo_consulta.startswith("select"):
                    return cursor.fetchall()

                if tipo_consulta.startswith("insert"):
                    return cursor.lastrowid

                return cursor.rowcount

            except Exception as e:
                print("Something went wrong:", e)
                return False

            finally:
                self.connection.close()


def connectToMySQL(db):
    """
    Crea una instancia de conexión con la base de datos.
    """

    return MySQLConnection(db)
```

> Debes cambiar `user` y `password` de acuerdo con tu instalación local de MySQL.

---

# 📦 Modelo

## `flask_app/models/pedido.py`

Este archivo representa la tabla:

```text
pedidos
```

Además contiene el método que validará la información.

```python
from flask import flash

from flask_app.config.mysqlconnection import connectToMySQL


class Pedido:
    """
    Representa un registro de la tabla pedidos.
    """

    def __init__(self, data):
        self.id = data["id"]
        self.nombre = data["nombre"]
        self.tipo_arepa = data["tipo_arepa"]
        self.cantidad = data["cantidad"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]


    # ======================================================
    # VALIDACIÓN
    # ======================================================

    @staticmethod
    def validar_pedido(pedido):
        """
        Valida los datos recibidos desde el formulario.

        Devuelve:
            True  → información válida.
            False → existen errores.
        """

        es_valido = True


        # --------------------------------------------------
        # Nombre obligatorio
        # --------------------------------------------------

        if not pedido["nombre"]:

            flash(
                "El nombre es obligatorio.",
                "danger"
            )

            es_valido = False


        # --------------------------------------------------
        # Nombre mínimo
        # --------------------------------------------------

        elif len(pedido["nombre"]) < 2:

            flash(
                "El nombre debe tener al menos 2 caracteres.",
                "danger"
            )

            es_valido = False


        # --------------------------------------------------
        # Tipo de arepa obligatorio
        # --------------------------------------------------

        if not pedido["tipo_arepa"]:

            flash(
                "El tipo de arepa es obligatorio.",
                "danger"
            )

            es_valido = False


        # --------------------------------------------------
        # Cantidad obligatoria
        # --------------------------------------------------

        if not pedido["cantidad"]:

            flash(
                "La cantidad es obligatoria.",
                "danger"
            )

            es_valido = False

        else:

            # Intentamos convertir la cantidad a entero.
            try:

                cantidad = int(
                    pedido["cantidad"]
                )

                if cantidad <= 0:

                    flash(
                        "La cantidad debe ser mayor que 0.",
                        "danger"
                    )

                    es_valido = False

            except ValueError:

                flash(
                    "La cantidad debe ser mayor que 0.",
                    "danger"
                )

                es_valido = False


        return es_valido


    # ======================================================
    # READ
    # ======================================================

    @classmethod
    def get_all(cls):
        """
        Obtiene todos los pedidos.
        """

        query = """
            SELECT
                id,
                nombre,
                tipo_arepa,
                cantidad,
                created_at,
                updated_at
            FROM pedidos
            ORDER BY id DESC;
        """


        resultados = connectToMySQL(
            "esquema_arepas"
        ).query_db(query)


        pedidos = []


        for pedido in resultados:

            pedidos.append(
                cls(pedido)
            )


        return pedidos


    # ======================================================
    # CREATE
    # ======================================================

    @classmethod
    def save(cls, data):
        """
        Guarda un nuevo pedido en la base de datos.
        """

        query = """
            INSERT INTO pedidos
            (
                nombre,
                tipo_arepa,
                cantidad
            )
            VALUES
            (
                %(nombre)s,
                %(tipo_arepa)s,
                %(cantidad)s
            );
        """


        return connectToMySQL(
            "esquema_arepas"
        ).query_db(
            query,
            data
        )
```

---

# 🧠 ¿Qué hace `@staticmethod`?

El método:

```python
@staticmethod
def validar_pedido(pedido):
```

es una función auxiliar de la clase.

No necesita:

```text
self
```

ni:

```text
cls
```

Solamente necesita recibir los datos que queremos validar:

```python
pedido
```

Por eso podemos hacer:

```python
Pedido.validar_pedido(data)
```

---

# 🧠 Flujo de validación del modelo

```text
Pedido.validar_pedido(data)
        ↓
es_valido = True
        ↓
comprobar nombre
        ↓
comprobar tipo_arepa
        ↓
comprobar cantidad
        ↓
¿errores?
   │
   ├── Sí → flash() + False
   │
   └── No → True
```

---

# 🎮 Controlador

## `flask_app/controllers/pedidos.py`

```python
from flask_app import app

from flask import (
    render_template,
    request,
    redirect,
    url_for
)

from flask_app.models.pedido import Pedido


# ==========================================================
# INICIO
# ==========================================================

@app.route("/")
def inicio():
    """
    La ruta raíz redirige al listado de pedidos.
    """

    return redirect(
        url_for("pedidos")
    )


# ==========================================================
# LISTADO DE PEDIDOS
# ==========================================================

@app.route("/pedidos")
def pedidos():
    """
    Recupera los pedidos desde MySQL
    y los envía a la vista.
    """

    todos_los_pedidos = Pedido.get_all()


    return render_template(
        "pedidos.html",
        pedidos=todos_los_pedidos
    )


# ==========================================================
# FORMULARIO NUEVO PEDIDO
# ==========================================================

@app.route("/pedidos/nuevo")
def nuevo_pedido():
    """
    Muestra el formulario de creación.
    """

    return render_template(
        "nuevo_pedido.html"
    )


# ==========================================================
# CREAR PEDIDO
# ==========================================================

@app.route(
    "/pedidos/crear",
    methods=["POST"]
)
def crear_pedido():
    """
    Recibe la información del formulario,
    valida los datos y, si son correctos,
    guarda el pedido.
    """

    # ------------------------------------------------------
    # Recuperamos los datos enviados por el formulario.
    # ------------------------------------------------------

    nombre = request.form.get(
        "nombre",
        ""
    ).strip()

    tipo_arepa = request.form.get(
        "tipo_arepa",
        ""
    ).strip()

    cantidad = request.form.get(
        "cantidad",
        ""
    ).strip()


    # ------------------------------------------------------
    # Creamos el diccionario que recibirá el modelo.
    # ------------------------------------------------------

    data = {
        "nombre": nombre,
        "tipo_arepa": tipo_arepa,
        "cantidad": cantidad
    }


    # ------------------------------------------------------
    # Validamos ANTES de guardar.
    # ------------------------------------------------------

    if not Pedido.validar_pedido(data):

        return redirect(
            url_for("nuevo_pedido")
        )


    # ------------------------------------------------------
    # Como la validación fue correcta, convertimos
    # cantidad a entero antes de guardarla.
    # ------------------------------------------------------

    data["cantidad"] = int(
        data["cantidad"]
    )


    # ------------------------------------------------------
    # Guardamos el pedido.
    # ------------------------------------------------------

    resultado = Pedido.save(
        data
    )


    # ------------------------------------------------------
    # En caso de error en la base de datos.
    # ------------------------------------------------------

    if resultado is False:

        from flask import flash

        flash(
            "No fue posible guardar el pedido.",
            "danger"
        )

        return redirect(
            url_for("nuevo_pedido")
        )


    # ------------------------------------------------------
    # Pedido creado correctamente.
    # ------------------------------------------------------

    from flask import flash

    flash(
        "Pedido creado correctamente.",
        "success"
    )


    return redirect(
        url_for("pedidos")
    )
```

---

# 🧠 ¿Qué ocurre en el controlador?

Cuando llega:

```text
POST /pedidos/crear
```

el controlador recibe:

```python
request.form
```

y construye:

```python
data = {
    "nombre": nombre,
    "tipo_arepa": tipo_arepa,
    "cantidad": cantidad
}
```

Después:

```python
Pedido.validar_pedido(data)
```

Si devuelve:

```python
False
```

no se ejecuta:

```python
Pedido.save(data)
```

Esto es fundamental.

---

# 🚫 Datos inválidos

El flujo es:

```text
POST
 ↓
request.form
 ↓
data
 ↓
validar_pedido()
 ↓
False
 ↓
flash()
 ↓
redirect()
 ↓
/pedidos/nuevo
```

La base de datos **no recibe el INSERT**.

---

# ✅ Datos válidos

El flujo es:

```text
POST
 ↓
request.form
 ↓
data
 ↓
validar_pedido()
 ↓
True
 ↓
int(cantidad)
 ↓
Pedido.save()
 ↓
INSERT
 ↓
MySQL
 ↓
flash()
 ↓
redirect()
 ↓
/pedidos
```

---

# 👁️ Vista de pedidos

## `flask_app/templates/pedidos.html`

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
        Pedidos de Arepas
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

    <div class="d-flex justify-content-between align-items-center mb-4">

        <div>

            <h1>
                Pedidos de Arepas
            </h1>

            <p class="text-muted mb-0">
                Pedidos registrados en la base de datos.
            </p>

        </div>


        <a
            href="{{ url_for('nuevo_pedido') }}"
            class="btn btn-success"
        >

            Nuevo Pedido

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
         LISTADO
    =================================================== -->

    <div class="card shadow-sm border-0">

        <div class="card-body p-0">


            {% if pedidos %}

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
                                    Tipo de Arepa
                                </th>

                                <th>
                                    Cantidad
                                </th>

                            </tr>

                        </thead>


                        <tbody>

                            {% for pedido in pedidos %}

                                <tr>

                                    <td>
                                        {{ pedido.id }}
                                    </td>

                                    <td>
                                        {{ pedido.nombre }}
                                    </td>

                                    <td>
                                        {{ pedido.tipo_arepa }}
                                    </td>

                                    <td>
                                        {{ pedido.cantidad }}
                                    </td>

                                </tr>

                            {% endfor %}

                        </tbody>

                    </table>

                </div>


            {% else %}

                <div class="p-4">

                    <div class="alert alert-info mb-0">

                        No existen pedidos registrados.

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

# 📝 Vista Nuevo Pedido

## `flask_app/templates/nuevo_pedido.html`

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
        Nuevo Pedido
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

        <div class="col-lg-6">


            <div class="card shadow-sm border-0">

                <div class="card-body p-4">


                    <!-- ==================================================
                         ENCABEZADO
                    =================================================== -->

                    <h1 class="h2 mb-2">
                        Nuevo Pedido
                    </h1>


                    <p class="text-muted mb-4">

                        Completa los datos del pedido.

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
                        action="{{ url_for('crear_pedido') }}"
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
                                minlength="2"
                                required
                            >

                        </div>


                        <!-- TIPO DE AREPA -->

                        <div class="mb-3">

                            <label
                                for="tipo_arepa"
                                class="form-label"
                            >

                                Tipo de Arepa

                            </label>


                            <input
                                type="text"
                                id="tipo_arepa"
                                name="tipo_arepa"
                                class="form-control"
                                required
                            >

                        </div>


                        <!-- CANTIDAD -->

                        <div class="mb-4">

                            <label
                                for="cantidad"
                                class="form-label"
                            >

                                Cantidad

                            </label>


                            <input
                                type="number"
                                id="cantidad"
                                name="cantidad"
                                class="form-control"
                                min="1"
                                required
                            >

                        </div>


                        <!-- BOTONES -->

                        <div class="d-flex gap-2">

                            <button
                                type="submit"
                                class="btn btn-success"
                            >

                                Crear Pedido

                            </button>


                            <a
                                href="{{ url_for('pedidos') }}"
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

@media (max-width: 576px) {

    .d-flex {
        flex-wrap: wrap;
    }

}
```

---

# 🚀 Punto de entrada

## `server.py`

```python
from flask_app import app

# Importamos el controlador para registrar las rutas.
from flask_app.controllers import pedidos


if __name__ == "__main__":
    app.run(debug=True)
```

---

# 🔄 Flujo de navegación

La aplicación tendrá las siguientes rutas:

| Método | Ruta | Función |
|---|---|---|
| `GET` | `/` | Redirige a pedidos |
| `GET` | `/pedidos` | Muestra todos los pedidos |
| `GET` | `/pedidos/nuevo` | Muestra el formulario |
| `POST` | `/pedidos/crear` | Valida y crea el pedido |

---

# 🧭 Flujo de `/`

Cuando el usuario entra a:

```text
http://127.0.0.1:5000/
```

se ejecuta:

```python
return redirect(
    url_for("pedidos")
)
```

y Flask envía al usuario a:

```text
/pedidos
```

---

# 📋 Flujo de lectura

Cuando se visita:

```text
/pedidos
```

se ejecuta:

```python
todos_los_pedidos = Pedido.get_all()
```

El modelo consulta:

```sql
SELECT ...
FROM pedidos
```

y devuelve una lista de objetos:

```text
Pedido
Pedido
Pedido
```

El controlador entrega esos objetos a:

```text
pedidos.html
```

Jinja2 los recorre:

```jinja
{% for pedido in pedidos %}
```

y muestra:

```jinja
{{ pedido.nombre }}
{{ pedido.tipo_arepa }}
{{ pedido.cantidad }}
```

---

# 📨 Flujo de un formulario

Al presionar:

```text
Crear Pedido
```

el navegador realiza:

```text
POST /pedidos/crear
```

Los datos son recibidos mediante:

```python
request.form
```

Por ejemplo:

```text
nombre = "María"
tipo_arepa = "Arepa de queso"
cantidad = "2"
```

Observa que:

```text
"2"
```

llega inicialmente como texto.

Por eso, después de validar, realizamos:

```python
int(data["cantidad"])
```

obteniendo:

```text
2
```

como número entero.

---

# 🧠 Flujo de validación

El controlador llama:

```python
Pedido.validar_pedido(data)
```

El método devuelve:

```text
True
```

o:

```text
False
```

Por ejemplo:

```python
if not Pedido.validar_pedido(data):
    return redirect(
        url_for("nuevo_pedido")
    )
```

Esto significa:

```text
Si NO es válido
       ↓
regresa al formulario
```

---

# ✨ Mensajes flash

Para mostrar un error utilizamos:

```python
flash(
    "El nombre es obligatorio.",
    "danger"
)
```

Otro ejemplo:

```python
flash(
    "La cantidad debe ser mayor que 0.",
    "danger"
)
```

Y para una operación correcta:

```python
flash(
    "Pedido creado correctamente.",
    "success"
)
```

---

# 🧠 ¿Cómo llegan los mensajes al HTML?

En:

```text
nuevo_pedido.html
```

tenemos:

```jinja
{% with messages = get_flashed_messages(
    with_categories=true
) %}
```

Esto recupera los mensajes flash.

Después:

```jinja
{% for category, message in messages %}
```

permite recorrerlos.

Finalmente:

```jinja
{{ message }}
```

muestra el texto.

La categoría:

```jinja
{{ category }}
```

se utiliza para elegir el estilo Bootstrap:

```html
<div class="alert alert-{{ category }}">
```

Por ejemplo:

```text
danger
```

genera:

```html
alert alert-danger
```

---

# 🔥 ¿Por qué pueden aparecer varios errores?

El método de validación no termina después del primer error.

Supongamos:

```text
Nombre:
A

Tipo de Arepa:

Cantidad:
0
```

Podrían generarse:

```text
El nombre debe tener al menos 2 caracteres.
El tipo de arepa es obligatorio.
La cantidad debe ser mayor que 0.
```

Todos los mensajes se almacenan mediante `flash()`.

Después:

```python
return False
```

y el controlador redirige al formulario.

---

# 🧠 Frontend vs Backend

El formulario utiliza:

```html
required
```

y:

```html
min="1"
```

Esto ayuda al usuario desde el navegador.

Pero no debemos depender exclusivamente de ello.

Tenemos:

```text
HTML
 ↓
validación frontend
```

y:

```text
Python
 ↓
validación backend
```

La validación en Python es fundamental porque la solicitud podría enviarse directamente al servidor sin respetar las restricciones visuales del formulario.

---

# 🔐 Sentencias preparadas

El método `save()` utiliza:

```python
query = """
    INSERT INTO pedidos
    (
        nombre,
        tipo_arepa,
        cantidad
    )
    VALUES
    (
        %(nombre)s,
        %(tipo_arepa)s,
        %(cantidad)s
    );
"""
```

Los valores se entregan por separado:

```python
data = {
    "nombre": "María",
    "tipo_arepa": "Arepa de queso",
    "cantidad": 2
}
```

Esto evita construir consultas concatenando directamente los datos ingresados.

---

# 🧠 Modelo mental

La aplicación puede entenderse como:

```text
                 USUARIO
                    │
                    ▼
              FORMULARIO
                    │
                    │ POST
                    ▼
              CONTROLLER
                    │
                    ▼
          request.form / data
                    │
                    ▼
             VALIDACIÓN
                    │
             ┌──────┴──────┐
             │             │
             ▼             ▼
          INVÁLIDO       VÁLIDO
             │             │
             ▼             ▼
           flash()      Pedido.save()
             │             │
             ▼             ▼
         redirect()       INSERT
             │             │
             └──────┬──────┘
                    ▼
                 MySQL
                    │
                    ▼
                redirect()
                    │
                    ▼
                /pedidos
```

---

# 🧩 Arquitectura completa

```text
                    NAVEGADOR
                        │
                        ▼
                    CONTROLLER
                        │
                ┌───────┴───────┐
                │               │
                ▼               ▼
              MODEL           VIEW
                │               │
                ▼               ▼
              MySQL          Jinja2
                │               │
                └───────┬───────┘
                        │
                        ▼
                       HTML
```

---

# 🧪 Pruebas funcionales

## ✅ Prueba 1 — Pedido válido

Ingresar:

```text
Nombre:
María

Tipo de Arepa:
Arepa de queso

Cantidad:
2
```

Resultado:

```text
Pedido creado correctamente.
```

El usuario debe volver a:

```text
/pedidos
```

y el pedido debe aparecer.

---

# ❌ Prueba 2 — Formulario vacío

Enviar:

```text
Nombre: vacío
Tipo de Arepa: vacío
Cantidad: vacío
```

Deben aparecer mensajes equivalentes a:

```text
El nombre es obligatorio.
El tipo de arepa es obligatorio.
La cantidad es obligatoria.
```

No se debe ejecutar el `INSERT`.

---

# ❌ Prueba 3 — Nombre demasiado corto

Ingresar:

```text
Nombre:
A
```

Debe aparecer:

```text
El nombre debe tener al menos 2 caracteres.
```

---

# ❌ Prueba 4 — Cantidad igual a cero

Ingresar:

```text
Cantidad:
0
```

Debe aparecer:

```text
La cantidad debe ser mayor que 0.
```

---

# ❌ Prueba 5 — Cantidad negativa

Ingresar:

```text
Cantidad:
-3
```

Debe aparecer:

```text
La cantidad debe ser mayor que 0.
```

---

# ❌ Prueba 6 — Varios errores

Ingresar:

```text
Nombre:
A

Tipo de Arepa:

Cantidad:
0
```

Deben mostrarse los errores correspondientes.

---

# 🔎 Comprobación en MySQL

Después de crear un pedido correctamente:

```sql
USE esquema_arepas;

SELECT *
FROM pedidos;
```

El nuevo registro debe aparecer.

Si se envió un formulario inválido, dicho pedido **no debe aparecer**.

---

# ⚠️ Errores comunes

## Olvidar `secret_key`

Si utilizas:

```python
flash()
```

debes tener:

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

## Guardar antes de validar

Incorrecto:

```python
Pedido.save(data)

if not Pedido.validar_pedido(data):
    ...
```

Correcto:

```python
if not Pedido.validar_pedido(data):
    return redirect(
        url_for("nuevo_pedido")
    )

Pedido.save(data)
```

---

## No convertir `cantidad`

Los datos provenientes del formulario llegan como texto.

Por ejemplo:

```text
"5"
```

Después de validar utilizamos:

```python
int(data["cantidad"])
```

para obtener:

```text
5
```

como entero.

---

## No utilizar `method="POST"`

El formulario debe tener:

```html
<form
    action="{{ url_for('crear_pedido') }}"
    method="POST"
>
```

---

## `name` incorrecto

Debe coincidir con `request.form`.

HTML:

```html
<input name="nombre">
```

Python:

```python
request.form.get("nombre")
```

HTML:

```html
<input name="tipo_arepa">
```

Python:

```python
request.form.get("tipo_arepa")
```

HTML:

```html
<input name="cantidad">
```

Python:

```python
request.form.get("cantidad")
```

---

# 🔄 Relación entre HTML y Python

```text
HTML
─────────────────────────────
name="nombre"
        ↓
request.form["nombre"]


name="tipo_arepa"
        ↓
request.form["tipo_arepa"]


name="cantidad"
        ↓
request.form["cantidad"]
```

---

# 🧠 Relación entre Controller y Model

El controlador:

```text
recibe información
```

El modelo:

```text
valida y trabaja con los datos
```

Por ejemplo:

```python
Pedido.validar_pedido(data)
```

y:

```python
Pedido.save(data)
```

El controlador decide cuándo ejecutar cada uno.

---

# 📚 Responsabilidad de cada archivo

| Archivo | Responsabilidad |
|---|---|
| `server.py` | Ejecutar aplicación |
| `__init__.py` | Crear aplicación Flask |
| `mysqlconnection.py` | Conectar con MySQL |
| `pedido.py` | Modelo, consultas y validación |
| `pedidos.py` | Rutas y flujo de la aplicación |
| `pedidos.html` | Listado de pedidos |
| `nuevo_pedido.html` | Formulario |
| `style.css` | Diseño |
| `esquema_arepas.sql` | Base de datos |
| `esquema_arepas_erd.mwb` | Modelo visual de BD |

---

# 🎓 Conceptos fundamentales

| Concepto | Función |
|---|---|
| `request.form` | Recuperar datos del formulario |
| `@staticmethod` | Crear una función auxiliar dentro de la clase |
| `validar_pedido()` | Comprobar reglas |
| `flash()` | Mostrar mensajes temporales |
| `secret_key` | Configuración necesaria para sesiones/flash |
| `render_template()` | Renderizar una plantilla |
| `redirect()` | Redirigir a otra ruta |
| `url_for()` | Generar una URL a partir de una función |
| `save()` | Insertar información |
| `get_all()` | Recuperar información |
| `Jinja2` | Mostrar datos dinámicos |
| `Pipenv` | Gestionar el entorno y dependencias |

---

# 🧠 Flujo de un dato

Ejemplo:

```text
Usuario escribe:

María
```

HTML:

```html
<input
    type="text"
    name="nombre"
>
```

↓

Flask:

```python
request.form.get("nombre")
```

↓

Diccionario:

```python
data = {
    "nombre": "María",
    ...
}
```

↓

Validación:

```python
Pedido.validar_pedido(data)
```

↓

Guardado:

```python
Pedido.save(data)
```

↓

SQL:

```text
INSERT INTO pedidos
```

↓

MySQL:

```text
María
```

---

# 🧠 ¿Qué ocurre si el dato es inválido?

Ejemplo:

```text
Nombre:
A
```

Flujo:

```text
A
 ↓
request.form
 ↓
data
 ↓
validar_pedido()
 ↓
len(nombre) < 2
 ↓
flash()
 ↓
False
 ↓
redirect()
 ↓
nuevo_pedido.html
```

No se ejecuta:

```text
INSERT
```

---

# 🧪 Resultado visual esperado

## `/pedidos`

```text
┌─────────────────────────────────────────────────────┐
│ Pedidos de Arepas                  [Nuevo Pedido]  │
│                                                     │
│ ID │ Nombre │ Tipo de Arepa       │ Cantidad       │
├────┼────────┼─────────────────────┼────────────────┤
│ 1  │ María  │ Arepa de queso      │ 2              │
│ 2  │ Carlos │ Arepa de carne      │ 3              │
│ 3  │ Ana    │ Arepa de pollo      │ 1              │
└─────────────────────────────────────────────────────┘
```

---

## `/pedidos/nuevo`

```text
┌──────────────────────────────────┐
│        Nuevo Pedido              │
│                                  │
│ Nombre                           │
│ [________________________]       │
│                                  │
│ Tipo de Arepa                    │
│ [________________________]       │
│                                  │
│ Cantidad                         │
│ [________________________]       │
│                                  │
│ [ Crear Pedido ] [ Volver ]      │
└──────────────────────────────────┘
```

En caso de error:

```text
┌──────────────────────────────────┐
│ ⚠ El nombre es obligatorio.     │
│ ⚠ La cantidad debe ser > 0.     │
└──────────────────────────────────┘
```

---

# 🧪 Comprobación final

La aplicación debe demostrar:

```text
CREATE
  ↓
Validación
  ↓
FLASH
  ↓
MYSQL
  ↓
READ
```

Específicamente:

```text
Formulario válido
        ↓
INSERT
        ↓
redirección
        ↓
listado
        ↓
nuevo pedido visible
```

y:

```text
Formulario inválido
        ↓
flash
        ↓
redirección
        ↓
formulario
        ↓
mensaje visible
        ↓
NO INSERT
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
[ ] Tabla pedidos creada
[ ] Datos de prueba insertados
[ ] ERD creado
[ ] ERD guardado en resources/

[ ] flask_app creado
[ ] __init__.py creado
[ ] secret_key configurada
[ ] mysqlconnection.py funciona

[ ] models/pedido.py creado
[ ] controllers/pedidos.py creado
[ ] templates/pedidos.html creado
[ ] templates/nuevo_pedido.html creado
[ ] static/css/style.css creado
[ ] server.py creado

[ ] GET / funciona
[ ] GET /pedidos funciona
[ ] GET /pedidos/nuevo funciona
[ ] POST /pedidos/crear funciona

[ ] Crear pedido funciona
[ ] Mostrar pedidos funciona
[ ] request.form funciona
[ ] @staticmethod funciona
[ ] validar_pedido() funciona
[ ] Todos los campos obligatorios
[ ] Nombre mínimo de 2 caracteres
[ ] Cantidad mayor que 0

[ ] flash() funciona
[ ] get_flashed_messages() funciona
[ ] redirect() funciona
[ ] url_for() funciona

[ ] Los datos inválidos NO se guardan
[ ] Los datos válidos SÍ se guardan
[ ] Los múltiples errores pueden mostrarse
[ ] La información aparece después de guardar
```

---

# 📦 Entregables

## 1. Repositorio GitHub

El repositorio debe incluir:

```text
pedidos_arepas/
│
├── flask_app/
├── resources/
├── Pipfile
├── Pipfile.lock
├── .gitignore
└── server.py
```

---

## 2. Evidencia

Entregar una captura de pantalla donde se observe la aplicación funcionando.

Idealmente mostrar:

```text
Listado de pedidos
+
Nuevo Pedido
+
al menos un registro creado
```

También es recomendable incluir una captura donde se observe un mensaje de validación funcionando.

---

## 3. ERD

La carpeta:

```text
resources/
```

debe contener:

```text
esquema_arepas_erd.mwb
```

---

# 🏁 Resultado final

Al finalizar tendrás una aplicación modularizada que implementa:

```text
                   FLASK
                     │
                     ▼
                 CONTROLLER
                     │
                     ▼
                 request.form
                     │
                     ▼
                  VALIDACIÓN
                     │
              ┌──────┴──────┐
              │             │
              ▼             ▼
           INVÁLIDO        VÁLIDO
              │             │
              ▼             ▼
           flash()       Pedido.save()
              │             │
              ▼             ▼
          redirect()      MySQL
                            │
                            ▼
                         redirect()
                            │
                            ▼
                         /pedidos
```

La actividad integra:

```text
Flask
+
MVC
+
POO
+
MySQL
+
PyMySQL
+
Jinja2
+
POST
+
request.form
+
Validación
+
@staticmethod
+
flash()
+
redirect()
+
url_for()
+
Pipenv
```

El concepto principal que debe quedar aprendido es:

> **Los datos de un formulario deben validarse en el backend antes de enviarse a la base de datos. Si existen errores, se informa al usuario mediante mensajes flash y se vuelve al formulario. Si los datos son válidos, se ejecuta el `INSERT` y se redirige al listado.**