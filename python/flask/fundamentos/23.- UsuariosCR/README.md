# 👥 Usuarios CR — Flask + MySQL + POO

> **Práctica:** Create + Read  
> **Tecnologías:** Python · Flask · MySQL · PyMySQL · Jinja2 · HTML5 · Bootstrap

---

## 📖 Descripción

En esta práctica construiremos una aplicación web con Flask para administrar usuarios almacenados en una base de datos MySQL.

La actividad corresponde a las primeras dos operaciones del patrón **CRUD**:

```text
C → Create → Crear
R → Read   → Leer
U → Update → Actualizar
D → Delete → Eliminar
```

En esta etapa trabajaremos únicamente con:

```text
CREATE + READ
```

La aplicación permitirá:

- Visualizar todos los usuarios almacenados en MySQL.
- Acceder a un formulario para crear un nuevo usuario.
- Ingresar nombre, apellido y e-mail.
- Enviar los datos mediante `POST`.
- Crear el registro mediante `INSERT`.
- Redirigir nuevamente al listado.
- Visualizar inmediatamente el usuario creado.

---

# 🎯 Objetivos

Al finalizar esta actividad podrás:

- Conectar Flask con MySQL.
- Utilizar PyMySQL.
- Utilizar Programación Orientada a Objetos para modelar usuarios.
- Recuperar registros mediante `SELECT`.
- Insertar registros mediante `INSERT`.
- Utilizar sentencias SQL preparadas.
- Utilizar diccionarios para enviar parámetros a SQL.
- Utilizar `request.form`.
- Utilizar formularios HTML mediante `POST`.
- Utilizar `redirect()`.
- Utilizar `url_for()`.
- Utilizar Jinja2 para recorrer objetos.
- Mostrar información de una base de datos en una tabla HTML.
- Separar la aplicación en distintas responsabilidades.

---

# 🗄️ Esquema de la base de datos

La tabla proporcionada para esta actividad es:

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

Según el esquema:

| Campo | Tipo |
|---|---|
| `id` | `INT` |
| `nombre` | `VARCHAR(45)` |
| `apellido` | `VARCHAR(45)` |
| `email` | `VARCHAR(45)` |
| `created_at` | `DATETIME` |
| `updated_at` | `DATETIME` |

`id` corresponde a la clave primaria.

> La imagen del esquema no permite confirmar visualmente si `id` tiene activado `AUTO_INCREMENT` ni cuáles son los valores `DEFAULT` de los campos de fecha. Por ello, esta actividad trabaja sobre el esquema `esquema_usuarios` ya creado previamente en MySQL y no asume propiedades que no aparecen confirmadas en el diagrama.

---

# 🧠 Relación entre la interfaz y la base de datos

El wireframe muestra una columna:

```text
Nombre Completo
```

Sin embargo, la base de datos tiene dos campos:

```text
nombre
apellido
```

Por lo tanto, **no crearemos un campo `nombre_completo`**.

En Jinja2 construiremos el nombre completo:

```jinja
{{ usuario.nombre }} {{ usuario.apellido }}
```

Por ejemplo:

```text
Ricky Martin
```

La base de datos continuará manteniendo:

```text
nombre  → Ricky
apellido → Martin
```

---

# 🌐 Rutas de la aplicación

La aplicación utilizará tres rutas:

| Método | Ruta | Función |
|---|---|---|
| `GET` | `/usuarios` | Mostrar todos los usuarios |
| `GET` | `/usuarios/nuevo` | Mostrar formulario |
| `POST` | `/usuarios/crear` | Crear nuevo usuario |

El flujo será:

```text
GET /usuarios
      ↓
Listado

GET /usuarios/nuevo
      ↓
Formulario

POST /usuarios/crear
      ↓
INSERT
      ↓
redirect()
      ↓
GET /usuarios
      ↓
Listado actualizado
```

---

# 📁 Estructura final del proyecto

```text
usuarios_cr/
│
├── server.py
├── usuario.py
├── mysqlconnection.py
├── schema.sql
├── requirements.txt
├── .gitignore
│
├── templates/
│   ├── usuarios.html
│   └── usuario_nuevo.html
│
└── static/
    └── css/
        └── style.css
```

