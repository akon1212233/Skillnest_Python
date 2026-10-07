
# 👨‍🎓 Actualizar y eliminar registros con Flask + MySQL
![alt text](image.png)

> **Curso:** Desarrollo Web con Flask desde Cero  
> **Unidad:** Bases de Datos + CRUD  
> **Práctica:** UPDATE y DELETE  
> **Tecnologías:** Python · Flask · MySQL · PyMySQL · Jinja2 · POO · Pipenv · HTML5 · CSS3

---

# 📖 Descripción

Hasta este momento hemos aprendido a:

- conectar Flask con MySQL;
- consultar registros mediante `SELECT`;
- convertir registros de MySQL en objetos Python;
- crear nuevos registros utilizando formularios;
- utilizar `INSERT`;
- utilizar sentencias preparadas;
- trabajar con `request.form`;
- utilizar `redirect()`;
- utilizar `url_for()`.

Ahora completaremos las dos operaciones que faltan para construir un **CRUD completo**:

```text
C → CREATE → Crear
R → READ   → Leer
U → UPDATE → Actualizar
D → DELETE → Eliminar
```

En esta práctica trabajaremos específicamente con:

```text
UPDATE
DELETE
```

La aplicación permitirá administrar estudiantes almacenados en MySQL.

El usuario podrá:

- visualizar todos los estudiantes;
- ver un estudiante individual;
- abrir un formulario de edición;
- modificar sus datos;
- eliminar un estudiante;
- regresar al listado después de cada operación.

---

# 🎯 Objetivos

Al finalizar esta lección podrás:

- configurar un proyecto Flask utilizando Pipenv;
- conectar Flask con MySQL mediante PyMySQL;
- representar una tabla mediante POO;
- recuperar un registro específico utilizando su ID;
- utilizar rutas dinámicas con `<int:id_estudiante>`;
- construir formularios de edición;
- precargar valores existentes en inputs;
- ejecutar consultas `UPDATE`;
- ejecutar consultas `DELETE`;
- utilizar sentencias preparadas;
- utilizar `WHERE` correctamente;
- utilizar `request.form`;
- utilizar `redirect()`;
- utilizar `url_for()`;
- utilizar `confirm()` antes de eliminar;
- comprender por qué las operaciones destructivas requieren especial cuidado.

---

# 🧠 Resultado que construiremos

La aplicación final tendrá este flujo:

```text
                         ESTUDIANTES
                              │
                 ┌────────────┼────────────┐
                 │            │            │
                 ▼            ▼            ▼
                Ver         Editar       Eliminar
                 │            │            │
                 ▼            ▼            ▼
              Detalle      Formulario    DELETE
                              │            │
                              ▼            │
                            UPDATE         │
                              │            │
                              └─────┬──────┘
                                    │
                                    ▼
                                redirect()
                                    │
                                    ▼
                              /estudiantes
```

---

# 🗄️ Base de datos

Utilizaremos la base de datos:

```text
esquema_estudiantes
```

y la tabla:

```text
estudiantes
```

La estructura será:

```text
estudiantes
│
├── id_estudiante
├── nombre
├── email
└── created_at
```

---

# 📊 Estructura de la tabla

| Campo | Tipo | Función |
|---|---|---|
| `id_estudiante` | `INT` | Identificador único |
| `nombre` | `VARCHAR(100)` | Nombre del estudiante |
| `email` | `VARCHAR(100)` | Correo electrónico |
| `created_at` | `TIMESTAMP` | Fecha de creación |

El campo:

```text
id_estudiante
```

es:

```text
PRIMARY KEY
AUTO_INCREMENT
```

El campo:

```text
created_at
```

utiliza:

```text
DEFAULT CURRENT_TIMESTAMP
```

---

# 📁 Estructura final del proyecto

```text
estudiantes_app/
│
├── server.py
├── estudiante.py
├── mysqlconnection.py
├── schema.sql
├── Pipfile
├── Pipfile.lock
├── .gitignore
│
├── templates/
│   ├── estudiantes.html
│   ├── estudiante_ver.html
│   └── estudiante_editar.html
│
└── static/
    └── css/
        └── style.css
```

> `Pipfile.lock` es generado automáticamente por Pipenv. No es recomendable escribirlo manualmente. Debe generarse mediante `pipenv install` o `pipenv lock`.

---

# 🐍 1. Preparar el proyecto con Pipenv

## ¿Qué es Pipenv?

Pipenv permite administrar:

- el entorno virtual;
- las dependencias;
- las versiones de las librerías.

En lugar de instalar todo globalmente, cada proyecto tendrá su propio entorno.

La estructura conceptual es:

```text
Proyecto
   │
   ▼
Pipenv
   │
   ├── Entorno virtual
   ├── Flask
   └── PyMySQL
```

---

# 📦 Crear el entorno

Desde la carpeta del proyecto:

```bash
pipenv install flask
```

Luego:

```bash
pipenv install pymysql
```

Para ingresar al entorno:

```bash
pipenv shell
```

También podemos ejecutar directamente:

```bash
pipenv run python server.py
```

sin entrar manualmente al shell.

---

# 📄 `Pipfile`

Después de instalar las dependencias, Pipenv generará un archivo similar a:

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

Las versiones exactas pueden variar según el entorno y la fecha de instalación.

---

# 🔒 `Pipfile.lock`

Pipenv generará automáticamente:

```text
Pipfile.lock
```

Este archivo fija las versiones exactas y hashes de las dependencias.

No debemos escribirlo manualmente.

