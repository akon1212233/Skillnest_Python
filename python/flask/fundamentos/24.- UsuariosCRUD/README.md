# 👥 Usuarios CRUD — Flask + MySQL + POO

> **Práctica:** CRUD completo  
> **Operaciones:** Create · Read · Update · Delete  
> **Tecnologías:** Python · Flask · MySQL · PyMySQL · Jinja2 · HTML5 · CSS · Bootstrap

---

# 📖 Descripción

En las prácticas anteriores construimos una aplicación que permitía:

- Crear usuarios.
- Leer y mostrar usuarios.

Ahora ampliaremos ese mismo proyecto para completar el **CRUD**.

CRUD corresponde a:

```text
C → Create → Crear
R → Read   → Leer
U → Update → Actualizar
D → Delete → Eliminar
```

La aplicación final permitirá:

```text
┌─────────────────────────────────────────────┐
│ Usuarios                    Nuevo Usuario   │
├─────────────────────────────────────────────┤
│ ID │ Nombre │ E-mail │ Fecha │ Acciones     │
├────┼────────┼────────┼───────┼──────────────┤
│ 1  │ ...    │ ...    │ ...   │ Ver Editar   │
│ 2  │ ...    │ ...    │ ...   │ Borrar       │
└─────────────────────────────────────────────┘
```

Cada usuario tendrá las acciones:

```text
Ver
Editar
Borrar
```

---

# 🎯 Objetivos

Al finalizar esta práctica podrás:

- Completar un CRUD utilizando Flask.
- Buscar un usuario por ID.
- Utilizar rutas dinámicas con `<int:id>`.
- Mostrar el detalle de un usuario.
- Cargar un registro existente en un formulario.
- Actualizar información mediante `UPDATE`.
- Eliminar información mediante `DELETE`.
- Utilizar sentencias preparadas.
- Utilizar `request.form`.
- Utilizar `redirect()`.
- Utilizar `url_for()`.
- Trabajar con varias plantillas Jinja2.
- Mantener separadas las responsabilidades entre rutas, modelos y presentación.

---

# 🗄️ Esquema de la base de datos

La tabla utilizada en esta actividad es:

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

Según el esquema proporcionado:

| Campo | Tipo |
|---|---|
| `id` | `INT` |
| `nombre` | `VARCHAR(45)` |
| `apellido` | `VARCHAR(45)` |
| `email` | `VARCHAR(45)` |
| `created_at` | `DATETIME` |
| `updated_at` | `DATETIME` |

`id` es la clave primaria.

La interfaz mostrará:

```text
Nombre Completo
```

pero esto **no es un campo de la base de datos**.

Se construirá utilizando:

```jinja
{{ usuario.nombre }} {{ usuario.apellido }}
```

---

# 🧠 Arquitectura de la aplicación

El proyecto seguirá esta separación:

```text
server.py
   │
   │ rutas
   ▼
usuario.py
   │
   │ modelo
   ▼
mysqlconnection.py
   │
   │ conexión
   ▼
MySQL
   │
   ▼
usuarios
```

La presentación se encuentra en:

```text
templates/
```

---

# 📁 Estructura final del proyecto

```text
usuarios_crud/
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
│   ├── usuario_nuevo.html
│   ├── usuario.html
│   └── usuario_editar.html
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

Esta práctica utiliza la base de datos:

```text
esquema_usuarios
```

y la tabla:

```text
usuarios
```

Puedes verificar su estructura mediante:

```sql
USE esquema_usuarios;