---

# 📦 `requirements.txt`

```text
Flask
PyMySQL
```

---

# 🚫 `.gitignore`

```text
venv/
__pycache__/
*.pyc
.env
```

---

# 🗃️ `schema.sql`

La actividad indica que debemos utilizar el esquema `esquema_usuarios` creado anteriormente en el módulo de MySQL.

Por eso comenzaremos comprobando que exista y que la tabla tenga la estructura esperada.

```sql
-- ==========================================================
-- SELECCIONAR BASE DE DATOS
-- ==========================================================

USE esquema_usuarios;


-- ==========================================================
-- VER ESTRUCTURA DE LA TABLA
-- ==========================================================

DESCRIBE usuarios;


-- ==========================================================
-- VER PROPIEDADES COMPLETAS DE LA TABLA
-- ==========================================================

SHOW CREATE TABLE usuarios;


-- ==========================================================
-- CONSULTAR USUARIOS
-- ==========================================================

SELECT *
FROM usuarios;
```

## ¿Por qué utilizamos `DESCRIBE`?

Permite observar la estructura de la tabla.

Podremos comprobar:

```text
Field
Type
Null
Key
Default
Extra
```

Esto es importante porque permite verificar propiedades que no necesariamente aparecen claramente en el diagrama visual.

---

# 🔌 `mysqlconnection.py`

Este archivo se encargará de centralizar la conexión con MySQL.

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
    Administra la conexión entre Python y MySQL.
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
            no devuelve registros.

        Si ocurre un error:
            devuelve False.
        """

        with self.connection.cursor() as cursor:

            try:

                # --------------------------------------------------
                # Ejecutar consulta.
                #
                # "data" contiene los valores utilizados
                # por los parámetros de la consulta.
                # --------------------------------------------------

                cursor.execute(query, data)


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

                print("Something went wrong:")

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
    Crea y devuelve una instancia de MySQLConnection.
    """

    return MySQLConnection(db)
```

---

# 🔍 ¿Qué hace esta clase?

La clase:

```python
MySQLConnection
```

centraliza:

```text
Conexión
   ↓
Cursor
   ↓
Consulta
   ↓
Resultado
   ↓
Cerrar conexión
```

El resto de nuestra aplicación no necesita repetir:

```python
pymysql.connect(...)
```

cada vez que necesita acceder a la base de datos.

---

# 📚 `DictCursor`

Utilizamos:

```python
cursorclass=pymysql.cursors.DictCursor
```

Esto permite que un `SELECT` entregue resultados como diccionarios.

Por ejemplo:

```python
[
    {
        "id": 1,
        "nombre": "Ricky",
        "apellido": "Martin",
        "email": "ricky@example.com"
    }
]
```

Por lo tanto:

```text
SELECT
  ↓
Lista
  ↓
Diccionarios
```

Luego el modelo transformará esos diccionarios en objetos Python.

---

# 👤 `usuario.py`

Este archivo representa la tabla `usuarios` mediante una clase.

```python
# ==========================================================
# MODELO USUARIO
# ==========================================================

from mysqlconnection import connectToMySQL


# ==========================================================
# CLASE USUARIO
# ==========================================================