Después de clonar el proyecto, podemos utilizar:

```bash
pipenv install
```

para reconstruir el entorno utilizando el `Pipfile.lock`.

---

# 🚫 `.gitignore`

```text
venv/
.venv/
__pycache__/
*.pyc
.env
```

---

# 🗄️ 2. Crear la base de datos

## `schema.sql`

```sql
-- ==========================================================
-- CREAR BASE DE DATOS
-- ==========================================================

CREATE DATABASE IF NOT EXISTS esquema_estudiantes;

USE esquema_estudiantes;


-- ==========================================================
-- CREAR TABLA
-- ==========================================================

CREATE TABLE IF NOT EXISTS estudiantes (

    id_estudiante INT AUTO_INCREMENT PRIMARY KEY,

    nombre VARCHAR(100),

    email VARCHAR(100),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);


-- ==========================================================
-- INSERTAR DATOS DE PRUEBA
-- ==========================================================

INSERT INTO estudiantes
(
    nombre,
    email
)
VALUES
(
    "Joe Doe",
    "joedoe@email.com"
),
(
    "Ana Pérez",
    "ana@email.com"
),
(
    "Carlos Soto",
    "carlos@email.com"
),
(
    "María González",
    "maria@email.com"
);
```

---

# 🔍 Analizando la tabla

## `PRIMARY KEY`

```sql
id_estudiante INT AUTO_INCREMENT PRIMARY KEY
```

significa que:

```text
id_estudiante
```

identifica de manera única cada estudiante.

Ejemplo:

```text
1 → Joe Doe
2 → Ana Pérez
3 → Carlos Soto
4 → María González
```

---

## `AUTO_INCREMENT`

MySQL genera automáticamente el ID.

No debemos escribir:

```sql
INSERT INTO estudiantes
(id_estudiante, nombre, email)
...
```

Para crear un estudiante normalmente enviamos:

```sql
nombre
email
```

y MySQL genera:

```text
id_estudiante
```

---

## `created_at`

```sql
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

permite registrar automáticamente el momento en que se crea el registro.

---

# 🔎 Comprobar la base de datos

En MySQL Workbench:

```sql
USE esquema_estudiantes;

DESCRIBE estudiantes;
```

También:

```sql
SELECT *
FROM estudiantes;
```

Deberíamos obtener algo similar a:

```text
id_estudiante | nombre            | email
--------------|-------------------|----------------------
1             | Joe Doe           | joedoe@email.com
2             | Ana Pérez         | ana@email.com
3             | Carlos Soto       | carlos@email.com
4             | María González    | maria@email.com
```

---

# 🔌 3. Conexión con MySQL

## `mysqlconnection.py`

Este archivo será responsable de establecer la conexión y ejecutar nuestras consultas.

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
    Administra una conexión entre Python y MySQL.
    """

    def __init__(self, db):
        """
        Recibe el nombre de la base de datos
        y establece la conexión.
        """

        self.connection = pymysql.connect(

            host="localhost",

            user="root",

            password="root",

            database=db,

            charset="utf8mb4",

            cursorclass=pymysql.cursors.DictCursor,

            autocommit=True

        )


    # ======================================================
    # EJECUTAR CONSULTA
    # ======================================================

    def query_db(self, query, data=None):
        """
        Ejecuta una consulta SQL.

        SELECT:
            devuelve una lista de diccionarios.

        INSERT:
            devuelve el ID generado.

        UPDATE / DELETE:
            no devuelven una lista de registros.

        Error:
            devuelve False.
        """

        with self.connection.cursor() as cursor:

            try:

                # --------------------------------------------------
                # Ejecutar consulta con parámetros.
                # --------------------------------------------------

                cursor.execute(
                    query,
                    data
                )


                # --------------------------------------------------
                # SELECT
                # --------------------------------------------------

                if query.strip().lower().startswith("select"):

                    resultados = cursor.fetchall()

                    return resultados


                # --------------------------------------------------
                # INSERT
                # --------------------------------------------------

                elif query.strip().lower().startswith("insert"):

                    return cursor.lastrowid


                # --------------------------------------------------
                # UPDATE / DELETE
                # --------------------------------------------------

                else:

                    return None


            except Exception as e:

                print(
                    "Something went wrong:"
                )

                print(e)

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
    Recibe el nombre de la base de datos
    y devuelve una instancia de MySQLConnection.
    """

    return MySQLConnection(db)
```

---

# 🔐 Configurar credenciales

Debes modificar:

```python
user="root",
password="root",
```

según las credenciales de tu instalación local.

Por ejemplo:

```python
user="root",
password="MiClave123",
```

En una aplicación real no deberíamos mantener estas credenciales directamente en el código.

Posteriormente podemos utilizar variables de entorno.

---

# 👨‍🎓 4. Crear el modelo `Estudiante`

El archivo:

```text
estudiante.py
```

representará la tabla:

```text
estudiantes
```

---

# 📄 `estudiante.py`