DESCRIBE usuarios;
```

También puedes revisar la definición completa:

```sql
SHOW CREATE TABLE usuarios;
```

Y consultar los registros:

```sql
SELECT *
FROM usuarios;
```

No necesitamos crear nuevas columnas para implementar el CRUD.

---

# 🔌 `mysqlconnection.py`

Este archivo mantiene la responsabilidad de conectarse a MySQL y ejecutar las consultas.

## Código completo

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
        y establece una conexión.
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

        Si ocurre un error:
            devuelve False.
        """

        with self.connection.cursor() as cursor:

            try:

                # --------------------------------------------------
                # Ejecutar consulta
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
                # Cerrar conexión
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

# 🧠 ¿Qué cambia en esta etapa?

En las prácticas anteriores utilizábamos principalmente:

```text
SELECT
INSERT
```

Ahora tendremos además:

```text
UPDATE
DELETE
```

Por lo tanto:

```text
CRUD
│
├── SELECT → READ
├── INSERT → CREATE
├── UPDATE → UPDATE
└── DELETE → DELETE
```

---

# 👤 `usuario.py`

Este archivo representa la tabla `usuarios` y contiene las operaciones del CRUD.

## Código completo

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
        Recupera todos los usuarios.
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
            ORDER BY id;
        """


        resultados = connectToMySQL(
            "esquema_usuarios"
        ).query_db(query)


        usuarios = []


        for usuario in resultados:

            usuarios.append(
                cls(usuario)
            )


        return usuarios


    # ======================================================
    # READ
    # OBTENER USUARIO POR ID
    # ======================================================

    @classmethod
    def get_by_id(cls, id):
        """
        Busca un usuario específico mediante su ID.

        Si existe:
            devuelve un objeto Usuario.

        Si no existe:
            devuelve None.
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


        resultados = connectToMySQL(
            "esquema_usuarios"
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
    # CREATE
    # CREAR USUARIO
    # ======================================================

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


        return connectToMySQL(
            "esquema_usuarios"
        ).query_db(
            query,
            data
        )


    # ======================================================
    # UPDATE
    # ACTUALIZAR USUARIO
    # ======================================================

    @classmethod
    def update(cls, data):
        """
        Actualiza los datos de un usuario existente.

        data debe contener:

        id
        nombre
        apellido
        email
        """

        query = """
            UPDATE usuarios
            SET
                nombre = %(nombre)s,
                apellido = %(apellido)s,
                email = %(email)s,
                updated_at = NOW()
            WHERE id = %(id)s;
        """


        return connectToMySQL(
            "esquema_usuarios"
        ).query_db(
            query,
            data
        )


    # ======================================================
    # DELETE
    # ELIMINAR USUARIO
    # ======================================================

    @classmethod
    def delete(cls, id):
        """
        Elimina un usuario utilizando su ID.
        """

        query = """
            DELETE FROM usuarios
            WHERE id = %(id)s;
        """


        data = {
            "id": id
        }


        return connectToMySQL(
            "esquema_usuarios"
        ).query_db(
            query,
            data
        )
```

---

# 🧠 Análisis del modelo

Ahora nuestra clase contiene:

```text
Usuario
│
├── get_all()
├── get_by_id()
├── save()
├── update()
└── delete()
```

Esto representa:

```text
CREATE → save()
READ   → get_all()
READ   → get_by_id()
UPDATE → update()
DELETE → delete()
```

---

# 🔍 `get_by_id()`

Este método es nuevo.

```python
Usuario.get_by_id(3)
```

utiliza:

```sql
SELECT
    id,
    nombre,
    apellido,
    email,
    created_at,
    updated_at
FROM usuarios
WHERE id = %(id)s;
```

El valor:

```python
3
```

viaja mediante:

```python
data = {
    "id": 3
}
```

---

# 🧠 Flujo de `get_by_id()`

```text
/usuarios/3
    ↓
id = 3
    ↓
Usuario.get_by_id(3)
    ↓
SELECT ... WHERE id = 3
    ↓
MySQL
    ↓
diccionario
    ↓
Usuario(...)
    ↓
objeto Usuario
```

---

# ✏️ `update()`

Este método utiliza:

```sql
UPDATE usuarios
SET
    nombre = %(nombre)s,
    apellido = %(apellido)s,
    email = %(email)s,
    updated_at = NOW()
WHERE id = %(id)s;
```

El diccionario será:

```python
data = {
    "id": 3,
    "nombre": "Celia",
    "apellido": "Cruz",
    "email": "celia@email.com"
}
```

---

# ⚠️ Importancia de `WHERE`

Observa:

```sql
WHERE id = %(id)s
```

Esto es fundamental.

Sin `WHERE`:

```sql
UPDATE usuarios
SET nombre = "Celia";
```

