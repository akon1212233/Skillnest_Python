# 🔎 Consultas con datos variables en Flask y MySQL

> **Curso:** Desarrollo Web con Flask desde Cero  
> **Unidad:** Integración con Bases de Datos  
> **Tema:** Consultas SQL con valores variables y sentencias preparadas  
> **Tecnologías:** Python · Flask · MySQL · PyMySQL · POO

---

# 📖 Descripción

En la lección anterior aprendimos a recuperar todos los registros de una tabla mediante una consulta como:

```sql
SELECT * FROM mascotas;
```

El problema es que una aplicación real rara vez necesita obtener siempre todos los registros.

Normalmente necesitamos realizar consultas utilizando información que puede cambiar.

Por ejemplo:

```sql
SELECT *
FROM mascotas
WHERE id = 3;
```

o:

```sql
SELECT *
FROM mascotas
WHERE nombre = "Firulais";
```

También podemos necesitar modificar información:

```sql
UPDATE mascotas
SET nombre = "Maria"
WHERE id = 3;
```

En estos casos los valores:

```text
3
Firulais
Maria
```

pueden cambiar.

Por eso no debemos construir manualmente una cadena SQL cada vez que necesitemos utilizar datos variables.

En esta lección aprenderemos a utilizar **sentencias preparadas** mediante parámetros y diccionarios.

---

# 🎯 Objetivos

Al finalizar esta lección deberás comprender cómo:

- Crear consultas SQL con valores variables.
- Utilizar parámetros en consultas SQL.
- Crear diccionarios para enviar valores a MySQL.
- Utilizar el patrón:

```python
query = "..."
data = {...}
```

- Ejecutar consultas mediante `query_db(query, data)`.
- Consultar registros mediante un identificador.
- Utilizar `WHERE` con valores dinámicos.
- Utilizar parámetros en `UPDATE`.
- Comprender por qué no debemos concatenar valores directamente en SQL.
- Mantener separadas la consulta SQL y la información variable.

---

# 🧠 El problema

Supongamos que queremos buscar una mascota por ID.

Podríamos pensar inicialmente en esto:

```python
id_mascota = 3

query = f"SELECT * FROM mascotas WHERE id = {id_mascota};"
```

Aunque puede parecer sencillo, **no trabajaremos de esta manera**.

El objetivo es utilizar una consulta preparada.

La consulta tendrá una estructura como:

```python
query = """
    SELECT *
    FROM mascotas
    WHERE id = %(id_mascota)s;
"""
```

Y los datos viajarán aparte:

```python
data = {
    "id_mascota": id_mascota
}
```

Posteriormente enviaremos ambos valores:

```python
connectToMySQL("primera_flask").query_db(
    query,
    data
)
```

---

# 🔐 ¿Por qué utilizar sentencias preparadas?

Separar la consulta de los valores permite que el controlador de base de datos maneje correctamente los parámetros.

Evita que tengamos que construir manualmente consultas como:

```python
"SELECT * FROM mascotas WHERE nombre = '" + nombre + "'"
```

o:

```python
f"SELECT * FROM mascotas WHERE nombre = '{nombre}'"
```

Este tipo de concatenación puede abrir la puerta a problemas de **SQL Injection** cuando los datos provienen de usuarios.

En esta etapa no necesitamos estudiar todavía SQL Injection en profundidad.

La regla importante es:

> **Cuando una consulta SQL utiliza datos variables, no concatenes esos valores directamente en la cadena SQL. Utiliza parámetros.**

---

# 📁 Estructura del proyecto

Continuaremos utilizando el proyecto:

```text
primera_app_mysql/
│
├── app.py
├── mascota.py
├── mysqlconnection.py
├── schema.sql
├── requirements.txt
├── .gitignore
│
└── templates/
    ├── index.html
    └── mascota.html
```

---

# 🗄️ Base de datos

Utilizaremos la misma base de datos:

```text
primera_flask
```

y la tabla:

```text
mascotas
```

---

# 🧾 `schema.sql`

Utiliza este script para disponer de datos de prueba.

