# 🐾 Del formulario a la base de datos — Flask + MySQL

> **Curso:** Desarrollo Web con Flask desde Cero
> **Unidad:** Integración con Bases de Datos
> **Tema:** Crear registros mediante formularios HTML
> **Tecnologías:** Python · Flask · MySQL · PyMySQL · Jinja2 · POO

---

# 📖 Descripción

Hasta este momento nuestra aplicación Flask ya puede **recuperar y visualizar mascotas almacenadas en MySQL**.

El flujo que ya conocemos es:

```text
GET /
   ↓
Mascota.get_all()
   ↓
SELECT
   ↓
MySQL
   ↓
objetos Mascota
   ↓
Jinja2
   ↓
HTML
```

Ahora agregaremos una nueva funcionalidad:

> **Permitir que el usuario complete un formulario HTML y que esa información termine almacenada en MySQL.**

El nuevo flujo será:

```text
Formulario HTML
      ↓
POST
      ↓
request.form
      ↓
diccionario datos
      ↓
Mascota.save(datos)
      ↓
INSERT
      ↓
MySQL
      ↓
redirect()
      ↓
GET /
      ↓
Mascota.get_all()
      ↓
nuevo registro visible
```

Esta es una etapa fundamental porque estamos conectando por primera vez de forma completa:

```text
HTML
 ↓
Flask
 ↓
POO
 ↓
PyMySQL
 ↓
MySQL
```

---

# 🎯 Objetivos

Al finalizar esta lección deberás ser capaz de:

- Crear un formulario HTML.
- Utilizar `method="POST"`.
- Utilizar `action`.
- Recuperar información mediante `request.form`.
- Construir un diccionario con los datos recibidos.
- Crear un método `save()` en una clase.
- Ejecutar un `INSERT` desde Python.
- Utilizar sentencias preparadas.
- Enviar un diccionario de parámetros a PyMySQL.
- Utilizar `redirect()`.
- Comprender el patrón **POST → Redirect → GET**.
- Verificar que el nuevo registro aparece nuevamente en la página.

---

# 🧠 Lo que estamos agregando

Hasta ahora teníamos:

```text
READ
```

Ahora agregaremos:

```text
CREATE
```

Por lo tanto:

```text
CRUD

C → CREATE  ← nueva funcionalidad
R → READ    ← ya implementado
U → UPDATE  ← posteriormente
D → DELETE  ← posteriormente
```

---

# 📁 Estructura del proyecto

Continuaremos utilizando el proyecto:

```text
primera_app_mysql/
│
├── server.py
├── mascota.py
├── mysqlconnection.py
├── requirements.txt
├── schema.sql
│
└── templates/
    └── index.html
```

Después de esta lección tendremos:

```text
primera_app_mysql/
│
├── server.py
├── mascota.py
├── mysqlconnection.py
├── requirements.txt
├── schema.sql
│
└── templates/
    └── index.html
```

No necesitamos crear nuevos archivos para implementar esta funcionalidad.

Modificaremos los archivos existentes.

---

# 🗄️ Base de datos

La aplicación seguirá utilizando:

```text
Base de datos:
primera_flask
```

y:

```text
Tabla:
mascotas
```

con la estructura:

```text
mascotas
│
├── id
├── nombre
├── tipo
├── color
├── created_at
└── updated_at
```

El formulario permitirá crear:

```text
nombre
tipo
color
```

Los campos:

```text
created_at
updated_at
```

serán generados mediante:

```sql
NOW()
```

---

# 🧾 `schema.sql`

Si necesitas comprobar que la tabla existe y contiene los campos esperados:

```sql
-- ==========================================================
-- BASE DE DATOS
-- ==========================================================

USE primera_flask;


-- ==========================================================
-- VERIFICAR TABLA
-- ==========================================================

DESCRIBE mascotas;


-- ==========================================================
-- VERIFICAR REGISTROS
-- ==========================================================

SELECT *
FROM mascotas;
```

Para esta práctica no necesitamos recrear la tabla si ya fue creada en la lección anterior.

---

# 🔌 `mysqlconnection.py`