se podrían modificar **todos los usuarios**.

Con:

```sql
WHERE id = 3
```

solamente se modifica:

```text
usuario 3
```

La misma regla es fundamental para `DELETE`.

---

# 🗑️ `delete()`

El método utiliza:

```sql
DELETE FROM usuarios
WHERE id = %(id)s;
```

Por ejemplo:

```python
Usuario.delete(3)
```

eliminará únicamente:

```text
usuario id = 3
```

---

# 🌐 `server.py`

Ahora agregaremos todas las rutas del CRUD.

## Código completo

```python
# ==========================================================
# SERVIDOR FLASK — CRUD USUARIOS
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
    Muestra todos los usuarios.
    """

    todos_los_usuarios = Usuario.get_all()


    return render_template(
        "usuarios.html",
        usuarios=todos_los_usuarios
    )


# ==========================================================
# CREATE
# MOSTRAR FORMULARIO
# ==========================================================

@app.route("/usuarios/nuevo")
def nuevo_usuario():
    """
    Muestra el formulario para crear un usuario.
    """

    return render_template(
        "usuario_nuevo.html"
    )


# ==========================================================
# CREATE
# PROCESAR FORMULARIO
# ==========================================================

@app.route(
    "/usuarios/crear",
    methods=["POST"]
)
def crear_usuario():
    """
    Recibe y guarda los datos del formulario.
    """

    nombre = request.form["nombre"].strip()

    apellido = request.form["apellido"].strip()

    email = request.form["email"].strip()


    if not nombre or not apellido or not email:

        return render_template(
            "usuario_nuevo.html",
            error="Todos los campos son obligatorios."
        )


    data = {
        "nombre": nombre,
        "apellido": apellido,
        "email": email
    }


    resultado = Usuario.save(data)


    if resultado is False:

        return render_template(
            "usuario_nuevo.html",
            error="No fue posible crear el usuario."
        )


    return redirect(
        url_for("usuarios")
    )


# ==========================================================
# READ
# VER USUARIO
# ==========================================================

@app.route("/usuarios/<int:id>")
def ver_usuario(id):
    """
    Muestra la información completa de un usuario.
    """

    usuario = Usuario.get_by_id(id)


    if usuario is None:

        return "Usuario no encontrado", 404


    return render_template(
        "usuario.html",
        usuario=usuario
    )


# ==========================================================
# UPDATE
# MOSTRAR FORMULARIO DE EDICIÓN
# ==========================================================

@app.route("/usuarios/editar/<int:id>")
def editar_usuario(id):
    """
    Recupera un usuario y carga sus datos
    dentro del formulario de edición.
    """

    usuario = Usuario.get_by_id(id)


    if usuario is None:

        return "Usuario no encontrado", 404


    return render_template(
        "usuario_editar.html",
        usuario=usuario
    )


# ==========================================================
# UPDATE
# PROCESAR EDICIÓN
# ==========================================================

@app.route(
    "/usuarios/<int:id>/actualizar",
    methods=["POST"]
)
def actualizar_usuario(id):
    """
    Recibe los nuevos datos y actualiza
    el usuario correspondiente.
    """

    nombre = request.form["nombre"].strip()

    apellido = request.form["apellido"].strip()

    email = request.form["email"].strip()


    if not nombre or not apellido or not email:

        usuario = Usuario.get_by_id(id)


        return render_template(
            "usuario_editar.html",
            usuario=usuario,
            error="Todos los campos son obligatorios."
        )


    data = {
        "id": id,
        "nombre": nombre,
        "apellido": apellido,
        "email": email
    }


    resultado = Usuario.update(data)


    if resultado is False:

        usuario = Usuario.get_by_id(id)


        return render_template(
            "usuario_editar.html",
            usuario=usuario,
            error="No fue posible actualizar el usuario."
        )


    return redirect(
        url_for("usuarios")
    )


# ==========================================================
# DELETE
# BORRAR USUARIO
# ==========================================================
#
# Para seguir la estructura original de la actividad,
# utilizaremos una ruta GET para el enlace "Borrar".
#
# En aplicaciones reales es preferible utilizar POST
# o DELETE para operaciones destructivas.
# ==========================================================

@app.route("/usuarios/borrar/<int:id>")
def borrar_usuario(id):
    """
    Elimina el usuario correspondiente al ID.
    """

    resultado = Usuario.delete(id)


    if resultado is False:

        return "No fue posible eliminar el usuario.", 500


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

# 🧠 Rutas del CRUD

Nuestra aplicación ahora tiene:

| Método | Ruta | Operación |
|---|---|---|
| `GET` | `/usuarios` | READ — listado |
| `GET` | `/usuarios/nuevo` | Formulario CREATE |
| `POST` | `/usuarios/crear` | CREATE |
| `GET` | `/usuarios/<id>` | READ — detalle |
| `GET` | `/usuarios/editar/<id>` | Formulario UPDATE |
| `POST` | `/usuarios/<id>/actualizar` | UPDATE |
| `GET` | `/usuarios/borrar/<id>` | DELETE |

---

# 🔢 Rutas dinámicas

La ruta:

```python
@app.route("/usuarios/<int:id>")
```

permite:

```text
/usuarios/1
/usuarios/2
/usuarios/3
/usuarios/4
```

Flask convierte automáticamente:

```text
"3"
```

en:

```python
3
```

por utilizar:

```text
<int:id>
```

---

# 🔍 `url_for()` con parámetros

Para crear el enlace de detalle:

```jinja
{{ url_for("ver_usuario", id=usuario.id) }}
```

Si:

```python
usuario.id = 3
```

Flask genera:

```text
/usuarios/3
```

Para editar:

```jinja
{{ url_for("editar_usuario", id=usuario.id) }}
```

genera:

```text
/usuarios/editar/3
```

Para borrar:

```jinja
{{ url_for("borrar_usuario", id=usuario.id) }}
```

genera:

```text
/usuarios/borrar/3
```

---

# 📄 `templates/usuarios.html`

Esta es la vista principal.

```html
<!DOCTYPE html>
<html lang="es">

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>Todos los Usuarios</title>


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
                Usuarios
            </h1>

            <p class="text-muted">
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

                                <th>
                                    Acciones
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

                                        <strong>

                                            {{ usuario.nombre }}
                                            {{ usuario.apellido }}

                                        </strong>

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
                                                href="{{ url_for('ver_usuario', id=usuario.id) }}"
                                                class="btn btn-sm btn-outline-primary"
                                            >
                                                Ver
                                            </a>


                                            <a
                                                href="{{ url_for('editar_usuario', id=usuario.id) }}"
                                                class="btn btn-sm btn-outline-warning"
                                            >
                                                Editar
                                            </a>


                                            <a
                                                href="{{ url_for('borrar_usuario', id=usuario.id) }}"
                                                class="btn btn-sm btn-outline-danger"
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
                        href="{{ url_for('nuevo_usuario') }}"
                        class="btn btn-primary"
                    >
                        Nuevo Usuario
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