```sql
-- ==========================================================
-- BASE DE DATOS
-- ==========================================================

CREATE DATABASE IF NOT EXISTS primera_flask;

USE primera_flask;


-- ==========================================================
-- TABLA MASCOTAS
-- ==========================================================

CREATE TABLE IF NOT EXISTS mascotas (

    id INT AUTO_INCREMENT PRIMARY KEY,

    nombre VARCHAR(100) NOT NULL,

    tipo VARCHAR(100) NOT NULL,

    color VARCHAR(100) NOT NULL,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);


-- ==========================================================
-- DATOS DE PRUEBA
-- ==========================================================

INSERT INTO mascotas
    (nombre, tipo, color)
VALUES
    ("Firulais", "Perro", "Café"),
    ("Michi", "Gato", "Negro"),
    ("Luna", "Perro", "Blanco"),
    ("Nala", "Gato", "Naranjo"),
    ("Coco", "Conejo", "Blanco");
```

---

# 🔌 `mysqlconnection.py`

Nuestra clase de conexión ya recibe dos argumentos:

```python
query
```

y:

```python
data
```

Por lo tanto podemos utilizarla para consultas variables.

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
    Administra una conexión con una base de datos MySQL.
    """

    def __init__(self, db):
        """
        Establece una conexión con la base de datos
        recibida como parámetro.
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

        query:
            Cadena con la consulta SQL.

        data:
            Diccionario con los valores que serán enviados
            a los parámetros de la consulta.
        """

        with self.connection.cursor() as cursor:

            try:

                # --------------------------------------------------
                # Ejecutar consulta con parámetros.
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
# FUNCIÓN DE CONEXIÓN
# ==========================================================

def connectToMySQL(db):
    """
    Crea y devuelve una instancia de MySQLConnection.
    """

    return MySQLConnection(db)
```

---

# 🔍 Lo importante de `query_db()`

Observa:

```python
def query_db(self, query, data=None):
```

Tenemos dos parámetros.

### `query`

Contiene la consulta SQL:

```python
query = """
    SELECT *
    FROM mascotas
    WHERE id = %(id_mascota)s;
"""
```

### `data`

Contiene los valores variables:

```python
data = {
    "id_mascota": 3
}
```

Finalmente:

```python
cursor.execute(query, data)
```

envía ambos a PyMySQL.

---

# 🧩 La estructura de una consulta preparada

La forma general será:

```python
query = """
    SQL
    WHERE campo = %(nombre_clave)s;
"""

data = {
    "nombre_clave": valor
}
```

La clave del diccionario debe coincidir con el nombre utilizado dentro del query.

Por ejemplo:

```python
query = """
    SELECT *
    FROM mascotas
    WHERE id = %(id_mascota)s;
"""
```

y:

```python
data = {
    "id_mascota": 3
}
```

La correspondencia es:

```text
%(id_mascota)s
       ↑
       │
       └── "id_mascota"
```

---

# 📌 ¿Qué significa `%(`nombre`)s`?

Esta parte:

```python
%(id_mascota)s
```

es un **placeholder**.

No representa literalmente el valor `3`.

Representa un espacio reservado donde PyMySQL colocará el valor enviado mediante:

```python
data = {
    "id_mascota": 3
}
```

Podemos pensar:

```text
QUERY
│
└── %(id_mascota)s
          │
          ▼
DATA
│
└── "id_mascota": 3
```

---

# 🐕 `mascota.py`

Ahora agregaremos una consulta que permita buscar una mascota específica mediante su ID.

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
        Convierte un diccionario de MySQL en un objeto Mascota.
        """

        self.id = data["id"]

        self.nombre = data["nombre"]

        self.tipo = data["tipo"]

        self.color = data["color"]

        self.created_at = data["created_at"]

        self.updated_at = data["updated_at"]


    # ======================================================
    # OBTENER TODAS LAS MASCOTAS
    # ======================================================

    @classmethod
    def get_all(cls):
        """
        Devuelve todas las mascotas de la base de datos.
        """

        query = """
            SELECT *
            FROM mascotas;
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
    # OBTENER MASCOTA POR ID
    # ======================================================

    @classmethod
    def get_by_id(cls, id):
        """
        Busca una mascota utilizando su ID.

        El ID recibido desde Python se envía como parámetro
        de una sentencia preparada.
        """

        # --------------------------------------------------
        # QUERY
        # --------------------------------------------------

        query = """
            SELECT *
            FROM mascotas
            WHERE id = %(id_mascota)s;
        """


        # --------------------------------------------------
        # DATOS VARIABLES
        # --------------------------------------------------

        data = {
            "id_mascota": id
        }


        # --------------------------------------------------
        # EJECUTAR CONSULTA
        # --------------------------------------------------

        resultados = connectToMySQL(
            "primera_flask"
        ).query_db(
            query,
            data
        )


        # --------------------------------------------------
        # COMPROBAR RESULTADO
        # --------------------------------------------------

        if resultados:

            return cls(
                resultados[0]
            )


        return None
```

---

# 🔍 Analizando `get_by_id()`

La función recibe:

```python
def get_by_id(cls, id):
```

Por ejemplo:

```python
Mascota.get_by_id(3)
```

En ese momento:

```python
id
```

vale:

```text
3
```

---

# 🧾 Construimos el `query`

Tenemos:

```python
query = """
    SELECT *
    FROM mascotas
    WHERE id = %(id_mascota)s;