```python
# ==========================================================
# MODELO ESTUDIANTE
# ==========================================================

from mysqlconnection import connectToMySQL


# ==========================================================
# CLASE ESTUDIANTE
# ==========================================================

class Estudiante:
    """
    Representa un registro de la tabla estudiantes.
    """

    def __init__(self, data):
        """
        Recibe un diccionario proveniente de MySQL
        y lo convierte en un objeto Estudiante.
        """

        self.id_estudiante = data["id_estudiante"]

        self.nombre = data["nombre"]

        self.email = data["email"]

        self.created_at = data["created_at"]


    # ======================================================
    # READ
    # OBTENER TODOS
    # ======================================================

    @classmethod
    def get_all(cls):
        """
        Recupera todos los estudiantes.
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
            "esquema_estudiantes"
        ).query_db(query)


        estudiantes = []


        for estudiante in resultados:

            estudiantes.append(
                cls(estudiante)
            )


        return estudiantes


    # ======================================================
    # READ
    # OBTENER UNO POR ID
    # ======================================================

    @classmethod
    def get_by_id(cls, id_estudiante):
        """
        Busca un estudiante específico mediante su ID.

        Si existe:
            devuelve un objeto Estudiante.

        Si no existe:
            devuelve None.
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
            "esquema_estudiantes"
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
    # UPDATE
    # ACTUALIZAR ESTUDIANTE
    # ======================================================

    @classmethod
    def actualizar(cls, data):
        """
        Actualiza el nombre y email de un estudiante.

        data debe contener:

        id_estudiante
        nombre
        email
        """

        query = """
            UPDATE estudiantes
            SET
                nombre = %(nombre)s,
                email = %(email)s
            WHERE id_estudiante = %(id_estudiante)s;
        """


        return connectToMySQL(
            "esquema_estudiantes"
        ).query_db(
            query,
            data
        )


    # ======================================================
    # DELETE
    # ELIMINAR ESTUDIANTE
    # ======================================================

    @classmethod
    def eliminar(cls, data):
        """
        Elimina un estudiante mediante su ID.
        """

        query = """
            DELETE FROM estudiantes
            WHERE id_estudiante = %(id_estudiante)s;
        """


        return connectToMySQL(
            "esquema_estudiantes"
        ).query_db(
            query,
            data
        )
```

---

# 🧠 ¿Qué hemos agregado?

Nuestra clase ahora tiene cuatro operaciones:

```text
Estudiante
│
├── get_all()
│       ↓
│     SELECT
│
├── get_by_id()
│       ↓
│     SELECT + WHERE
│
├── actualizar()
│       ↓
│     UPDATE
│
└── eliminar()
        ↓
      DELETE
```

---

# 🔍 5. `get_by_id()`

Necesitamos recuperar un solo estudiante.

Por ejemplo:

```python
Estudiante.get_by_id(3)
```

La consulta utiliza:

```sql
SELECT
    id_estudiante,
    nombre,
    email,
    created_at
FROM estudiantes
WHERE id_estudiante = %(id_estudiante)s;
```

El diccionario:

```python
data = {
    "id_estudiante": 3
}
```

Esto significa:

```text
URL
 ↓
id_estudiante = 3
 ↓
get_by_id(3)
 ↓
SELECT ... WHERE id_estudiante = 3
 ↓
MySQL
 ↓
objeto Estudiante
```

---

# ✏️ 6. `UPDATE`

## ¿Qué hace `UPDATE`?

`UPDATE` permite modificar información de un registro existente.

Ejemplo directo en MySQL:

```sql
UPDATE estudiantes
SET
    nombre = "Joe Doe",
    email = "joedoe@email.com"
WHERE id_estudiante = 2;
```

Este comando modifica solamente al estudiante:

```text
id_estudiante = 2
```

---

# 🧠 Estructura de `UPDATE`

La sintaxis general es:

```sql
UPDATE tabla
SET
    campo = valor
WHERE condición;
```

En nuestro caso:

```sql
UPDATE estudiantes
SET
    nombre = %(nombre)s,
    email = %(email)s
WHERE id_estudiante = %(id_estudiante)s;
```

---

# ⚠️ `WHERE` es fundamental

Observa:

```sql
UPDATE estudiantes
SET nombre = "Pedro";
```

Esta consulta modificaría:

```text
TODOS los estudiantes
```

En cambio:

```sql
UPDATE estudiantes
SET nombre = "Pedro"
WHERE id_estudiante = 3;
```

modifica únicamente:

```text
estudiante 3
```

Por eso:

> **Nunca debes olvidar el `WHERE` cuando quieres actualizar un registro específico.**

---

# 🗑️ 7. `DELETE`

## ¿Qué hace `DELETE`?

`DELETE` elimina registros de una tabla.

Ejemplo:

```sql
DELETE FROM estudiantes
WHERE id_estudiante = 3;
```

Esto elimina:

```text
estudiante 3
```

---

# ⚠️ `DELETE` también necesita `WHERE`

Nunca ejecutes:

```sql
DELETE FROM estudiantes;
```

a menos que realmente quieras eliminar **todos los registros**.

Para eliminar un estudiante específico:

```sql
DELETE FROM estudiantes
WHERE id_estudiante = 3;
```

---

# 👨‍💻 8. `server.py`

Ahora construiremos el controlador de nuestra aplicación.

Tendrá las siguientes rutas:

```text
GET  /estudiantes
GET  /estudiantes/ver/<int:id_estudiante>
GET  /estudiantes/editar/<int:id_estudiante>
POST /actualizar_estudiante
GET  /eliminar_estudiante/<int:id_estudiante>
```

---

# 📄 `server.py`