class Usuario:
    """
    Representa un registro de la tabla usuarios.
    """

    def __init__(self, data):
        """
        Recibe un diccionario proveniente de MySQL
        y lo transforma en un objeto Usuario.
        """

        self.id = data["id"]

        self.nombre = data["nombre"]

        self.apellido = data["apellido"]

        self.email = data["email"]

        self.created_at = data["created_at"]

        self.updated_at = data["updated_at"]


    # ======================================================
    # READ
    # OBTENER TODOS LOS USUARIOS
    # ======================================================

    @classmethod
    def get_all(cls):
        """
        Recupera todos los usuarios de la base de datos.

        Retorna una lista de objetos Usuario.
        """

        # --------------------------------------------------
        # CONSULTA
        # --------------------------------------------------

        query = """
            SELECT
                id,
                nombre,
                apellido,
                email,
                created_at,
                updated_at
            FROM usuarios
            ORDER BY id;
        """


        # --------------------------------------------------
        # EJECUTAR CONSULTA
        # --------------------------------------------------

        resultados = connectToMySQL(
            "esquema_usuarios"
        ).query_db(query)


        # --------------------------------------------------
        # CREAR LISTA DE OBJETOS
        # --------------------------------------------------

        usuarios = []


        # --------------------------------------------------
        # CONVERTIR CADA DICCIONARIO
        # EN UN OBJETO Usuario
        # --------------------------------------------------

        for usuario in resultados:

            usuarios.append(
                cls(usuario)
            )


        # --------------------------------------------------
        # RETORNAR RESULTADOS
        # --------------------------------------------------

        return usuarios


    # ======================================================
    # CREATE
    # CREAR NUEVO USUARIO
    # ======================================================

    @classmethod
    def save(cls, data):
        """
        Inserta un nuevo usuario en la base de datos.

        Recibe un diccionario con:

        nombre
        apellido
        email
        """

        # --------------------------------------------------
        # INSERT
        # --------------------------------------------------
        #
        # Los datos provenientes del formulario NO se
        # concatenan directamente en el SQL.
        #
        # Utilizamos parámetros preparados.
        #
        # created_at y updated_at se generan mediante NOW().
        # --------------------------------------------------

        query = """
            INSERT INTO usuarios
            (
                nombre,
                apellido,
                email,
                created_at,
                updated_at
            )
            VALUES
            (
                %(nombre)s,
                %(apellido)s,
                %(email)s,
                NOW(),
                NOW()
            );
        """


        # --------------------------------------------------
        # EJECUTAR INSERT
        # --------------------------------------------------

        return connectToMySQL(
            "esquema_usuarios"
        ).query_db(
            query,
            data
        )
```

---

# 🔍 El modelo `Usuario`

## Constructor

El constructor recibe:

```python
data
```

Por ejemplo:

```python
{
    "id": 1,
    "nombre": "Ricky",
    "apellido": "Martin",
    "email": "ricky@example.com",
    "created_at": "...",
    "updated_at": "..."
}
```

y crea un objeto:

```python
Usuario(...)
```

con:

```python
usuario.id
usuario.nombre
usuario.apellido
usuario.email
usuario.created_at
usuario.updated_at
```

---

# 📖 `get_all()`

Este método implementa **READ**.

```python
Usuario.get_all()
```

ejecuta:

```sql
SELECT
    id,
    nombre,
    apellido,
    email,
    created_at,
    updated_at
FROM usuarios
ORDER BY id;
```

MySQL devuelve:

```python
[
    {...},
    {...},
    {...}
]
```

El método transforma cada diccionario en:

```python
Usuario(...)
```

por lo que finalmente obtenemos:

```python
[
    Usuario(...),
    Usuario(...),
    Usuario(...)
]
```

---

# ✍️ `save()`

Este método implementa **CREATE**.

```python
Usuario.save(data)
```

recibe:

```python
data = {
    "nombre": "Juan",
    "apellido": "Pérez",
    "email": "juan@email.com"
}
```

y ejecuta:

```sql
INSERT INTO usuarios
```

---

# 🔐 Sentencia preparada

La consulta utiliza:

```python
%(nombre)s
```

```python
%(apellido)s
```

```python
%(email)s
```

y los valores se envían aparte:

```python
data = {
    "nombre": nombre,
    "apellido": apellido,
    "email": email
}
```

La relación es:

```text
%(nombre)s
     ↓
data["nombre"]

%(apellido)s
     ↓
data["apellido"]

%(email)s
     ↓