"""
```

Observa que **no hemos escrito**:

```text
WHERE id = 3
```

Estamos dejando un espacio reservado:

```text
%(id_mascota)s
```

---

# 📦 Construimos `data`

Creamos:

```python
data = {
    "id_mascota": id
}
```

Si `id` vale:

```text
3
```

el diccionario será:

```python
{
    "id_mascota": 3
}
```

---

# 🔗 Enviamos ambos

Finalmente:

```python
connectToMySQL(
    "primera_flask"
).query_db(
    query,
    data
)
```

Estamos diciendo:

> Utiliza la base de datos `primera_flask`, ejecuta este `query` y utiliza este diccionario como fuente de los valores variables.

---

# 📊 ¿Qué devuelve `SELECT`?

Recordemos que nuestro `query_db()` devuelve:

```python
cursor.fetchall()
```

por lo tanto recibiremos una lista.

Por ejemplo:

```python
[
    {
        "id": 3,
        "nombre": "Luna",
        "tipo": "Perro",
        "color": "Blanco"
    }
]
```

Como estamos buscando una sola mascota, tomamos:

```python
resultados[0]
```

y obtenemos:

```python
{
    "id": 3,
    "nombre": "Luna",
    "tipo": "Perro",
    "color": "Blanco"
}
```

Luego hacemos:

```python
return cls(
    resultados[0]
)
```

que transforma el diccionario en:

```python
Mascota(...)
```

---

# 🌐 `app.py`

Ahora utilizaremos el nuevo método desde Flask.

## Código completo

```python
# ==========================================================
# SERVIDOR FLASK
# ==========================================================

from flask import Flask, render_template

from mascota import Mascota


# ==========================================================
# CREAR APLICACIÓN
# ==========================================================

app = Flask(__name__)


# ==========================================================
# RUTA PRINCIPAL
# ==========================================================

@app.route("/")
def index():
    """
    Muestra todas las mascotas.
    """

    mascotas = Mascota.get_all()

    return render_template(
        "index.html",
        mascotas=mascotas
    )


# ==========================================================
# RUTA PARA BUSCAR MASCOTA POR ID
# ==========================================================

@app.route("/mascota/<int:id>")
def mostrar_mascota(id):
    """
    Recibe un ID desde la URL y busca la mascota
    correspondiente en la base de datos.
    """

    mascota = Mascota.get_by_id(id)


    # ------------------------------------------------------
    # Si no existe la mascota, mostramos un mensaje.
    # ------------------------------------------------------

    if mascota is None:

        return "Mascota no encontrada", 404


    # ------------------------------------------------------
    # Mostrar mascota encontrada.
    # ------------------------------------------------------

    return render_template(
        "mascota.html",
        mascota=mascota
    )


# ==========================================================
# EJECUTAR SERVIDOR
# ==========================================================

if __name__ == "__main__":

    app.run(debug=True)
```

---

# 🔍 ¿Qué ocurre en `/mascota/<int:id>`?

Esta ruta:

```python
@app.route("/mascota/<int:id>")
```

permite URLs como:

```text
/mascota/1
```

```text
/mascota/3
```

```text
/mascota/5
```

Flask convierte automáticamente:

```text
"3"
```

en:

```python
3
```

gracias a:

```text
<int:id>
```

---

# 🔄 Flujo completo

Si visitamos:

```text
http://127.0.0.1:5000/mascota/3
```

ocurre:

```text
URL
 ↓
id = 3
 ↓
mostrar_mascota(3)
 ↓
Mascota.get_by_id(3)
 ↓
query
 ↓
data = {"id_mascota": 3}
 ↓
query_db(query, data)
 ↓
MySQL
 ↓
SELECT
 ↓
resultado
 ↓
Mascota(resultado)
 ↓
mascota.html
```

---

# 🖥️ `templates/index.html`

Esta plantilla mostrará todas las mascotas y permitirá acceder a su información individual.

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

    <h1>Listado de Mascotas</h1>


    {% if mascotas %}

        <ul>

            {% for mascota in mascotas %}

                <li>

                    <strong>
                        {{ mascota.nombre }}
                    </strong>

                    -

                    {{ mascota.tipo }}

                    -

                    {{ mascota.color }}


                    <a
                        href="{{ url_for('mostrar_mascota', id=mascota.id) }}"
                    >

                        Ver detalles

                    </a>

                </li>

            {% endfor %}

        </ul>

    {% else %}

        <p>
            No existen mascotas registradas.
        </p>

    {% endif %}

</body>

</html>
```

---

# 🔗 `url_for()` con una variable

Aquí aparece una nueva forma de utilizar `url_for()`:

```jinja
{{ url_for(
    'mostrar_mascota',
    id=mascota.id
) }}
```

Nuestra ruta es:

```python
@app.route("/mascota/<int:id>")
```

y su función:

```python
def mostrar_mascota(id):
```

Por eso enviamos:

```python
id=mascota.id
```

Si la mascota tiene:

```python
id = 3
```

Flask generará:

```text
/mascota/3
```

---

# 🖥️ `templates/mascota.html`

Esta plantilla mostrará una mascota específica.

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

    <title>{{ mascota.nombre }}</title>

</head>

<body>

    <h1>

        {{ mascota.nombre }}

    </h1>


    <p>

        <strong>ID:</strong>

        {{ mascota.id }}

    </p>


    <p>

        <strong>Tipo:</strong>

        {{ mascota.tipo }}

    </p>


    <p>

        <strong>Color:</strong>

        {{ mascota.color }}

    </p>


    <p>

        <strong>Fecha de creación:</strong>

        {{ mascota.created_at }}

    </p>


    <p>

        <strong>Última actualización:</strong>

        {{ mascota.updated_at }}

    </p>


    <a href="{{ url_for('index') }}">

        Volver al listado

    </a>

</body>

</html>
```

---

# 🧪 Ejemplo práctico

Tenemos en MySQL:

```text
id | nombre   | tipo   | color
---|----------|--------|--------
1  | Firulais | Perro  | Café
2  | Michi    | Gato   | Negro
3  | Luna     | Perro  | Blanco
```

Visitamos:

```text
/mascota/3
```

Flask recibe:

```python
id = 3
```

El modelo prepara:

```python
query = """
    SELECT *
    FROM mascotas
    WHERE id = %(id_mascota)s;