```python
# ==========================================================
# SERVIDOR FLASK
# ==========================================================

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for
)


from estudiante import Estudiante


# ==========================================================
# CREAR APLICACIÓN
# ==========================================================

app = Flask(__name__)


# ==========================================================
# READ
# LISTAR ESTUDIANTES
# ==========================================================

@app.route("/estudiantes")
def estudiantes():
    """
    Muestra todos los estudiantes.
    """

    lista_estudiantes = Estudiante.get_all()


    return render_template(
        "estudiantes.html",
        estudiantes=lista_estudiantes
    )


# ==========================================================
# READ
# VER ESTUDIANTE
# ==========================================================

@app.route(
    "/estudiantes/ver/<int:id_estudiante>"
)
def ver_estudiante(id_estudiante):
    """
    Muestra la información de un estudiante específico.
    """

    estudiante = Estudiante.get_by_id(
        id_estudiante
    )


    # ------------------------------------------------------
    # Verificar si existe.
    # ------------------------------------------------------

    if estudiante is None:

        return (
            "Estudiante no encontrado",
            404
        )


    return render_template(
        "estudiante_ver.html",
        estudiante=estudiante
    )


# ==========================================================
# UPDATE
# MOSTRAR FORMULARIO
# ==========================================================

@app.route(
    "/estudiantes/editar/<int:id_estudiante>"
)
def editar_estudiante(id_estudiante):
    """
    Recupera un estudiante y muestra
    el formulario de edición.
    """

    estudiante = Estudiante.get_by_id(
        id_estudiante
    )


    if estudiante is None:

        return (
            "Estudiante no encontrado",
            404
        )


    return render_template(
        "estudiante_editar.html",
        estudiante=estudiante
    )


# ==========================================================
# UPDATE
# PROCESAR ACTUALIZACIÓN
# ==========================================================

@app.route(
    "/actualizar_estudiante",
    methods=["POST"]
)
def actualizar_estudiante():
    """
    Recibe los datos del formulario
    y actualiza el estudiante.
    """

    # ------------------------------------------------------
    # OBTENER DATOS
    # ------------------------------------------------------

    id_estudiante = request.form[
        "id_estudiante"
    ]

    nombre = request.form[
        "nombre"
    ].strip()

    email = request.form[
        "email"
    ].strip()


    # ------------------------------------------------------
    # VALIDACIÓN
    # ------------------------------------------------------

    if not nombre or not email:

        estudiante = Estudiante.get_by_id(
            int(id_estudiante)
        )


        return render_template(
            "estudiante_editar.html",
            estudiante=estudiante,
            error="Todos los campos son obligatorios."
        )


    # ------------------------------------------------------
    # CREAR DICCIONARIO
    # ------------------------------------------------------

    data = {

        "id_estudiante": id_estudiante,

        "nombre": nombre,

        "email": email

    }


    # ------------------------------------------------------
    # ACTUALIZAR
    # ------------------------------------------------------

    resultado = Estudiante.actualizar(
        data
    )


    # ------------------------------------------------------
    # COMPROBAR ERROR
    # ------------------------------------------------------

    if resultado is False:

        estudiante = Estudiante.get_by_id(
            int(id_estudiante)
        )


        return render_template(
            "estudiante_editar.html",
            estudiante=estudiante,
            error="No fue posible actualizar el estudiante."
        )


    # ------------------------------------------------------
    # REDIRECT
    # ------------------------------------------------------

    return redirect(
        url_for("estudiantes")
    )


# ==========================================================
# DELETE
# ELIMINAR ESTUDIANTE
# ==========================================================

@app.route(
    "/eliminar_estudiante/<int:id_estudiante>"
)
def eliminar_estudiante(id_estudiante):
    """
    Elimina un estudiante y vuelve al listado.
    """

    data = {

        "id_estudiante": id_estudiante

    }


    resultado = Estudiante.eliminar(
        data
    )


    if resultado is False:

        return (
            "No fue posible eliminar el estudiante.",
            500
        )


    return redirect(
        url_for("estudiantes")
    )


# ==========================================================
# EJECUTAR SERVIDOR
# ==========================================================

if __name__ == "__main__":

    app.run(debug=True)
```

---

# 🧠 9. Rutas dinámicas

Observa:

```python
@app.route(
    "/estudiantes/ver/<int:id_estudiante>"
)
```

Si visitamos:

```text
/estudiantes/ver/3
```

Flask recibe:

```python
id_estudiante = 3
```

La parte:

```text
<int:id_estudiante>
```

indica:

> "Esta parte de la URL debe ser un número entero y se almacenará en la variable `id_estudiante`."

---

# 🔄 Flujo de una ruta dinámica

```text
/estudiantes/ver/3
        ↓
id_estudiante = 3
        ↓
Estudiante.get_by_id(3)
        ↓
SELECT
        ↓
MySQL
        ↓
objeto Estudiante
        ↓
estudiante_ver.html
```

---

# 📝 10. Formulario de edición

El formulario debe recibir el ID del estudiante.

Utilizaremos:

```html
<input
    type="hidden"
    name="id_estudiante"
    value="{{ estudiante.id_estudiante }}"
>
```

---

# 🧠 ¿Qué es `type="hidden"`?

Es un campo que:

- existe dentro del formulario;
- se envía al servidor;
- pero no aparece visualmente para el usuario.

Por ejemplo:

```html
<input
    type="hidden"
    name="id_estudiante"
    value="3"
>
```

El usuario no lo ve, pero Flask recibe:

```python
request.form["id_estudiante"]
```

Esto nos permite saber qué estudiante debe modificarse.

---

# 📄 `templates/estudiantes.html`

Esta será nuestra página principal.

