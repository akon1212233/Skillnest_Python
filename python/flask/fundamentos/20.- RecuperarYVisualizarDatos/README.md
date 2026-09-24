# 🐾 Recuperar y visualizar datos desde MySQL con Flask

> **Curso:** Desarrollo Web con Flask desde Cero  
> **Unidad:** Integración con Bases de Datos  
> **Práctica:** Recuperar y visualizar datos  
> **Tecnologías:** Python · Flask · MySQL · PyMySQL · Jinja2 · POO

---

# 📖 Descripción

En la lección anterior aprendimos a conectar una aplicación Flask con una base de datos MySQL utilizando **PyMySQL** y **Programación Orientada a Objetos**.

Ahora daremos el siguiente paso:

> **Recuperar información almacenada en MySQL y mostrarla en una página web.**

La aplicación administrará mascotas almacenadas en una tabla llamada:

```text
mascotas
```

Cuando el usuario visite:

```text
http://127.0.0.1:5000/
```

Flask consultará la base de datos, obtendrá las mascotas registradas y enviará esos datos a una plantilla HTML para mostrarlos mediante Jinja2.

El flujo será:

```text
MySQL
   ↓
SELECT
   ↓
PyMySQL
   ↓
lista de diccionarios
   ↓
objetos Mascota
   ↓
Flask
   ↓
render_template()
   ↓
Jinja2
   ↓
HTML
   ↓
Navegador
```

---

# 🎯 Objetivos

Al finalizar esta lección deberás comprender cómo:

- Recuperar registros desde MySQL mediante `SELECT`.
- Utilizar un modelo Python para consultar datos.
- Utilizar `Mascota.get_all()`.
- Recibir una lista de objetos `Mascota`.
- Enviar esa lista desde Flask hacia Jinja2.
- Recorrer objetos utilizando un bucle `for`.
- Mostrar atributos de objetos en HTML.
- Construir una vista dinámica a partir de los datos de una base de datos.

---

# 📁 Estructura del proyecto

La estructura utilizada será:

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
    └── index.html
```

---

# 🗄️ Base de datos

La aplicación utilizará una base de datos llamada:

```text
primera_flask
```

Dentro de ella tendremos una tabla:

```text
mascotas
```

con los siguientes campos:

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | INT | Identificador único |
| `nombre` | VARCHAR(100) | Nombre de la mascota |
| `tipo` | VARCHAR(100) | Tipo de animal |
| `color` | VARCHAR(100) | Color |
| `created_at` | DATETIME | Fecha de creación |
| `updated_at` | DATETIME | Fecha de actualización |

---

# 🧾 `schema.sql`

Utiliza el siguiente script para crear la base de datos, la tabla y algunos registros de prueba.

```sql
-- ==========================================================
-- CREAR BASE DE DATOS
-- ==========================================================

CREATE DATABASE IF NOT EXISTS primera_flask;

USE primera_flask;


-- ==========================================================
-- CREAR TABLA MASCOTAS
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
-- INSERTAR DATOS DE PRUEBA
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

# 🔍 ¿Qué hace `SELECT`?

La consulta que utilizaremos para recuperar las mascotas es:

```sql
SELECT *
FROM mascotas;
```

Se puede interpretar como:

> "Selecciona todas las columnas de todos los registros de la tabla `mascotas`."

MySQL podría entregar:

```text
1 | Firulais | Perro   | Café
2 | Michi    | Gato    | Negro
3 | Luna     | Perro   | Blanco
4 | Nala     | Gato    | Naranjo
5 | Coco     | Conejo | Blanco
```

Gracias a `DictCursor`, Python recibirá esos datos como una lista de diccionarios:

```python
[
    {
        "id": 1,
        "nombre": "Firulais",
        "tipo": "Perro",
        "color": "Café"
    },
    {
        "id": 2,
        "nombre": "Michi",
        "tipo": "Gato",
        "color": "Negro"
    }
]
```

---

# 🔌 `mysqlconnection.py`

Este archivo será responsable de comunicarse con MySQL.