# 🔍 Análisis de las acciones

Cada usuario tendrá:

```text
Ver
Editar
Borrar
```

Los enlaces se generan mediante `url_for()`.

### Ver

```jinja
{{ url_for("ver_usuario", id=usuario.id) }}
```

### Editar

```jinja
{{ url_for("editar_usuario", id=usuario.id) }}
```

### Borrar

```jinja
{{ url_for("borrar_usuario", id=usuario.id) }}
```

---

# 👁️ `templates/usuario.html`

Esta página muestra toda la información de un usuario.

```html
<!DOCTYPE html>
<html lang="es">

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>Ver Usuario</title>


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

        <div class="page-header">

            <div>

                <h1>
                    Usuario {{ usuario.id }}
                </h1>

                <p class="text-muted">
                    Información completa del usuario.
                </p>

            </div>

        </div>


        <!-- ==================================================
             INFORMACIÓN
        =================================================== -->

        <div class="user-detail">

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


        <!-- ==================================================
             ACCIONES
        =================================================== -->

        <div class="mt-4">

            <a
                href="{{ url_for('editar_usuario', id=usuario.id) }}"
                class="btn btn-warning"
            >
                Editar
            </a>


            <a
                href="{{ url_for('borrar_usuario', id=usuario.id) }}"
                class="btn btn-danger"
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

# 🔍 Flujo de la vista de detalle

Si hacemos clic en:

```text
Ver
```

sobre el usuario:

```text
id = 3
```

la URL será:

```text
/usuarios/3
```

Flask ejecuta:

```python
ver_usuario(3)
```

y posteriormente:

```python
Usuario.get_by_id(3)
```

---

# ✏️ `templates/usuario_editar.html`

Esta página mostrará los datos actuales y permitirá modificarlos.

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

    <div class="row justify-content-center">

        <div class="col-lg-6">

            <!-- ==================================================
                 ENCABEZADO
            =================================================== -->

            <div class="page-header">

                <div>

                    <h1>
                        Editar usuario {{ usuario.id }}
                    </h1>

                    <p class="text-muted">
                        Modifica la información del usuario.
                    </p>

                </div>

            </div>


            <!-- ==================================================
                 FORMULARIO
            =================================================== -->

            <div class="card shadow-sm border-0">

                <div class="card-body p-4">


                    {% if error %}

                        <div class="alert alert-danger">

                            {{ error }}

                        </div>

                    {% endif %}


                    <form
                        action="{{ url_for('actualizar_usuario', id=usuario.id) }}"
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
                                value="{{ usuario.nombre }}"
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
                                value="{{ usuario.apellido }}"
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
                                value="{{ usuario.email }}"
                                maxlength="45"
                                required
                            >

                        </div>


                        <!-- ==================================================
                             BOTONES
                        =================================================== -->

                        <div class="d-flex gap-2">

                            <button
                                type="submit"
                                class="btn btn-success"
                            >
                                Actualizar
                            </button>


                            <a
                                href="{{ url_for('ver_usuario', id=usuario.id) }}"
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

# 🔍 ¿Cómo se cargan los valores existentes?

Supongamos que:

```python
usuario.nombre = "Celia"
```

Entonces:

```html
value="{{ usuario.nombre }}"
```

genera en el navegador:

```html
value="Celia"
```

Por eso el formulario aparece precargado.

El flujo es:

```text
GET /usuarios/editar/3
        ↓