La clase de conexión continúa siendo la encargada de ejecutar nuestras consultas.

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
            no devuelven registros.

        Si ocurre un error:
            devuelve False.
        """

        with self.connection.cursor() as cursor:

            try:

                # --------------------------------------------------
                # Ejecutamos la consulta.
                #
                # "query" contiene la estructura SQL.
                #
                # "data" contiene los valores variables.
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
                # Cerramos la conexión.
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

# 🧠 ¿Qué cambia realmente en esta lección?

La conexión ya estaba preparada para recibir:

```python
query_db(query, data)
```

Ahora aprovecharemos esa posibilidad para enviar datos variables.

Por ejemplo:

```python
query = """
    INSERT INTO mascotas
    (
        nombre,
        tipo,
        color,
        created_at,
        updated_at
    )
    VALUES
    (
        %(nombre)s,
        %(tipo)s,
        %(color)s,
        NOW(),
        NOW()
    );
"""
```

y:

```python
datos = {
    "nombre": "Firulais",
    "tipo": "Perro",
    "color": "Café"
}
```

Finalmente:

```python
query_db(query, datos)
```

---

# 🐕 `mascota.py`

Ahora nuestra clase `Mascota` tendrá una nueva responsabilidad:

> Crear registros en la tabla `mascotas`.

## Código completo

```python
# ==========================================================
# MODELO MASCOTA
# ==========================================================

from mysqlconnection import connectToMySQL


# ==========================================================
# CLASE MASCOTA
# ==========================================================

class Mascota:
    """
    Representa un registro de la tabla mascotas.
    """

    def __init__(self, data):
        """
        Recibe un diccionario proveniente de MySQL
        y lo transforma en un objeto Mascota.
        """

        self.id = data["id"]

        self.nombre = data["nombre"]

        self.tipo = data["tipo"]

        self.color = data["color"]

        self.created_at = data["created_at"]

        self.updated_at = data["updated_at"]


    # ======================================================
    # READ
    # OBTENER TODAS LAS MASCOTAS
    # ======================================================

    @classmethod
    def get_all(cls):
        """
        Recupera todas las mascotas de la base de datos.
        """

        query = """
            SELECT
                id,
                nombre,
                tipo,
                color,
                created_at,
                updated_at
            FROM mascotas
            ORDER BY id;
        """


        resultados = connectToMySQL(
            "primera_flask"
        ).query_db(query)


        mascotas = []


        for mascota in resultados:

            mascotas.append(
                cls(mascota)
            )


        return mascotas


    # ======================================================
    # CREATE
    # CREAR NUEVA MASCOTA
    # ======================================================

    @classmethod
    def save(cls, datos):
        """
        Crea una nueva mascota en la base de datos.

        Recibe un diccionario llamado "datos" con:

        nombre
        tipo
        color
        """

        # --------------------------------------------------
        # CONSULTA INSERT
        # --------------------------------------------------
        #
        # Los valores variables no se concatenan
        # directamente dentro del SQL.
        #
        # Utilizamos placeholders.
        # --------------------------------------------------

        query = """
            INSERT INTO mascotas
            (
                nombre,
                tipo,
                color,
                created_at,
                updated_at
            )
            VALUES
            (
                %(nombre)s,
                %(tipo)s,
                %(color)s,
                NOW(),
                NOW()
            );
        """


        # --------------------------------------------------
        # EJECUTAR CONSULTA
        # --------------------------------------------------

        return connectToMySQL(
            "primera_flask"
        ).query_db(
            query,
            datos
        )
```

---

# 🔍 ¿Qué es `save()`?

Este nuevo método:

```python
@classmethod
def save(cls, datos):
```

representa la operación:

```text
CREATE
```

Su responsabilidad es crear un nuevo registro.

Por ejemplo:

```python
datos = {
    "nombre": "Firulais",
    "tipo": "Perro",
    "color": "Café"
}
```

y:

```python
Mascota.save(datos)
```

produce un nuevo registro en MySQL.

---

# 🧩 ¿Por qué `save()` recibe un diccionario?

Porque nuestro sistema ya utiliza consultas preparadas.

Tenemos:

```python
query = """
    INSERT INTO mascotas
    (
        nombre,
        tipo,
        color,
        created_at,
        updated_at
    )
    VALUES
    (
        %(nombre)s,
        %(tipo)s,
        %(color)s,
        NOW(),
        NOW()
    );