```python
# ==========================================================
# MYSQL CONNECTION
# ==========================================================

import pymysql.cursors


# ==========================================================
# CLASE DE CONEXIÓN
# ==========================================================

class MySQLConnection:
    """
    Administra una conexión con una base de datos MySQL.
    """

    def __init__(self, db):
        """
        Recibe el nombre de la base de datos y establece
        la conexión con el servidor MySQL.
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

        Para SELECT:
            devuelve una lista de diccionarios.

        Para INSERT:
            devuelve el ID generado.

        Para UPDATE / DELETE:
            devuelve None.

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
    Recibe el nombre de una base de datos y devuelve
    una instancia de MySQLConnection.
    """

    return MySQLConnection(db)
```

---

# 🔐 Configuración de MySQL

Dentro de:

```python
mysqlconnection.py
```

debes configurar tus credenciales:

```python
host="localhost"
user="root"
password="root"
database=db
```

Por ejemplo:

```python
password="MiPassword123"
```

Debes utilizar las credenciales reales de tu instalación local de MySQL.

> No publiques credenciales reales en un repositorio público.

---

# 🐕 `mascota.py`

Este archivo representa la tabla `mascotas` utilizando una clase de Python.

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
        y lo transforma en atributos del objeto.
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
        Consulta todas las mascotas almacenadas
        en la base de datos.

        Retorna una lista de objetos Mascota.
        """

        # --------------------------------------------------
        # CONSULTA SQL
        # --------------------------------------------------

        query = """
            SELECT *
            FROM mascotas;
        """


        # --------------------------------------------------
        # EJECUTAR CONSULTA
        # --------------------------------------------------

        resultados = connectToMySQL(
            "primera_flask"
        ).query_db(query)


        # --------------------------------------------------
        # CREAR LISTA DE OBJETOS
        # --------------------------------------------------

        mascotas = []


        # --------------------------------------------------
        # CONVERTIR RESULTADOS EN OBJETOS
        # --------------------------------------------------

        for mascota in resultados:

            mascotas.append(
                cls(mascota)
            )


        # --------------------------------------------------
        # RETORNAR RESULTADOS
        # --------------------------------------------------

        return mascotas
```

---

# 🔍 ¿Qué ocurre en `get_all()`?

La función ejecuta:

```sql
SELECT *
FROM mascotas;
```

MySQL devuelve:

```python
[
    {...},
    {...},
    {...}
]
```

Posteriormente:

```python
for mascota in resultados:
```

recorre cada diccionario.

Y:

```python
cls(mascota)
```

convierte el diccionario en una instancia de:

```python
Mascota
```

Por lo tanto, el resultado final será:

```python
[
    Mascota(...),
    Mascota(...),
    Mascota(...)
]
```

---

# 🌐 `app.py`

Ahora conectaremos la consulta con Flask.

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
    Consulta todas las mascotas y las envía
    hacia la plantilla index.html.
    """

    # ------------------------------------------------------
    # OBTENER MASCOTAS DESDE MYSQL
    # ------------------------------------------------------

    mascotas = Mascota.get_all()


    # ------------------------------------------------------
    # MOSTRAR RESULTADOS EN TERMINAL
    # ------------------------------------------------------

    print(mascotas)


    # ------------------------------------------------------
    # ENVIAR DATOS A JINJA2
    # ------------------------------------------------------

    return render_template(

        "index.html",

        todas_mascotas=mascotas

    )


# ==========================================================
# EJECUTAR SERVIDOR
# ==========================================================

if __name__ == "__main__":

    app.run(debug=True)
```

---

# 🔍 Análisis de `app.py`

La línea más importante es:

```python
mascotas = Mascota.get_all()
```

Aquí Flask solicita al modelo:

> "Entrégame todas las mascotas almacenadas en MySQL."

El modelo se encarga de:

```text
Mascota
   ↓
get_all()
   ↓
SELECT *
FROM mascotas
   ↓
MySQL
   ↓
resultados
   ↓