"""
```

y:

```python
data = {
    "id_mascota": 3
}
```

MySQL devuelve:

```python
[
    {
        "id": 3,
        "nombre": "Luna",
        "tipo": "Perro",
        "color": "Blanco"
    }
]
```

Y finalmente la plantilla muestra:

```text
Luna

ID: 3
Tipo: Perro
Color: Blanco
```

---

# ✏️ Consultas `UPDATE`

El mismo patrón se utilizará posteriormente para modificar información.

Por ejemplo:

```python
query = """
    UPDATE mascotas
    SET nombre = %(nombre_mascota)s
    WHERE id = %(id_mascota)s;
"""
```

Y los valores:

```python
data = {
    "nombre_mascota": "Maria",
    "id_mascota": 3
}
```

Observa que tenemos **dos valores variables**:

```text
nombre_mascota
id_mascota
```

y ambos están dentro del diccionario.

---

# 🧠 Más de un parámetro

Una consulta puede utilizar tantos parámetros como sean necesarios.

Por ejemplo:

```python
query = """
    SELECT *
    FROM mascotas
    WHERE tipo = %(tipo_mascota)s
    AND color = %(color_mascota)s;
"""
```

Y:

```python
data = {
    "tipo_mascota": "Perro",
    "color_mascota": "Blanco"
}
```

La estructura es:

```text
QUERY
│
├── %(tipo_mascota)s
│
└── %(color_mascota)s

DATA
│
├── tipo_mascota → "Perro"
│
└── color_mascota → "Blanco"
```

---

# ⚠️ Error común: concatenar variables

Evita:

```python
id = 3

query = (
    "SELECT * FROM mascotas WHERE id = "
    + str(id)
)
```

También evita:

```python
query = f"""
    SELECT *
    FROM mascotas
    WHERE id = {id};