data["email"]
```

Esto permite separar:

```text
SQL
```

de:

```text
datos
```

y evita concatenar directamente los valores enviados por el usuario.

---

# 🌐 `server.py`

Este archivo contiene las rutas de Flask.

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


from usuario import Usuario


# ==========================================================
# CREAR APLICACIÓN
# ==========================================================

app = Flask(__name__)


# ==========================================================
# READ
# LISTADO DE USUARIOS
# ==========================================================

@app.route("/usuarios")
def usuarios():
    """
    Recupera todos los usuarios desde MySQL
    y los envía a la plantilla.
    """

    # ------------------------------------------------------
    # CONSULTAR MODELO
    # ------------------------------------------------------

    todos_los_usuarios = Usuario.get_all()


    # ------------------------------------------------------
    # ENVIAR RESULTADO A JINJA2
    # ------------------------------------------------------

    return render_template(
        "usuarios.html",
        usuarios=todos_los_usuarios
    )


# ==========================================================
# MOSTRAR FORMULARIO
# ==========================================================

@app.route("/usuarios/nuevo")
def nuevo_usuario():
    """
    Muestra el formulario de creación.
    """

    return render_template(
        "usuario_nuevo.html"
    )


# ==========================================================
# CREATE
# CREAR USUARIO
# ==========================================================

@app.route("/usuarios/crear", methods=["POST"])
def crear_usuario():
    """
    Recibe la información del formulario
    y crea un nuevo usuario.
    """

    # ------------------------------------------------------
    # RECUPERAR DATOS DEL FORMULARIO
    # ------------------------------------------------------

    nombre = request.form["nombre"].strip()

    apellido = request.form["apellido"].strip()

    email = request.form["email"].strip()


    # ------------------------------------------------------
    # VALIDACIÓN BÁSICA
    # ------------------------------------------------------

    if not nombre or not apellido or not email:

        return render_template(
            "usuario_nuevo.html",
            error="Todos los campos son obligatorios."
        )


    # ------------------------------------------------------
    # CREAR DICCIONARIO
    # ------------------------------------------------------

    data = {

        "nombre": nombre,

        "apellido": apellido,

        "email": email

    }


    # ------------------------------------------------------
    # CREAR USUARIO
    # ------------------------------------------------------

    resultado = Usuario.save(data)


    # ------------------------------------------------------
    # COMPROBAR ERROR
    # ------------------------------------------------------

    if resultado is False:

        return render_template(
            "usuario_nuevo.html",
            error="No fue posible crear el usuario."
        )


    # ------------------------------------------------------
    # REDIRECT
    # ------------------------------------------------------
    #
    # Después de crear el usuario aplicamos:
    #
    # POST → Redirect → GET
    #
    # ------------------------------------------------------

    return redirect(
        url_for("usuarios")
    )


# ==========================================================
# EJECUTAR SERVIDOR
# ==========================================================

if __name__ == "__main__":

    app.run(debug=True)
```

---

# 🔍 Ruta `GET /usuarios`

Esta ruta representa:

```text
READ
```

El flujo:

```text
GET /usuarios
      ↓
Usuario.get_all()
      ↓
SELECT
      ↓
MySQL
      ↓
objetos Usuario
      ↓
render_template()
      ↓
usuarios.html
```

---

# 🔍 Ruta `GET /usuarios/nuevo`

Esta ruta solamente muestra el formulario:

```text
GET /usuarios/nuevo
        ↓
usuario_nuevo.html
```

No modifica información.

---

# 🔍 Ruta `POST /usuarios/crear`

Esta ruta representa:

```text
CREATE
```

El flujo:

```text
POST /usuarios/crear
        ↓
request.form
        ↓
data
        ↓
Usuario.save(data)
        ↓
INSERT
        ↓
redirect()
        ↓
GET /usuarios
```

---

# 🔄 ¿Por qué `redirect()`?

Después de insertar el usuario:

```python
return redirect(
    url_for("usuarios")
)
```

no renderizamos directamente:

```python
usuarios.html
```

La idea es utilizar:

```text
POST → Redirect → GET
```

Así:

```text
POST /usuarios/crear
        ↓
INSERT
        ↓
redirect()
        ↓
GET /usuarios
```

El navegador termina ubicado en:

```text
/usuarios
```

Esto evita que la respuesta final sea una respuesta directa al POST.

---

# 📄 `templates/usuarios.html`

Esta plantilla corresponde al listado principal.