objetos Mascota
```

---

# 📤 Enviar los datos a Jinja2

Después:

```python
return render_template(
    "index.html",
    todas_mascotas=mascotas
)
```

estamos enviando la variable:

```text
todas_mascotas
```

hacia:

```text
index.html
```

Esto significa que dentro de Jinja2 podremos utilizar:

```jinja
todas_mascotas
```

---

# 🖥️ `templates/index.html`

Ahora construiremos la página que mostrará la información.

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

    <h1>Las mascotas</h1>


    <!-- ==================================================
         COMPROBAR SI EXISTEN MASCOTAS
    =================================================== -->

    {% if todas_mascotas %}


        <!-- ==================================================
             RECORRER MASCOTAS
        =================================================== -->

        {% for una_mascota in todas_mascotas %}

            <div>

                <p>

                    <b>Nombre:</b>
                    {{ una_mascota.nombre }}

                    <br>

                    <b>Tipo:</b>
                    {{ una_mascota.tipo }}

                    <br>

                    <b>Color:</b>
                    {{ una_mascota.color }}

                </p>

            </div>

        {% endfor %}


    {% else %}


        <!-- ==================================================
             SIN REGISTROS
        =================================================== -->

        <p>

            No existen mascotas registradas.

        </p>


    {% endif %}

</body>

</html>
```

---

# 🔍 Análisis de `index.html`

## `todas_mascotas`

Flask envía:

```python
todas_mascotas=mascotas
```

Por lo tanto Jinja2 recibe una colección.

Conceptualmente:

```text
todas_mascotas
│
├── Mascota
├── Mascota
├── Mascota
├── Mascota
└── Mascota
```

---

# 🔄 Bucle `for`

Utilizamos:

```jinja
{% for una_mascota in todas_mascotas %}
```

Esto significa:

> "Recorre todos los objetos que existen dentro de `todas_mascotas` y guarda temporalmente cada uno en `una_mascota`."

Por ejemplo:

```text
primera vuelta
una_mascota → Firulais

segunda vuelta
una_mascota → Michi

tercera vuelta
una_mascota → Luna
```

---

# 🐶 Acceder a los atributos

Como `una_mascota` es un objeto:

```jinja
{{ una_mascota.nombre }}
```

obtiene:

```python
una_mascota.nombre
```

Lo mismo para:

```jinja
{{ una_mascota.tipo }}
```

y:

```jinja
{{ una_mascota.color }}
```

---

# 🧩 Diccionario → Objeto → Jinja2

Este es uno de los conceptos más importantes de la lección.

MySQL inicialmente entrega:

```python
{
    "nombre": "Firulais",
    "tipo": "Perro",
    "color": "Café"
}
```

La clase lo transforma:

```python
Mascota(data)
```

y obtenemos:

```python
mascota.nombre
mascota.tipo
mascota.color
```

Finalmente Jinja2 muestra:

```jinja
{{ una_mascota.nombre }}
```

El recorrido completo es:

```text
MySQL
  ↓
Diccionario
  ↓
Mascota(data)
  ↓
Objeto Python
  ↓
Flask
  ↓
Jinja2
  ↓
HTML
```

---

# 🔎 El condicional `{% if %}`

Utilizamos:

```jinja
{% if todas_mascotas %}
```

para comprobar si la colección contiene información.

Si existen mascotas:

```text
→ ejecutamos el for
```

Si no existen:

```text
→ mostramos "No existen mascotas registradas."
```

Esto evita presentar una página vacía cuando la tabla no tiene registros.

---

# 📊 Resultado esperado

Si la base de datos contiene:

```text
Firulais | Perro   | Café
Michi    | Gato    | Negro
Luna     | Perro   | Blanco
Nala     | Gato    | Naranjo
Coco     | Conejo  | Blanco
```

la página mostrará:

```text
Las mascotas

Nombre: Firulais
Tipo: Perro
Color: Café


Nombre: Michi
Tipo: Gato
Color: Negro


Nombre: Luna
Tipo: Perro
Color: Blanco


Nombre: Nala
Tipo: Gato
Color: Naranjo


Nombre: Coco
Tipo: Conejo
Color: Blanco
```

---

# 🌐 Ruta disponible

La aplicación tendrá:

```text
GET /
```

URL:

```text
http://127.0.0.1:5000/
```

La ruta:

```python
@app.route("/")
```

ejecutará:

```python
Mascota.get_all()
```

y mostrará los resultados.

---

# 🧠 Flujo completo de la aplicación

Cuando el usuario visita `/`:

```text
1. Navegador
       ↓
2. GET /
       ↓
3. Flask
       ↓
4. Mascota.get_all()
       ↓
5. SELECT * FROM mascotas
       ↓
6. MySQL
       ↓
7. Lista de diccionarios
       ↓
8. Objetos Mascota
       ↓
9. render_template()
       ↓
10. Jinja2
       ↓
11. HTML
       ↓
12. Navegador
```

---

# 🧪 Verificación

Con MySQL ejecutándose y la base de datos creada, inicia Flask:

```bash
python app.py
```

Luego abre:

```text
http://127.0.0.1:5000/
```

También podrás observar en la terminal que se consultaron las mascotas.

---

# 📌 ¿Qué sucede si agregamos otra mascota?

Ejecuta en MySQL:

```sql
USE primera_flask;

INSERT INTO mascotas
    (nombre, tipo, color)
VALUES
    ("Rocky", "Perro", "Negro");
```

No necesitamos modificar:

```text
app.py
```

ni:

```text
index.html
```

Cuando actualicemos la página:

```text
GET /
```

Flask volverá a ejecutar:

```python
Mascota.get_all()
```

y la nueva mascota aparecerá automáticamente.

Esto demuestra una de las principales ventajas de utilizar una base de datos.

---

# 🔄 Antes y después

### Antes

La información estaba escrita directamente en Python:

```python
mascotas = [
    {
        "nombre": "Firulais"
    }
]
```

### Ahora

La información vive en MySQL:

```text
MySQL
 ↓
mascotas
 ↓
SELECT
 ↓
Flask
```

Esto significa que podemos agregar o modificar datos **sin cambiar el código de la aplicación**.

---

# 📚 Conceptos aprendidos

| Concepto | Aplicación |
|---|---|
| `SELECT` | Recuperar información |
| `fetchall()` | Obtener múltiples registros |
| `DictCursor` | Convertir registros en diccionarios |
| `get_all()` | Consultar todos los registros |
| `@classmethod` | Ejecutar consulta desde la clase |
| POO | Representar registros como objetos |
| `render_template()` | Enviar datos a HTML |
| Jinja2 `for` | Recorrer mascotas |
| Jinja2 `if` | Comprobar si existen registros |
| Atributos | Mostrar datos del objeto |
| Flask | Coordinar el proceso |

---

# 📝 Actividad de consolidación

Modifica la plantilla para mostrar también:

```text
ID
Fecha de creación
Fecha de actualización
```

Por ejemplo:

```text
ID: 1
Nombre: Firulais
Tipo: Perro
Color: Café
Creado: 2026-09-07
Actualizado: 2026-09-07
```

Los datos ya están disponibles en el objeto:

```python
una_mascota.id
una_mascota.created_at
una_mascota.updated_at
```

Por lo tanto, no necesitas modificar la consulta SQL.

---

# 🚀 Desafío

Crea una ruta:

```text
/mascotas/perros
```

que muestre únicamente las mascotas cuyo tipo sea:

```text
Perro
```

La idea será comenzar a utilizar una consulta SQL más específica:

```sql
SELECT *
FROM mascotas
WHERE tipo = %(tipo)s;
```

y enviar el resultado a una plantilla.

El objetivo es comenzar a comprender que **el modelo no solamente puede recuperar todos los registros, sino también realizar consultas específicas utilizando criterios**.

---

# 🏁 Conclusión

En esta lección completamos el primer flujo real de lectura de información desde una base de datos.

Ahora nuestra aplicación puede:

```text
                 MYSQL
                   │
                   ▼
              tabla mascotas
                   │
                   ▼
                 SELECT
                   │
                   ▼
              PyMySQL
                   │
                   ▼
          lista de diccionarios
                   │
                   ▼
            clase Mascota
                   │
                   ▼
             objetos Python
                   │
                   ▼
                 Flask
                   │
                   ▼
             render_template()
                   │
                   ▼
                Jinja2
                   │
                   ▼
             página HTML
```

La idea fundamental es:

> **MySQL almacena los datos, el modelo los recupera y transforma, Flask los envía y Jinja2 los presenta.**

Este flujo será la base de las siguientes operaciones de una aplicación CRUD, donde además de **leer (`SELECT`)**, aprenderemos a **crear (`INSERT`)**, **actualizar (`UPDATE`)** y **eliminar (`DELETE`)** registros.
Mostrando README.md