"""
```

En su lugar:

```python
query = """
    SELECT *
    FROM mascotas
    WHERE id = %(id_mascota)s;
"""
```

y:

```python
data = {
    "id_mascota": id
}
```

---

# 🧠 Regla fundamental

Cuando tengas una consulta variable, piensa siempre en dos elementos:

### 1. El `query`

```python
query = """
    SELECT *
    FROM mascotas
    WHERE id = %(id_mascota)s;
"""
```

### 2. El `data`

```python
data = {
    "id_mascota": id
}
```

Luego:

```python
connectToMySQL(
    "primera_flask"
).query_db(
    query,
    data
)
```

---

# 📚 Resumen

## Consulta fija

Cuando no existen variables:

```python
query = """
    SELECT *
    FROM mascotas;
"""

connectToMySQL(
    "primera_flask"
).query_db(query)
```

---

## Consulta variable

Cuando existen valores dinámicos:

```python
query = """
    SELECT *
    FROM mascotas
    WHERE id = %(id_mascota)s;
"""

data = {
    "id_mascota": 3
}

connectToMySQL(
    "primera_flask"
).query_db(
    query,
    data
)
```

---

# 📝 Actividad de consolidación

Agrega al modelo `Mascota` un método:

```python
@classmethod
def get_by_name(cls, nombre):
```

que permita buscar una mascota por nombre.

La consulta deberá seguir el patrón:

```python
query = """
    SELECT *
    FROM mascotas
    WHERE nombre = %(nombre_mascota)s;
"""
```

y:

```python
data = {
    "nombre_mascota": nombre
}
```

Después crea una ruta que permita consultar, por ejemplo:

```text
/mascota/nombre/Firulais
```

y mostrar la información de la mascota encontrada.

---

# 🚀 Desafío

Crea un método:

```python
@classmethod
def get_by_tipo(cls, tipo):
```

que devuelva todas las mascotas de un determinado tipo.

Por ejemplo:

```python
Mascota.get_by_tipo("Perro")
```

debería ejecutar una consulta equivalente a:

```sql
SELECT *
FROM mascotas
WHERE tipo = %(tipo_mascota)s;
```

El método deberá devolver una **lista de objetos `Mascota`**, no una lista de diccionarios.

---

# 🏁 Conclusión

En esta lección aprendimos a pasar información variable a las consultas SQL sin construir manualmente las cadenas.

El patrón fundamental es:

```text
            QUERY
              │
              │
              ▼
SELECT ... WHERE id = %(id_mascota)s
              │
              │
              │
            DATA
              │
              ▼
{"id_mascota": 3}
              │
              ▼
         PyMySQL
              │
              ▼
            MySQL
```

La idea más importante que debes recordar es:

> **La consulta SQL define la estructura y el diccionario `data` proporciona los valores variables.**

Por eso trabajaremos siempre con:

```python
query = """
    ...
    %(nombre_clave)s
    ...
"""
```

y:

```python
data = {
    "nombre_clave": valor
}
```

Este mecanismo será fundamental en las próximas operaciones CRUD, especialmente cuando comencemos a utilizar:

```text
SELECT
INSERT
UPDATE
DELETE
```

con información proporcionada dinámicamente por el usuario.
Mostrando README.md