```html
<!DOCTYPE html>
<html lang="es">

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>Estudiantes</title>


    <!-- ==================================================
         BOOTSTRAP
    =================================================== -->

    <link
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.7/dist/css/bootstrap.min.css"
        rel="stylesheet"
    >


    <!-- ==================================================
         CSS PROPIO
    =================================================== -->

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
                Estudiantes
            </h1>

            <p class="text-muted">

                Listado de estudiantes registrados.

            </p>

        </div>

    </div>


    <!-- ==================================================
         TABLA
    =================================================== -->

    <div class="card shadow-sm border-0">

        <div class="card-body p-0">


            {% if estudiantes %}


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
                                    Email
                                </th>

                                <th>
                                    Fecha Creación
                                </th>

                                <th>
                                    Acciones
                                </th>

                            </tr>

                        </thead>


                        <tbody>

                            {% for estudiante in estudiantes %}


                                <tr>

                                    <td>
                                        {{ estudiante.id_estudiante }}
                                    </td>


                                    <td>
                                        {{ estudiante.nombre }}
                                    </td>


                                    <td>
                                        {{ estudiante.email }}
                                    </td>


                                    <td>

                                        {% if estudiante.created_at %}

                                            {{ estudiante.created_at.strftime("%Y-%m-%d") }}

                                        {% endif %}

                                    </td>


                                    <td>

                                        <div class="acciones">


                                            <!-- VER -->

                                            <a
                                                href="{{ url_for('ver_estudiante', id_estudiante=estudiante.id_estudiante) }}"
                                                class="btn btn-sm btn-outline-primary"
                                            >
                                                Ver
                                            </a>


                                            <!-- EDITAR -->

                                            <a
                                                href="{{ url_for('editar_estudiante', id_estudiante=estudiante.id_estudiante) }}"
                                                class="btn btn-sm btn-outline-warning"
                                            >
                                                Editar
                                            </a>


                                            <!-- ELIMINAR -->

                                            <a
                                                href="{{ url_for('eliminar_estudiante', id_estudiante=estudiante.id_estudiante) }}"
                                                class="btn btn-sm btn-outline-danger"
                                                onclick="return confirm('¿Estás seguro de eliminar este estudiante?');"
                                            >
                                                Eliminar
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
                        No existen estudiantes.
                    </h3>

                </div>


            {% endif %}


        </div>

    </div>

</div>

</body>

</html>
```

---

# 👁️ 11. Ver un estudiante

## `templates/estudiante_ver.html`

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
        Estudiante {{ estudiante.id_estudiante }}
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

            Estudiante
            {{ estudiante.id_estudiante }}

        </h1>


        <p class="text-muted">

            Información del estudiante.

        </p>


        <hr>


        <div class="user-detail">


            <p>

                <strong>
                    Nombre:
                </strong>

                {{ estudiante.nombre }}

            </p>


            <p>

                <strong>
                    E-mail:
                </strong>

                {{ estudiante.email }}

            </p>


            <p>

                <strong>
                    Fecha de creación:
                </strong>

                {{ estudiante.created_at }}

            </p>


        </div>


        <!-- ==================================================
             ACCIONES
        =================================================== -->

        <div class="mt-4">


            <a
                href="{{ url_for('editar_estudiante', id_estudiante=estudiante.id_estudiante) }}"
                class="btn btn-warning"
            >
                Editar
            </a>


            <a
                href="{{ url_for('eliminar_estudiante', id_estudiante=estudiante.id_estudiante) }}"
                class="btn btn-danger"
                onclick="return confirm('¿Estás seguro de eliminar este estudiante?');"
            >
                Eliminar
            </a>


            <a
                href="{{ url_for('estudiantes') }}"
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

# ✏️ 12. Formulario de edición

## `templates/estudiante_editar.html`

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
        Editar estudiante
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


    <div class="row justify-content-center">

        <div class="col-lg-6">


            <div class="page-header">

                <div>

                    <h1>
                        Editar estudiante
                    </h1>

                    <p class="text-muted">

                        Modifica la información del estudiante.

                    </p>

                </div>

            </div>


            <div class="card shadow-sm border-0">

                <div class="card-body p-4">


                    {% if error %}

                        <div class="alert alert-danger">

                            {{ error }}

                        </div>

                    {% endif %}


                    <!-- ==================================================
                         FORMULARIO
                    =================================================== -->

                    <form
                        action="{{ url_for('actualizar_estudiante') }}"
                        method="POST"
                    >


                        <!-- ID -->

                        <input
                            type="hidden"
                            name="id_estudiante"
                            value="{{ estudiante.id_estudiante }}"
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
                                value="{{ estudiante.nombre }}"
                                maxlength="100"
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
                                value="{{ estudiante.email }}"
                                maxlength="100"
                                required
                            >

                        </div>


                        <!-- BOTONES -->

                        <div class="d-flex gap-2">


                            <button
                                type="submit"
                                class="btn btn-success"
                            >
                                Actualizar
                            </button>


                            <a
                                href="{{ url_for('ver_estudiante', id_estudiante=estudiante.id_estudiante) }}"
                                class="btn btn-outline-secondary"
                            >
                                Cancelar
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

# 🎨 13. CSS

## `static/css/style.css`

```css
/* ==========================================================
   ESTUDIANTES
========================================================== */

body {
    background-color: #f5f6f8;
    font-family: Arial, Helvetica, sans-serif;
    color: #212529;
}


h1 {
    font-weight: 700;
}


.card,
.detail-card {
    border-radius: 10px;
}


.page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 20px;
    margin-bottom: 25px;
}


.page-header h1 {
    margin-bottom: 5px;
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


.detail-card {
    max-width: 800px;
    margin: 0 auto;
    padding: 35px;
    background-color: #ffffff;
    box-shadow: 0 4px 18px rgba(0, 0, 0, 0.08);
}


.user-detail {
    margin-top: 20px;
    padding: 25px;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    background-color: #fafafa;
}


.user-detail p {
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

    .page-header {
        align-items: flex-start;
        flex-direction: column;
    }


    .acciones {
        flex-direction: column;
    }


    .acciones .btn {
        width: 100%;
    }

}


@media (max-width: 576px) {

    .detail-card {
        padding: 20px;
    }

}
```