Usuario.get_by_id(3)
        ↓
usuario
        ↓
usuario_editar.html
        ↓
value="Celia"
value="Cruz"
value="celia@email.com"
```

---

# ➕ `templates/usuario_nuevo.html`

Esta es la vista utilizada para crear usuarios.

```html
<!DOCTYPE html>
<html lang="es">

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

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

    <div class="row justify-content-center">

        <div class="col-lg-6">

            <div class="page-header">

                <div>

                    <h1>
                        Crear nuevo usuario
                    </h1>

                    <p class="text-muted">
                        Ingresa la información del usuario.
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


                        <!-- BOTONES -->

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

# 🎨 `static/css/style.css`

```css
/* ==========================================================
   USUARIOS CRUD
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

    .container {
        padding-left: 15px;
        padding-right: 15px;
    }


    .detail-card {
        padding: 20px;
    }

}
```

---

# 🧠 UPDATE paso a paso

La operación UPDATE tiene dos momentos.

Primero necesitamos **mostrar el formulario con los datos existentes**.

```text
GET /usuarios/editar/3
```

Después necesitamos **procesar la modificación**.

```text
POST /usuarios/3/actualizar
```

Por eso tenemos dos rutas.

---

## 1. GET — Mostrar formulario

```python
@app.route("/usuarios/editar/<int:id>")
def editar_usuario(id):
```

El ID viene desde la URL.

Por ejemplo:

```text
/usuarios/editar/3
```

entrega:

```python
id = 3
```

Luego:

```python
usuario = Usuario.get_by_id(id)
```

consulta la base de datos.

Finalmente:

```python
return render_template(
    "usuario_editar.html",
    usuario=usuario
)
```

envía el usuario a Jinja2.

---

## 2. Formulario precargado

El formulario utiliza:

```jinja
value="{{ usuario.nombre }}"
```

```jinja
value="{{ usuario.apellido }}"
```

```jinja
value="{{ usuario.email }}"
```