```html
<!DOCTYPE html>
<html lang="es">

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>Usuarios</title>


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

    <div class="d-flex justify-content-between align-items-center mb-4">

        <div>

            <h1 class="mb-1">
                Usuarios
            </h1>

            <p class="text-muted mb-0">
                Usuarios registrados en el sistema.
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
                                    Id
                                </th>

                                <th>
                                    Nombre Completo
                                </th>

                                <th>
                                    E-mail
                                </th>

                                <th>
                                    Fecha Creación
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

                                </tr>

                            {% endfor %}

                        </tbody>

                    </table>

                </div>

            {% else %}

                <div class="empty-state">

                    <h3>
                        No hay usuarios registrados
                    </h3>

                    <p class="text-muted">

                        Crea el primer usuario para comenzar.

                    </p>


                    <a
                        href="{{ url_for('nuevo_usuario') }}"
                        class="btn btn-primary"
                    >

                        Crear usuario

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

# 🔍 Jinja2 en `usuarios.html`

Flask envía:

```python
usuarios=todos_los_usuarios
```

La plantilla recibe:

```text
usuarios
```

y recorre:

```jinja
{% for usuario in usuarios %}
```

Cada elemento es un objeto:

```python
Usuario
```

por lo tanto podemos utilizar:

```jinja
{{ usuario.id }}
```

```jinja
{{ usuario.nombre }}
```

```jinja
{{ usuario.apellido }}
```

```jinja
{{ usuario.email }}
```

```jinja
{{ usuario.created_at }}
```

---

# 👤 Nombre completo

Aunque la columna se llama:

```text
Nombre Completo
```

no existe ese campo en la base de datos.

Se construye en la plantilla:

```jinja
{{ usuario.nombre }} {{ usuario.apellido }}
```

Por ejemplo:

```text
Ricky Martin
```

---

# 📝 `templates/usuario_nuevo.html`

Esta plantilla contiene el formulario de creación.

```html
<!DOCTYPE html>
<html lang="es">

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>Crear nuevo usuario</title>


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


    <div class="row justify-content-center">

        <div class="col-lg-6">


            <!-- ==================================================
                 ENCABEZADO
            =================================================== -->

            <div class="d-flex justify-content-between align-items-center mb-4">

                <h1 class="mb-0">
                    Crear nuevo usuario
                </h1>


                <a
                    href="{{ url_for('usuarios') }}"
                    class="btn btn-outline-secondary"
                >

                    Volver

                </a>

            </div>


            <!-- ==================================================
                 FORMULARIO
            =================================================== -->

            <div class="card shadow-sm border-0">

                <div class="card-body p-4">


                    <!-- ==================================================
                         MENSAJE DE ERROR
                    =================================================== -->

                    {% if error %}

                        <div class="alert alert-danger">

                            {{ error }}

                        </div>

                    {% endif %}


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
                                maxlength="45"
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
                                maxlength="45"
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
                                maxlength="45"
                                required
                            >

                        </div>


                        <!-- BOTÓN -->

                        <div class="d-grid">

                            <button
                                type="submit"
                                class="btn btn-primary"
                            >

                                Crear

                            </button>

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

# 🔍 Relación HTML → Flask

El input:

```html
name="nombre"
```

se recupera mediante:

```python
request.form["nombre"]
```

El input:

```html
name="apellido"
```

se recupera mediante:

```python
request.form["apellido"]
```

El input:

```html
name="email"
```

se recupera mediante:

```python
request.form["email"]
```

Por lo tanto:

```text
HTML
 │
 ├── name="nombre"
 ├── name="apellido"
 └── name="email"
          │
          ▼
     request.form
          │
          ▼
       Python
          │
          ▼
        data
          │
          ▼
      Usuario.save()
```

---

# 🔗 `url_for()`

Para acceder al formulario:

```jinja
{{ url_for('nuevo_usuario') }}
```

genera:

```text
/usuarios/nuevo
```

Para crear:

```jinja
{{ url_for('crear_usuario') }}
```

genera:

```text
/usuarios/crear
```

Para volver al listado:

```jinja
{{ url_for('usuarios') }}
```

genera:

```text
/usuarios
```

`url_for()` utiliza el **nombre de la función Python**, no la ruta escrita.

Por ejemplo:

```python
@app.route("/usuarios/nuevo")
def nuevo_usuario():
```

se referencia mediante:

```jinja
url_for("nuevo_usuario")
```

---

# 🎨 `static/css/style.css`