---

# 🧠 14. Comprendiendo UPDATE

La operación:

```sql
UPDATE estudiantes
SET
    nombre = %(nombre)s,
    email = %(email)s
WHERE id_estudiante = %(id_estudiante)s;
```

tiene tres partes fundamentales.

## `UPDATE`

Indica que vamos a modificar un registro.

```sql
UPDATE estudiantes
```

---

## `SET`

Indica qué columnas cambiarán:

```sql
SET
    nombre = %(nombre)s,
    email = %(email)s
```

---

## `WHERE`

Indica qué registro queremos modificar:

```sql
WHERE id_estudiante = %(id_estudiante)s
```

El flujo completo es:

```text
UPDATE estudiantes
      ↓
SET nuevos valores
      ↓
WHERE identifica registro
```

---

# 🔢 Ejemplo

Tenemos:

```text
id_estudiante: 2
nombre: Joe Doe
email: joedoe@email.com
```

El usuario cambia:

```text
nombre: Joe Smith
email: joesmith@email.com
```

El servidor construye:

```python
data = {
    "id_estudiante": 2,
    "nombre": "Joe Smith",
    "email": "joesmith@email.com"
}
```

La consulta:

```sql
UPDATE estudiantes
SET
    nombre = %(nombre)s,
    email = %(email)s
WHERE id_estudiante = %(id_estudiante)s;
```

modifica únicamente:

```text
ID 2
```

---

# 🔄 Flujo de UPDATE

```text
/estudiantes
      ↓
Editar
      ↓
/estudiantes/editar/2
      ↓
get_by_id(2)
      ↓
mostrar formulario
      ↓
usuario modifica datos
      ↓
POST /actualizar_estudiante
      ↓
request.form
      ↓
data
      ↓
Estudiante.actualizar(data)
      ↓
UPDATE
      ↓
redirect()
      ↓
/estudiantes
```

---

# 🗑️ 15. Comprendiendo DELETE

La consulta:

```sql
DELETE FROM estudiantes
WHERE id_estudiante = %(id_estudiante)s;
```

significa:

> Elimina de la tabla `estudiantes` el registro cuyo `id_estudiante` coincida con el valor recibido.

Por ejemplo:

```python
data = {
    "id_estudiante": 3
}
```

produce conceptualmente:

```sql
DELETE FROM estudiantes
WHERE id_estudiante = 3;
```

---

# ⚠️ DELETE es irreversible

Cuando eliminamos:

```sql
DELETE FROM estudiantes
WHERE id_estudiante = 3;
```

el registro desaparece de la tabla.

Por eso la aplicación incorporará una confirmación visual:

```javascript
confirm(
    "¿Estás seguro de eliminar este estudiante?"
)
```

---

# 🟡 16. `confirm()`

Utilizamos:

```html
onclick="return confirm('¿Estás seguro de eliminar este estudiante?');"
```

Cuando el usuario presiona:

```text
Eliminar
```

aparece:

```text
¿Estás seguro de eliminar este estudiante?

[Cancelar] [Aceptar]
```

Si pulsa:

```text
Aceptar
```

`confirm()` devuelve:

```javascript
true
```

y el navegador continúa hacia la URL.

Si pulsa:

```text
Cancelar
```

devuelve:

```javascript
false
```

y el navegador cancela la navegación.

---

# ⚠️ Importante sobre `confirm()`

`confirm()` es una protección de **interfaz**.

No reemplaza las validaciones del backend.

Por ejemplo, un usuario podría escribir directamente una URL.

Por eso el servidor igualmente debe controlar:

- existencia del ID;
- permisos;
- autenticación;
- autorización.

En esta práctica todavía estamos trabajando con un CRUD básico, por lo que utilizaremos `confirm()` para mejorar la experiencia del usuario.

---

# 🔐 17. ¿Por qué DELETE mediante GET?

La práctica utiliza:

```text
/eliminar_estudiante/<id>
```

como enlace.

Esto facilita el aprendizaje inicial:

```text
clic
 ↓
ruta
 ↓
delete()
 ↓
redirect()
```

Sin embargo, en una aplicación de producción **no es recomendable utilizar GET para una operación destructiva**.

Una alternativa más apropiada sería:

```text
POST /estudiantes/<id>/eliminar
```

o:

```text
DELETE /estudiantes/<id>
```

Esto es importante porque `GET` debería representar principalmente una operación segura de lectura.

---

# 🧠 18. `redirect()` en UPDATE

Después de actualizar:

```python
Estudiante.actualizar(data)
```

utilizamos:

```python
return redirect(
    url_for("estudiantes")
)
```

Por lo tanto:

```text
POST
 ↓
UPDATE
 ↓
redirect()
 ↓
GET
```

Esto es el patrón:

```text
POST → Redirect → GET
```

---

# 🧠 19. `redirect()` en DELETE

Después de:

```python
Estudiante.eliminar(data)
```

utilizamos:

```python
return redirect(
    url_for("estudiantes")
)
```

Entonces:

```text
DELETE
 ↓
redirect()
 ↓
GET /estudiantes
```