Así el usuario no tiene que escribir nuevamente toda la información.

---

## 3. POST — Actualizar

Al presionar:

```text
Actualizar
```

se envían los nuevos datos:

```text
POST /usuarios/3/actualizar
```

Flask obtiene:

```python
request.form
```

y construye:

```python
data = {
    "id": 3,
    "nombre": "Celia",
    "apellido": "Cruz",
    "email": "celia@nuevo.com"
}
```

Luego:

```python
Usuario.update(data)
```

---

# 📝 ¿Por qué enviamos el `id`?

Porque necesitamos decirle a MySQL:

> "¿Qué usuario debo actualizar?"

La consulta:

```sql
UPDATE usuarios
SET
    nombre = %(nombre)s,
    apellido = %(apellido)s,
    email = %(email)s
WHERE id = %(id)s;
```

utiliza:

```python
"id": 3
```

para identificar el registro.

---

# 🔄 Flujo completo del UPDATE

```text
Lista
  ↓
Editar
  ↓
GET /usuarios/editar/3
  ↓
Usuario.get_by_id(3)
  ↓
Formulario precargado
  ↓
Usuario modifica datos
  ↓
POST /usuarios/3/actualizar
  ↓
request.form
  ↓
data
  ↓
Usuario.update(data)
  ↓
UPDATE MySQL
  ↓
redirect()
  ↓
GET /usuarios
  ↓
usuario actualizado visible
```

---

# 🗑️ DELETE paso a paso

El enlace:

```text
Borrar
```

apunta a:

```text
/usuarios/borrar/3
```

Flask recibe:

```python
id = 3
```

y ejecuta:

```python
Usuario.delete(3)
```

El modelo ejecuta:

```sql
DELETE FROM usuarios
WHERE id = %(id)s;
```

Después:

```python
redirect(url_for("usuarios"))
```

---

# 🔄 Flujo completo del DELETE

```text
Lista
  ↓
Borrar
  ↓
/usuarios/borrar/3
  ↓
Usuario.delete(3)
  ↓
DELETE
  ↓
MySQL
  ↓
redirect()
  ↓
GET /usuarios
  ↓
usuario desaparece
```

---

# ⚠️ ¿Por qué `WHERE` es tan importante?

Nunca debemos ejecutar:

```sql
DELETE FROM usuarios;
```

porque eliminaría todos los registros.

Debemos utilizar:

```sql
DELETE FROM usuarios
WHERE id = %(id)s;
```

Así solamente eliminaremos el usuario correspondiente.

Lo mismo sucede con:

```sql
UPDATE
```

Nunca debemos hacer:

```sql
UPDATE usuarios
SET nombre = "Celia";
```

porque modificaríamos todos los usuarios.

Debemos utilizar:

```sql
WHERE id = %(id)s;
```

---

# ⚠️ Nota sobre Borrar mediante GET

En esta práctica utilizamos:

```text
GET /usuarios/borrar/<id>
```

porque es la estructura sencilla planteada por el ejercicio.

Sin embargo, en una aplicación real una operación destructiva no debería depender de un enlace GET.

Una alternativa más apropiada sería:

```text
POST /usuarios/<id>/eliminar
```

o utilizar:

```text
HTTP DELETE
```

Esto evita que una acción destructiva se ejecute simplemente al visitar una URL.

Para esta actividad mantenemos `GET` porque el objetivo es aprender el funcionamiento del CRUD y las rutas dinámicas.

---

# 👁️ READ — Ver detalle

El READ ahora tiene dos posibilidades:

### Todos los usuarios

```text
GET /usuarios
```

utiliza:

```python
Usuario.get_all()
```

### Un usuario

```text
GET /usuarios/3
```

utiliza:

```python
Usuario.get_by_id(3)
```

Esto demuestra que una operación READ no necesariamente significa solamente "mostrar todos".

También podemos obtener un registro específico.

---

# 🔗 Relación entre URL y `id`

Tenemos:

```python
@app.route("/usuarios/<int:id>")
```

y:

```jinja
{{ url_for("ver_usuario", id=usuario.id) }}
```

La relación es:

```text
usuario.id = 3
        ↓
url_for()
        ↓
/usuarios/3
        ↓
Flask
        ↓
id = 3
```

---

# 🧪 Prueba completa del CRUD

## 1. READ

Abrir:

```text
http://127.0.0.1:5000/usuarios
```

Deberá aparecer el listado.

---

## 2. CREATE

Presionar:

```text
Nuevo Usuario
```

Crear un registro.

Por ejemplo:

```text
Nombre: Pedro
Apellido: González
E-mail: pedro@email.com
```

Después de presionar:

```text
Crear
```

deberá aparecer en el listado.

---

## 3. READ individual

Presionar:

```text
Ver
```

El navegador irá a:

```text
/usuarios/<id>
```

y mostrará:

```text
Usuario 5

Nombre Completo: Pedro González
E-mail: pedro@email.com
Fecha Creación: ...
Fecha Actualización: ...
```

---

## 4. UPDATE

Presionar:

```text
Editar
```

El formulario aparecerá precargado:

```text
Nombre: Pedro
Apellido: González
E-mail: pedro@email.com
```

Cambiar, por ejemplo:

```text
Nombre: Pedro Andrés
```

y presionar:

```text
Actualizar
```

El usuario volverá al listado y deberá aparecer:

```text
Pedro Andrés González
```

---

## 5. DELETE

Presionar:

```text
Borrar
```

El registro será eliminado y volveremos al listado.

El usuario ya no deberá aparecer.

---

# 🧭 Mapa completo de la aplicación

```text
                         /usuarios
                             │
                             ▼
                    ┌─────────────────┐
                    │ Lista Usuarios  │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
             Ver           Editar         Borrar
              │              │              │
              ▼              ▼              ▼
       /usuarios/3    /usuarios/editar/3   /usuarios/borrar/3
              │              │              │
              │              ▼              │
              │       Formulario            │
              │              │              │
              │              │ POST         │
              │              ▼              │
              │    /usuarios/3/actualizar   │
              │              │              │
              │              ▼              │
              │           UPDATE            │
              │              │              │
              │              ▼              │
              └────────── redirect() ───────┘
                             │
                             ▼
                         /usuarios
```

---

# 🧩 CRUD completo

Ahora la clase `Usuario` representa todas las operaciones principales:

```text
Usuario
│
├── save(data)
│      ↓
│   INSERT
│
├── get_all()
│      ↓
│   SELECT
│
├── get_by_id(id)
│      ↓
│   SELECT ... WHERE
│
├── update(data)
│      ↓
│   UPDATE
│
└── delete(id)
       ↓
     DELETE
```

---

# 📚 Tabla resumen del CRUD

| Operación | Método del modelo | SQL |
|---|---|---|
| Create | `save()` | `INSERT` |
| Read todos | `get_all()` | `SELECT` |
| Read uno | `get_by_id()` | `SELECT ... WHERE` |
| Update | `update()` | `UPDATE` |
| Delete | `delete()` | `DELETE` |

---

# 🧠 Conceptos nuevos de esta práctica

| Concepto | Uso |
|---|---|
| `<int:id>` | Ruta dinámica |
| `get_by_id()` | Obtener un registro específico |
| `UPDATE` | Modificar datos |
| `DELETE` | Eliminar datos |
| `value="{{ ... }}"` | Precargar formularios |
| `url_for(..., id=...)` | Generar URLs dinámicas |
| `updated_at = NOW()` | Registrar actualización |
| `WHERE id = ...` | Seleccionar el registro correcto |
| CRUD completo | Integrar las cuatro operaciones |

---

# ⚠️ Errores comunes

## Usuario no encontrado

Si:

```python
Usuario.get_by_id(id)
```

devuelve:

```python
None
```

la ruta debe responder con:

```python
return "Usuario no encontrado", 404
```

---

## `BuildError` en `url_for()`

Si la función es:

```python
def ver_usuario(id):
```

debemos utilizar:

```jinja
url_for("ver_usuario", id=usuario.id)
```

No:

```jinja
url_for("usuario", id=usuario.id)
```

---

## `BadRequestKeyError`

Si Python intenta:

```python
request.form["apellido"]
```

el HTML debe tener:

```html
name="apellido"
```

---

## UPDATE sin WHERE

Nunca utilizar:

```sql
UPDATE usuarios
SET nombre = %(nombre)s;
```

Debe existir:

```sql
WHERE id = %(id)s;
```

---

## DELETE sin WHERE

Nunca utilizar:

```sql
DELETE FROM usuarios;
```

Debe existir:

```sql
DELETE FROM usuarios
WHERE id = %(id)s;
```

---

## El formulario se muestra vacío

Revisa:

```html
value="{{ usuario.nombre }}"
```

```html
value="{{ usuario.apellido }}"
```

```html
value="{{ usuario.email }}"
```

---

## El UPDATE funciona pero no veo el cambio

Comprueba que después de:

```python
Usuario.update(data)
```

exista:

```python
return redirect(
    url_for("usuarios")
)
```

---

## El DELETE funciona pero sigo viendo al usuario

Comprueba que después de:

```python
Usuario.delete(id)
```

se ejecute:

```python
return redirect(
    url_for("usuarios")
)
```

---

# ✅ Checklist final

```text
[ ] MySQL funciona
[ ] Tabla usuarios existe
[ ] mysqlconnection.py funciona
[ ] Usuario.get_all() funciona
[ ] Usuario.get_by_id() funciona
[ ] Usuario.save() funciona
[ ] Usuario.update() funciona
[ ] Usuario.delete() funciona

[ ] GET /usuarios funciona
[ ] GET /usuarios/nuevo funciona
[ ] POST /usuarios/crear funciona
[ ] GET /usuarios/<id> funciona
[ ] GET /usuarios/editar/<id> funciona
[ ] POST /usuarios/<id>/actualizar funciona
[ ] GET /usuarios/borrar/<id> funciona

[ ] Ver funciona
[ ] Editar funciona
[ ] Borrar funciona
[ ] CREATE funciona
[ ] READ funciona
[ ] UPDATE funciona
[ ] DELETE funciona

[ ] Las sentencias utilizan parámetros
[ ] request.form funciona
[ ] url_for() funciona
[ ] redirect() funciona
[ ] Jinja2 funciona
[ ] El listado se actualiza después de CREATE
[ ] El listado se actualiza después de UPDATE
[ ] El usuario desaparece después de DELETE
```

---

# 🏁 Resultado esperado

La aplicación terminada permitirá:

```text
                     USUARIOS
                         │
             ┌───────────┴───────────┐
             │                       │
             ▼                       ▼
      Listado usuarios         Nuevo Usuario
             │
             │
      ┌──────┼───────┐
      │      │       │
      ▼      ▼       ▼
     Ver   Editar   Borrar
      │      │       │
      ▼      ▼       ▼
    READ   UPDATE   DELETE
             │
             ▼
          redirect
             │
             ▼
          /usuarios
```

El CRUD queda implementado como:

```text
┌────────────────────────────────────────────┐
│                  CRUD                      │
├────────────────────────────────────────────┤
│ CREATE  → Usuario.save()      → INSERT    │
│ READ    → get_all()           → SELECT    │
│ READ    → get_by_id()        → SELECT     │
│ UPDATE  → Usuario.update()    → UPDATE    │
│ DELETE  → Usuario.delete()    → DELETE    │
└────────────────────────────────────────────┘
```

---

# 🏆 Conclusión

Con esta actividad la aplicación deja de ser únicamente una aplicación capaz de consultar y crear usuarios.

Ahora tenemos un **CRUD completo**.

El flujo general queda:

```text
                   FLASK
                     │
                     ▼
                  RUTAS
                     │
                     ▼
                 USUARIO
                   MODEL
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
      SELECT       UPDATE       DELETE
        │            │            │
        └────────────┼────────────┘
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

La idea fundamental es que **cada operación del CRUD tiene una responsabilidad clara**:

```text
CREATE → crear
READ   → consultar
UPDATE → modificar
DELETE → eliminar
```

y todas las operaciones se realizan utilizando el modelo `Usuario`, manteniendo separadas las responsabilidades entre:

```text
Flask
POO
PyMySQL
MySQL
Jinja2
HTML
```