```css
/* ==========================================================
   USUARIOS CR
========================================================== */

body {
    background-color: #f5f6f8;
    font-family: Arial, Helvetica, sans-serif;
}


h1 {
    font-weight: 700;
}


.card {
    border-radius: 10px;
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


@media (max-width: 576px) {

    .d-flex.justify-content-between {
        align-items: flex-start !important;
        flex-direction: column;
        gap: 15px;
    }

}
```

---

# 🧪 Prueba completa

## Listado inicial

Ejecuta:

```bash
python server.py
```

y visita:

```text
http://127.0.0.1:5000/usuarios
```

Deberías ver una tabla similar a:

```text
┌────┬──────────────────┬────────────────────────┬────────────────┐
│ Id │ Nombre Completo  │ E-mail                 │ Fecha Creación │
├────┼──────────────────┼────────────────────────┼────────────────┤
│ 1  │ Ricky Martin     │ ricky@codingdojo.com   │ 2024-04-30     │
│ 2  │ Enrique Iglesias │ enrique@codingdojo.com │ 2024-04-30     │
│ 3  │ Celia Cruz       │ celia@codingdojo.com   │ 2024-04-30     │
│ 4  │ Ricardo Montaner │ ricardo@codingdojo.com │ 2024-04-30     │
└────┴──────────────────┴────────────────────────┴────────────────┘

                         Nuevo Usuario
```

---

# ➕ Crear nuevo usuario

Accede a:

```text
http://127.0.0.1:5000/usuarios/nuevo
```

Completa:

```text
Nombre:
Juan

Apellido:
Pérez

E-mail:
juan@email.com
```

Presiona:

```text
Crear
```

---

# 📤 Flujo POST

Flask recibirá:

```python
request.form["nombre"]
request.form["apellido"]
request.form["email"]
```

Se construirá:

```python
data = {
    "nombre": nombre,
    "apellido": apellido,
    "email": email
}
```

Luego:

```python
Usuario.save(data)
```

ejecutará el `INSERT`.

---

# 🔄 Redirección

Una vez creado el usuario:

```python
return redirect(
    url_for("usuarios")
)
```

El navegador volverá a:

```text
GET /usuarios
```

La aplicación realizará nuevamente:

```python
Usuario.get_all()
```

y ejecutará:

```sql
SELECT
    id,
    nombre,
    apellido,
    email,
    created_at,
    updated_at
FROM usuarios
ORDER BY id;
```

Por lo tanto el nuevo registro aparecerá en la tabla automáticamente.

---

# 🧠 Flujo completo CREATE

```text
usuario_nuevo.html
        │
        │
        │ POST
        ▼
/usuarios/crear
        │
        ▼
request.form
        │
        ▼
data
        │
        ▼
Usuario.save(data)
        │
        ▼
INSERT
        │
        ▼
MySQL
        │
        ▼
redirect()
        │
        ▼
GET /usuarios
        │
        ▼
Usuario.get_all()
        │
        ▼
SELECT
        │
        ▼
usuarios.html
        │
        ▼
nuevo usuario visible
```

---

# 🧠 Flujo completo READ

```text
GET /usuarios
      │
      ▼
Usuario.get_all()
      │
      ▼
SELECT
      │
      ▼
MySQL
      │
      ▼
Lista de diccionarios
      │
      ▼
Lista de objetos Usuario
      │
      ▼
render_template()
      │
      ▼
Jinja2
      │
      ▼
Tabla HTML
```

---

# 🔐 ¿Por qué utilizar sentencias preparadas?

No debemos crear consultas de esta manera:

```python
query = (
    "INSERT INTO usuarios "
    "VALUES ('"
    + nombre
    + "', '"
    + apellido
    + "', '"
    + email
    + "')"
)
```

Tampoco:

```python
query = f"""
    INSERT INTO usuarios
    (nombre, apellido, email)
    VALUES
    ('{nombre}', '{apellido}', '{email}')
"""
```

La forma utilizada en esta actividad es:

```python
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
```

y:

```python
data = {
    "nombre": nombre,
    "apellido": apellido,
    "email": email
}
```

Esto separa:

```text
consulta SQL
```

de:

```text
datos variables
```

---

# ⚠️ Errores comunes