"""
```

y los valores:

```python
datos = {
    "nombre": nombre,
    "tipo": tipo,
    "color": color
}
```

El diccionario permite relacionar cada placeholder con su valor.

---

# 🔗 Relación entre `query` y `datos`

Observa:

```text
QUERY

%(nombre)s
     ↓
datos["nombre"]

%(tipo)s
     ↓
datos["tipo"]

%(color)s
     ↓
datos["color"]
```

Por eso las claves del diccionario deben coincidir exactamente.

Correcto:

```python
datos = {
    "nombre": "Firulais",
    "tipo": "Perro",
    "color": "Café"
}
```

Incorrecto:

```python
datos = {
    "nombre_mascota": "Firulais",
    "tipo_mascota": "Perro",
    "color_mascota": "Café"
}
```

porque el SQL espera:

```text
nombre
tipo
color
```

---

# 🔐 ¿Por qué utilizamos una sentencia preparada?

No debemos construir SQL así:

```python
query = f"""
    INSERT INTO mascotas
    (nombre, tipo, color)
    VALUES
    ('{nombre}', '{tipo}', '{color}');
"""
```

Tampoco:

```python
query = (
    "INSERT INTO mascotas "
    "(nombre, tipo, color) "
    "VALUES ('"
    + nombre
    + "', '"
    + tipo
    + "', '"
    + color
    + "')"
)
```

La forma correcta es separar:

```text
Consulta SQL
```

de:

```text
Valores
```

mediante parámetros.

Esto es especialmente importante cuando los valores provienen del usuario.

---

# 🧾 `templates/index.html`

Ahora agregaremos el formulario a la misma página donde ya mostramos las mascotas.

El usuario verá:

```text
Las mascotas

Nombre: Firulais
Tipo: Perro
Color: Café

----------------------------

Agregar una mascota

Nombre: [____________]

Tipo:   [____________]

Color:  [____________]

[Agregar Mascota]
```

## Código completo

```html
<!DOCTYPE html>
<html lang="es">

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>Mascotas</title>

</head>

<body>

    <!-- ==================================================
         LISTADO DE MASCOTAS
    =================================================== -->

    <h1>Las mascotas</h1>


    {% if mascotas %}

        {% for mascota in mascotas %}

            <p>

                <b>Nombre:</b>
                {{ mascota.nombre }}

                <br>

                <b>Tipo:</b>
                {{ mascota.tipo }}

                <br>

                <b>Color:</b>
                {{ mascota.color }}

            </p>

        {% endfor %}

    {% else %}

        <p>

            No existen mascotas registradas.

        </p>

    {% endif %}


    <!-- ==================================================
         FORMULARIO
    =================================================== -->

    <hr>


    <h2>Agregar una mascota</h2>


    <form
        action="{{ url_for('crear_mascota') }}"
        method="POST"
    >

        <!-- NOMBRE -->

        <label for="nombre">
            Nombre:
        </label>

        <input
            type="text"
            id="nombre"
            name="nombre"
            required
        >

        <br>


        <!-- TIPO -->

        <label for="tipo">
            Tipo:
        </label>

        <input
            type="text"
            id="tipo"
            name="tipo"
            required
        >

        <br>


        <!-- COLOR -->

        <label for="color">
            Color:
        </label>

        <input
            type="text"
            id="color"
            name="color"
            required
        >

        <br>


        <!-- BOTÓN -->

        <input
            type="submit"
            value="Agregar Mascota"
        >

    </form>

</body>

</html>
```

---

# 🔍 Analizando el formulario

La estructura principal es:

```html
<form
    action="{{ url_for('crear_mascota') }}"
    method="POST"
>
```

Tenemos dos conceptos nuevos que ya conocíamos por separado.

## `action`

Indica qué ruta recibirá la información.

```jinja
{{ url_for('crear_mascota') }}
```

genera:

```text
/crear_mascota
```

---

## `method`

Indica cómo enviaremos la información:

```html
method="POST"
```

Por lo tanto:

```text
Formulario
   ↓
POST
   ↓
/crear_mascota
```

---

# 🏷️ Importancia de `name`

Este campo:

```html
<input
    type="text"
    name="nombre"
>
```

es fundamental.

El atributo:

```text
name="nombre"
```

será utilizado posteriormente por Flask:

```python
request.form["nombre"]
```

Tenemos la siguiente relación:

```text
HTML
│
└── name="nombre"
         │
         ▼
Flask
│
└── request.form["nombre"]
```

Lo mismo ocurre con:

```text
name="tipo"
```

y:

```text
name="color"
```

---

# 📤 `server.py`

Ahora necesitamos crear la ruta encargada de recibir el formulario.

El archivo completo queda:

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


from mascota import Mascota


# ==========================================================
# CREAR APLICACIÓN
# ==========================================================

app = Flask(__name__)


# ==========================================================
# READ
# MOSTRAR MASCOTAS
# ==========================================================

@app.route("/")
def index():
    """
    Recupera todas las mascotas y las envía
    a index.html.
    """

    mascotas = Mascota.get_all()


    return render_template(
        "index.html",
        mascotas=mascotas
    )


# ==========================================================
# CREATE
# CREAR MASCOTA
# ==========================================================

@app.route(
    "/crear_mascota",
    methods=["POST"]
)
def crear_mascota():
    """
    Recibe la información del formulario
    y crea una nueva mascota.
    """

    # ------------------------------------------------------
    # RECIBIR INFORMACIÓN
    # ------------------------------------------------------

    datos = {

        "nombre": request.form["nombre"],

        "tipo": request.form["tipo"],

        "color": request.form["color"]

    }


    # ------------------------------------------------------
    # ENVIAR DATOS AL MODELO
    # ------------------------------------------------------

    Mascota.save(datos)


    # ------------------------------------------------------
    # REDIRECCIONAR
    # ------------------------------------------------------
    #
    # Después de recibir un POST utilizamos redirect()
    # para volver a la ruta principal.
    #
    # Flujo:
    #
    # POST /crear_mascota
    #       ↓
    # INSERT
    #       ↓
    # redirect
    #       ↓
    # GET /
    #
    # ------------------------------------------------------

    return redirect(
        url_for("index")
    )


# ==========================================================
# EJECUTAR SERVIDOR
# ==========================================================

if __name__ == "__main__":

    app.run(debug=True)
```

---

# 🔍 Analizando `request.form`

Cuando el usuario completa:

```text
Nombre → Firulais
Tipo   → Perro
Color  → Café
```

el navegador envía mediante POST información equivalente a:

```text
nombre=Firulais
tipo=Perro
color=Café
```

Flask la recibe en:

```python
request.form
```

Podemos imaginarlo como:

```python
{
    "nombre": "Firulais",
    "tipo": "Perro",
    "color": "Café"
}
```

Por eso podemos utilizar:

```python
request.form["nombre"]
```

para recuperar:

```text
Firulais
```

---

# 📦 Construcción del diccionario

En el servidor hacemos:

```python
datos = {
    "nombre": request.form["nombre"],
    "tipo": request.form["tipo"],
    "color": request.form["color"]
}
```

Si el usuario ingresó:

```text
Firulais
Perro
Café
```

el resultado será:

```python
datos = {
    "nombre": "Firulais",
    "tipo": "Perro",
    "color": "Café"
}
```

Este diccionario será enviado al modelo:

```python
Mascota.save(datos)
```

---

# 🔗 Flask → Modelo

Aquí ocurre una separación muy importante.

`server.py` **no contiene el SQL**.

En `server.py` solamente hacemos:

```python
Mascota.save(datos)
```

La clase `Mascota` es la responsable de saber cómo guardar esos datos.

Por lo tanto:

```text
server.py
   ↓
Mascota.save()
   ↓
mascota.py
   ↓
SQL
```

Esto mantiene separadas las responsabilidades.

---

# 💾 Mascota → MySQL

Dentro de `Mascota.save()` tenemos:

```python
query = """
    INSERT INTO mascotas
    (
        nombre,
        tipo,
        color,
        created_at,
        updated_at
    )
    VALUES
    (
        %(nombre)s,
        %(tipo)s,
        %(color)s,
        NOW(),
        NOW()
    );