El usuario vuelve al listado y puede comprobar que el registro desapareció.

---

# 👀 20. Vista individual

Si abrimos:

```text
http://127.0.0.1:5000/estudiantes/ver/3
```

Flask recibe:

```python
id_estudiante = 3
```

ejecuta:

```python
Estudiante.get_by_id(3)
```

y envía:

```python
estudiante
```

a:

```text
estudiante_ver.html
```

---

# ✏️ 21. Vista de edición

Si abrimos:

```text
http://127.0.0.1:5000/estudiantes/editar/3
```

Flask realiza:

```python
Estudiante.get_by_id(3)
```

y el formulario recibe:

```jinja
value="{{ estudiante.nombre }}"
```

```jinja
value="{{ estudiante.email }}"
```

Por ejemplo:

```html
<input
    value="Joe Doe"
>
```

y:

```html
<input
    value="joedoe@email.com"
>
```

---

# 🔗 22. `url_for()` con parámetros

Para ver:

```jinja
{{ url_for(
    "ver_estudiante",
    id_estudiante=estudiante.id_estudiante
) }}
```

Si:

```text
estudiante.id_estudiante = 3
```

genera:

```text
/estudiantes/ver/3
```

Para editar:

```jinja
{{ url_for(
    "editar_estudiante",
    id_estudiante=estudiante.id_estudiante
) }}
```

genera:

```text
/estudiantes/editar/3
```

Para eliminar:

```jinja
{{ url_for(
    "eliminar_estudiante",
    id_estudiante=estudiante.id_estudiante
) }}
```

genera:

```text
/eliminar_estudiante/3
```

---

# 🧪 23. Prueba completa

## READ

Inicia la aplicación:

```bash
pipenv run python server.py
```

Visita:

```text
http://127.0.0.1:5000/estudiantes
```

Deberás observar una tabla similar a:

```text
┌────┬────────────────┬─────────────────────┬───────────────┬──────────────────────┐
│ ID │ Nombre         │ Email               │ Fecha         │ Acciones             │
├────┼────────────────┼─────────────────────┼───────────────┼──────────────────────┤
│ 1  │ Joe Doe        │ joedoe@email.com    │ 2026-09-21    │ Ver Editar Eliminar  │
│ 2  │ Ana Pérez      │ ana@email.com        │ 2026-09-21    │ Ver Editar Eliminar  │
│ 3  │ Carlos Soto    │ carlos@email.com     │ 2026-09-21    │ Ver Editar Eliminar  │
└────┴────────────────┴─────────────────────┴───────────────┴──────────────────────┘
```

---

# ✏️ 24. Probar UPDATE

Selecciona:

```text
Editar
```

para el estudiante:

```text
ID 2
```

Se abrirá:

```text
/estudiantes/editar/2
```

El formulario debería mostrar:

```text
Nombre:
Ana Pérez

Email:
ana@email.com
```

Modifica:

```text
Nombre:
Ana María Pérez
```

y:

```text
Email:
anamaria@email.com
```

Presiona:

```text
Actualizar
```

El navegador volverá a:

```text
/estudiantes
```

y el listado deberá mostrar los datos modificados.

---

# 🔎 25. Comprobar UPDATE en MySQL

Utiliza:

```sql
USE esquema_estudiantes;

SELECT *
FROM estudiantes
WHERE id_estudiante = 2;
```

Deberás encontrar el registro actualizado.

---

# 🗑️ 26. Probar DELETE

En el listado selecciona:

```text
Eliminar
```

Aparecerá:

```text
¿Estás seguro de eliminar este estudiante?
```

Selecciona:

```text
Aceptar
```

El registro será eliminado.

Después:

```text
redirect()
 ↓
/estudiantes
```

y deberá desaparecer de la tabla.

---

# 🔎 27. Comprobar DELETE en MySQL

Ejecuta:

```sql
SELECT *
FROM estudiantes
WHERE id_estudiante = 3;
```

Si el usuario fue eliminado correctamente, la consulta no deberá devolver registros.

---

# 🧠 28. Flujo completo del CRUD

## CREATE

```text
Formulario
   ↓
POST
   ↓
request.form
   ↓
data
   ↓
INSERT
   ↓
redirect()
   ↓
GET
```

---

## READ

```text
GET /estudiantes
   ↓
get_all()
   ↓
SELECT
   ↓
objetos Estudiante
   ↓
Jinja2
   ↓
HTML
```

---

## UPDATE

```text
GET formulario
   ↓
get_by_id()
   ↓
precargar formulario
   ↓
POST
   ↓
request.form
   ↓
update()
   ↓
UPDATE
   ↓
redirect()
   ↓
GET listado
```

---

## DELETE

```text
Eliminar
   ↓
confirm()
   ↓
ruta
   ↓
delete()
   ↓
DELETE
   ↓
redirect()
   ↓
GET listado
```

---

# 🧩 29. Arquitectura completa

```text
                         NAVEGADOR
                              │
                              ▼
                           Flask
                              │
                ┌─────────────┼──────────────┐
                │             │              │
                ▼             ▼              ▼
             GET READ       UPDATE         DELETE
                │             │              │
                └─────────────┼──────────────┘
                              │
                              ▼
                        Estudiante
                           modelo
                              │
                              ▼
                     MySQLConnection
                              │
                              ▼
                           PyMySQL
                              │
                              ▼
                            MySQL
```

---

# 📊 30. CRUD y SQL