## `ModuleNotFoundError: No module named 'pymysql'`

Instala:

```bash
pip install PyMySQL
```

o:

```bash
pip install -r requirements.txt
```

---

## La base de datos no existe

Comprueba:

```sql
SHOW DATABASES;
```

Debe existir:

```text
esquema_usuarios
```

---

## La tabla no existe

Comprueba:

```sql
USE esquema_usuarios;

SHOW TABLES;
```

Debe existir:

```text
usuarios
```

---

## Error de conexión

Revisa:

```python
host="localhost"
user="root"
password="root"
```

y reemplaza la contraseña con la que corresponda a tu instalación.

---

## `BadRequestKeyError`

Por ejemplo, Python espera:

```python
request.form["nombre"]
```

pero el HTML utiliza:

```html
name="nombre_usuario"
```

Los nombres deben coincidir exactamente.

Correcto:

```html
name="nombre"
```

y:

```python
request.form["nombre"]
```

---

## `BuildError`

Si la función es:

```python
def nuevo_usuario():
```

debes utilizar:

```jinja
url_for("nuevo_usuario")
```

No:

```jinja
url_for("usuarios_nuevo")
```

`url_for()` trabaja con el **nombre de la función**.

---

# ✅ Checklist final

```text
[ ] Base de datos esquema_usuarios disponible
[ ] Tabla usuarios disponible
[ ] Estructura de usuarios verificada
[ ] PyMySQL instalado
[ ] mysqlconnection.py funcionando
[ ] Clase Usuario creada
[ ] Usuario.get_all() funcionando
[ ] Usuario.save() funcionando
[ ] GET /usuarios funcionando
[ ] GET /usuarios/nuevo funcionando
[ ] POST /usuarios/crear funcionando
[ ] request.form funcionando
[ ] INSERT funcionando
[ ] Sentencia preparada funcionando
[ ] redirect() funcionando
[ ] url_for() funcionando
[ ] Nuevo usuario aparece en la tabla
[ ] Jinja2 muestra correctamente los datos
```

---

# 📚 Conceptos aplicados

| Concepto | Aplicación |
|---|---|
| Flask | Servidor web |
| `@app.route()` | Definición de rutas |
| `GET` | Consultar y mostrar información |
| `POST` | Enviar datos para crear un registro |
| `request.form` | Leer datos del formulario |
| `redirect()` | Redirigir después del CREATE |
| `url_for()` | Generar URLs dinámicamente |
| PyMySQL | Conexión con MySQL |
| POO | Modelo `Usuario` |
| `@classmethod` | Métodos del modelo |
| `SELECT` | Leer usuarios |
| `INSERT` | Crear usuarios |
| Jinja2 | Renderizar datos |
| `{% for %}` | Recorrer usuarios |
| `{% if %}` | Manejar colecciones vacías |
| Sentencias preparadas | Enviar valores variables de forma segura |

---

# 🧩 CREATE + READ

Esta práctica deja implementadas dos operaciones del CRUD:

```text
┌─────────────────────────────┐
│            CRUD             │
├─────────────────────────────┤
│ C → CREATE ✅               │
│ R → READ   ✅               │
│ U → UPDATE ⏳               │
│ D → DELETE ⏳               │
└─────────────────────────────┘
```

---

# 🏁 Resultado esperado

La aplicación final deberá permitir:

```text
                    USUARIOS
                       │
             ┌─────────┴─────────┐
             │                   │
             ▼                   ▼
        Ver usuarios       Nuevo Usuario
             │                   │
             │                   ▼
             │              Formulario
             │                   │
             │                   │ POST
             │                   ▼
             │           /usuarios/crear
             │                   │
             │                   ▼
             │                INSERT
             │                   │
             │                   ▼
             │               redirect()
             │                   │
             └───────────────┐   │
                             ▼   ▼
                         /usuarios
                             │
                             ▼
                      SELECT actualizado
                             │
                             ▼
                       Tabla de usuarios
```

El objetivo se considera cumplido cuando el usuario puede **visualizar los registros existentes y crear un nuevo usuario desde el formulario, de modo que el nuevo registro aparezca inmediatamente en el listado**.
Mostrando README.md