"""
```

y:

```python
return connectToMySQL(
    "primera_flask"
).query_db(
    query,
    datos
)
```

Por lo tanto:

```text
datos
 ↓
query_db()
 ↓
PyMySQL
 ↓
MySQL
 ↓
INSERT
```

---

# 🔄 ¿Por qué usamos `redirect()`?

Después de guardar:

```python
Mascota.save(datos)
```

no queremos mantener al usuario en:

```text
POST /crear_mascota
```

En su lugar:

```python
return redirect(
    url_for("index")
)
```

provocará que el navegador vuelva a solicitar:

```text
GET /
```

El flujo completo:

```text
POST /crear_mascota
        ↓
request.form
        ↓
datos
        ↓
Mascota.save(datos)
        ↓
INSERT
        ↓
MySQL
        ↓
redirect()
        ↓
GET /
        ↓
Mascota.get_all()
        ↓
SELECT
        ↓
Jinja2
        ↓
nuevo registro visible
```

---

# 🧠 POST → Redirect → GET

Este patrón se conoce como:

> **POST → Redirect → GET (PRG)**

Es una técnica habitual al trabajar con formularios que crean o modifican información.

La idea es:

```text
POST
 ↓
procesar
 ↓
guardar
 ↓
redirect
 ↓
GET
 ↓
mostrar
```

---

# ❓ ¿`redirect()` guarda los datos?

No.

Esto es muy importante.

`redirect()` **no guarda nada en la base de datos**.

Los datos se guardan aquí:

```python
Mascota.save(datos)
```

y dentro de:

```python
INSERT
```

`redirect()` solamente le indica al navegador:

> "Ahora ve a esta otra ruta."

Por eso podemos separar conceptualmente:

```text
Mascota.save()
→ guarda

redirect()
→ navega
```

---

# 🧪 Prueba completa

## Estado inicial

Visita:

```text
http://127.0.0.1:5000/
```

Podrías ver:

```text
Las mascotas

Nombre: Firulais
Tipo: Perro
Color: Café

Nombre: Michi
Tipo: Gato
Color: Negro
```

y el formulario:

```text
Agregar una mascota

Nombre: [____________]

Tipo:   [____________]

Color:  [____________]

[Agregar Mascota]
```

---

# ✍️ Crear una mascota

Completa:

```text
Nombre:
Rocky

Tipo:
Perro

Color:
Negro
```

y presiona:

```text
Agregar Mascota
```

El navegador enviará:

```text
POST /crear_mascota
```

---

# 🔍 ¿Qué ocurre en el servidor?

Primero:

```python
request.form["nombre"]
```

obtiene:

```text
Rocky
```

Luego:

```python
request.form["tipo"]
```

obtiene:

```text
Perro
```

Finalmente:

```python
request.form["color"]
```

obtiene:

```text
Negro
```

Se construye:

```python
datos = {
    "nombre": "Rocky",
    "tipo": "Perro",
    "color": "Negro"
}
```

---

# 💾 INSERT

`Mascota.save(datos)` ejecutará:

```sql
INSERT INTO mascotas
(
    nombre,
    tipo,
    color,
    created_at,
    updated_at
)
VALUES
(
    'Rocky',
    'Perro',
    'Negro',
    NOW(),
    NOW()
);
```

La consulta real será construida y ejecutada mediante PyMySQL utilizando los parámetros preparados.

---

# 🔄 Volver al listado

Después del INSERT:

```python
redirect(url_for("index"))
```

El navegador realiza:

```text
GET /
```

Entonces Flask vuelve a ejecutar:

```python
mascotas = Mascota.get_all()
```

y obtiene:

```text
Firulais
Michi
Rocky
...
```

Por eso el nuevo registro aparece automáticamente.

---

# 🧪 Verificar directamente en MySQL

También podemos comprobarlo desde MySQL Workbench:

```sql
USE primera_flask;

SELECT *
FROM mascotas;
```

Debería aparecer el nuevo registro.

---

# 🖥️ Consultar la terminal

Durante el desarrollo puede ser útil observar la terminal de Flask.

Si algo falla, revisa:

```text
Running Query:
...
```

Esto permite comprobar qué consulta está intentando ejecutar la aplicación.

Si la consulta falla, copia el SQL y pruébalo directamente en MySQL Workbench.

Esto ayuda a determinar si el problema está en:

```text
Python
```

o en:

```text
SQL
```

---

# ⚠️ Errores comunes

## 1. `BadRequestKeyError`

Si Flask muestra un error relacionado con:

```python
request.form["nombre"]
```

revisa el HTML.

Debe existir:

```html
<input
    type="text"
    name="nombre"
>
```

El valor de `name` debe coincidir exactamente.

---

## 2. Las claves del diccionario no coinciden

Correcto:

```python
datos = {
    "nombre": ...,
    "tipo": ...,
    "color": ...
}
```

porque el SQL espera:

```text
%(nombre)s
%(tipo)s
%(color)s
```

Incorrecto:

```python
datos = {
    "nombre_mascota": ...,
    "tipo_mascota": ...,
    "color_mascota": ...
}
```

---

## 3. El formulario no llega al servidor

Revisa:

```html
<form
    action="{{ url_for('crear_mascota') }}"
    method="POST"
>
```

y:

```python
@app.route(
    "/crear_mascota",
    methods=["POST"]
)
```

El método debe coincidir.

---

## 4. El registro no aparece

Revisa que:

```python
Mascota.save(datos)
```

se ejecute correctamente.

Luego verifica la base de datos:

```sql
SELECT *
FROM mascotas;
```

Y finalmente comprueba que:

```python
Mascota.get_all()
```

esté recuperando el registro.

---

## 5. Error SQL

Revisa:

- nombre de la tabla;
- nombres de columnas;
- placeholders;
- sintaxis;
- nombre de la base de datos.

La consulta esperada es:

```sql
INSERT INTO mascotas
(
    nombre,
    tipo,
    color,
    created_at,
    updated_at
)
VALUES
(
    %(nombre)s,
    %(tipo)s,
    %(color)s,
    NOW(),
    NOW()
);
```

---

# 📚 Conceptos nuevos de esta lección

| Concepto | Función |
|---|---|
| `<form>` | Crear formulario HTML |
| `action` | Indicar qué ruta recibirá los datos |
| `method="POST"` | Enviar información al servidor |
| `name` | Identificar cada dato |
| `request.form` | Obtener los datos enviados |
| Diccionario `datos` | Agrupar valores |
| `save()` | Crear registro mediante el modelo |
| `INSERT` | Crear registro en MySQL |
| Sentencia preparada | Separar SQL y valores |
| `redirect()` | Redirigir al usuario |
| `url_for()` | Generar la URL |
| POST → Redirect → GET | Flujo recomendado después del POST |

---

# 🧠 Modelo mental

Cuando veas un formulario conectado a una base de datos, piensa:

```text
┌─────────────────────┐
│      HTML           │
│                     │
│ Nombre: [_______]   │
│ Tipo:   [_______]   │
│ Color:  [_______]   │
│                     │
│ [Agregar Mascota]   │
└──────────┬──────────┘
           │
           │ POST
           ▼
┌─────────────────────┐
│       Flask         │
│                     │
│ request.form        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   diccionario       │
│      datos          │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Mascota.save()    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│     INSERT SQL      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│       MySQL         │
└──────────┬──────────┘
           │
           ▼
       redirect()
           │
           ▼
        GET /
           │
           ▼
   Mascota.get_all()
           │
           ▼
       SELECT
           │
           ▼
       Jinja2
           │
           ▼
      HTML actualizado
```

---

# ✅ Checklist final

```text
[ ] La tabla mascotas existe
[ ] MySQL está funcionando
[ ] Flask puede conectarse a MySQL
[ ] mysqlconnection.py funciona
[ ] Mascota.get_all() funciona
[ ] Mascota.save() fue creado
[ ] El formulario tiene method="POST"
[ ] El formulario tiene action correcto
[ ] Cada input tiene name
[ ] request.form recibe los datos
[ ] Se crea el diccionario datos
[ ] Las claves coinciden con el SQL
[ ] La consulta utiliza parámetros
[ ] INSERT funciona
[ ] redirect() funciona
[ ] GET / vuelve a consultar las mascotas
[ ] El nuevo registro aparece en pantalla
[ ] El nuevo registro aparece en MySQL Workbench
```

---

# 🏁 Resultado final

Al completar la actividad, la aplicación habrá evolucionado de:

```text
                READ
                  │
                  ▼
             SELECT
                  │
                  ▼
               MySQL
                  │
                  ▼
             mostrar datos
```

a:

```text
                 CREATE + READ

FORMULARIO
    │
    │ POST
    ▼
request.form
    │
    ▼
datos
    │
    ▼
Mascota.save()
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
GET /
    │
    ▼
Mascota.get_all()
    │
    ▼
SELECT
    │
    ▼
Jinja2
    │
    ▼
nuevo registro visible
```

La idea fundamental de esta lección es:

> **El formulario recolecta los datos, Flask los recibe, el modelo los envía a MySQL mediante una sentencia preparada y `redirect()` nos devuelve al listado para consultar nuevamente los datos almacenados.**

Con esto ya tenemos implementadas dos operaciones fundamentales de CRUD:

```text
C → CREATE ✅
R → READ   ✅
U → UPDATE ⏳
D → DELETE ⏳
```