| Operación | Método Python | SQL |
|---|---|---|
| Create | `guardar()` | `INSERT` |
| Read todos | `get_all()` | `SELECT` |
| Read uno | `get_by_id()` | `SELECT ... WHERE` |
| Update | `actualizar()` | `UPDATE` |
| Delete | `eliminar()` | `DELETE` |

---

# ⚠️ 31. Errores comunes

## `ModuleNotFoundError`

Si aparece:

```text
No module named 'flask'
```

o:

```text
No module named 'pymysql'
```

revisa que Pipenv esté activo:

```bash
pipenv shell
```

o instala:

```bash
pipenv install flask
pipenv install pymysql
```

---

## Error de conexión MySQL

Revisa:

```python
host="localhost"
user="root"
password="..."
database="esquema_estudiantes"
```

---

## Error `BuildError`

Si utilizas:

```jinja
url_for("ver_estudiante")
```

pero tu función se llama:

```python
def ver_estudiante(id_estudiante):
```

la URL dinámica necesita:

```jinja
url_for(
    "ver_estudiante",
    id_estudiante=estudiante.id_estudiante
)
```

---

## `BadRequestKeyError`

Si Python utiliza:

```python
request.form["nombre"]
```

el formulario debe contener:

```html
name="nombre"
```

---

## El formulario aparece vacío

Revisa:

```jinja
value="{{ estudiante.nombre }}"
```

y:

```jinja
value="{{ estudiante.email }}"
```

---

## Todos los estudiantes se actualizaron

Probablemente falta:

```sql
WHERE id_estudiante = %(id_estudiante)s
```

---

## Todos los estudiantes fueron eliminados

Probablemente se ejecutó:

```sql
DELETE FROM estudiantes;
```

en lugar de:

```sql
DELETE FROM estudiantes
WHERE id_estudiante = %(id_estudiante)s;
```

---

## Se actualiza pero no vuelve al listado

Comprueba:

```python
return redirect(
    url_for("estudiantes")
)
```

---

## Se elimina pero el usuario sigue apareciendo

Comprueba:

```python
Estudiante.eliminar(data)
```

y:

```python
redirect()
```

También revisa directamente MySQL:

```sql
SELECT *
FROM estudiantes;
```

---

# ✅ 32. Checklist final

```text
[ ] Pipenv configurado
[ ] Flask instalado
[ ] PyMySQL instalado
[ ] Pipfile creado
[ ] Pipfile.lock generado
[ ] Base de datos creada
[ ] Tabla estudiantes creada

[ ] mysqlconnection.py funciona
[ ] Estudiante.get_all() funciona
[ ] Estudiante.get_by_id() funciona
[ ] Estudiante.actualizar() funciona
[ ] Estudiante.eliminar() funciona

[ ] GET /estudiantes funciona
[ ] GET /estudiantes/ver/<id> funciona
[ ] GET /estudiantes/editar/<id> funciona
[ ] POST /actualizar_estudiante funciona
[ ] GET /eliminar_estudiante/<id> funciona

[ ] Formulario de edición funciona
[ ] Los valores aparecen precargados
[ ] UPDATE funciona
[ ] DELETE funciona
[ ] WHERE está presente en UPDATE
[ ] WHERE está presente en DELETE
[ ] confirm() funciona
[ ] redirect() funciona
[ ] url_for() funciona
[ ] Jinja2 funciona
[ ] La base de datos refleja los cambios
```

---

# 🏁 33. Resultado final

La aplicación ahora permite administrar estudiantes utilizando las cuatro operaciones fundamentales:

```text
┌───────────────────────────────────────┐
│                CRUD                   │
├───────────────────────────────────────┤
│                                       │
│ CREATE → INSERT                       │
│                                       │
│ READ   → SELECT                       │
│                                       │
│ UPDATE → UPDATE                       │
│                                       │
│ DELETE → DELETE                       │
│                                       │
└───────────────────────────────────────┘
```

El flujo de actualización:

```text
/estudiantes/editar/3
        ↓
get_by_id(3)
        ↓
formulario
        ↓
POST
        ↓
request.form
        ↓
Estudiante.actualizar()
        ↓
UPDATE
        ↓
redirect()
        ↓
/estudiantes
```

El flujo de eliminación:

```text
Eliminar
   ↓
confirm()
   ↓
/eliminar_estudiante/3
   ↓
Estudiante.eliminar()
   ↓
DELETE
   ↓
redirect()
   ↓
/estudiantes
```

---

# 🧠 Conclusión

En esta práctica pasamos de trabajar solamente con:

```text
SELECT
INSERT
```

a trabajar con:

```text
SELECT
INSERT
UPDATE
DELETE
```

Esto completa el ciclo básico de persistencia de datos.

La arquitectura final queda:

```text
               FLASK
                  │
                  ▼
               RUTAS
                  │
                  ▼
             ESTUDIANTE
               MODELO
                  │
        ┌─────────┼─────────┐
        │         │         │
        ▼         ▼         ▼
      SELECT    UPDATE    DELETE
        │         │         │
        └─────────┼─────────┘
                  │
                  ▼
                MySQL
                  │
                  ▼
               Jinja2
                  │
                  ▼
                 HTML
```

La idea fundamental de la lección es:

> **Flask recibe la solicitud, el modelo ejecuta la operación correspondiente sobre MySQL y luego la aplicación redirige al usuario hacia una vista donde puede comprobar el resultado.**

Así, la aplicación ya es capaz de **leer, modificar y eliminar registros de una base de datos utilizando una arquitectura organizada con Flask, POO, PyMySQL, MySQL y Jinja2**.
Mostrando README.md 