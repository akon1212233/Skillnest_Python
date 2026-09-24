# 🐬 Conectando Flask con MySQL utilizando POO

> **Curso:** Desarrollo Web con Flask desde Cero  
> **Unidad:** Integración con Bases de Datos  
> **Tema:** Conexión Flask → MySQL utilizando PyMySQL y Programación Orientada a Objetos

---

# 📖 Descripción

Hasta este momento hemos trabajado con información almacenada directamente en Python.

Por ejemplo:

```python
mascotas = [
    {"nombre": "Firulais", "tipo": "Perro"},
    {"nombre": "Michi", "tipo": "Gato"}
]
```

Esto resulta útil para aprender los fundamentos de Flask, pero una aplicación real necesita almacenar información de manera persistente.

Si el servidor se reinicia, una lista creada directamente en Python mantiene únicamente los datos que estén escritos en el código.

Una base de datos permite solucionar este problema.

En esta lección conectaremos una aplicación Flask con **MySQL**, utilizando:

- **MySQL Workbench** para administrar la base de datos.
- **PyMySQL** para comunicarnos con MySQL desde Python.
- **POO** para representar los registros de la base de datos como objetos.
- **Flask** para ejecutar las consultas desde nuestras rutas.
- **Jinja2** para mostrar los resultados en HTML.

La arquitectura que construiremos será:

```text
Navegador
    │
    ▼
  Flask
    │
    ▼
  Modelo
  Mascota
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

# 🎯 Objetivos

Al finalizar esta lección deberás comprender cómo:

- Crear una base de datos en MySQL.
- Crear una tabla y sus campos.
- Insertar registros de prueba.
- Conectar Python con MySQL mediante PyMySQL.
- Crear una clase encargada de administrar la conexión.
- Ejecutar consultas SQL desde Python.
- Obtener resultados de un `SELECT`.
- Trabajar con `DictCursor`.
- Crear un modelo utilizando POO.
- Convertir registros de MySQL en objetos Python.
- Utilizar `@classmethod`.
- Consultar el modelo desde Flask.
- Enviar los resultados hacia Jinja2.

---

# 🧠 Concepto principal

La idea es separar las responsabilidades de nuestra aplicación.

```text
app.py
│
│   Controla las rutas
│
▼
mascota.py
│
│   Representa los datos
│
▼
mysqlconnection.py
│
│   Administra la conexión
│
▼
MySQL
│
│   Almacena la información
│
▼
tabla mascotas
```

Cada archivo tiene una responsabilidad específica.

Esto evita colocar toda la lógica en un solo archivo.

---

# 📁 Estructura del proyecto

La estructura final será:

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

# 📦 Dependencias

El proyecto utilizará:

```text
Flask
PyMySQL
```

## `requirements.txt`

```text
Flask
PyMySQL
```

---

# 🚫 `.gitignore`

Es recomendable utilizar un archivo `.gitignore` para evitar subir archivos que no deberían formar parte del repositorio.

## `.gitignore`

```text
venv/
__pycache__/
*.pyc
.env
```

> Más adelante, cuando trabajemos con variables de entorno, también evitaremos publicar credenciales de MySQL.

---

# 🗄️ Base de datos

La base de datos se llamará:

```text
primera_flask
```

Dentro de ella crearemos la tabla:

```text
mascotas
```

La tabla tendrá los siguientes campos:

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | `INT` | Identificador único |
| `nombre` | `VARCHAR(100)` | Nombre de la mascota |
| `tipo` | `VARCHAR(100)` | Tipo de animal |
| `color` | `VARCHAR(100)` | Color |
| `created_at` | `DATETIME` | Fecha de creación |
| `updated_at` | `DATETIME` | Fecha de actualización |

---

# 🧾 `schema.sql`

El siguiente archivo permite crear la base de datos y agregar algunos registros iniciales.

```sql
-- ==========================================================
-- CREAR BASE DE DATOS
-- ==========================================================

CREATE DATABASE IF NOT EXISTS primera_flask;

USE primera_flask;


-- ==========================================================
-- CREAR TABLA
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

# 🧠 ¿Qué hace `AUTO_INCREMENT`?

La definición:

```sql
id INT AUTO_INCREMENT PRIMARY KEY
```

permite que MySQL genere automáticamente el identificador.

Por ejemplo:

```text
id | nombre
---|---------
1  | Firulais
2  | Michi
3  | Luna
4  | Nala
```

No necesitamos crear manualmente esos números.

---

# 🔌 `mysqlconnection.py`

Este archivo será responsable de comunicarse con MySQL.

Su objetivo es evitar que tengamos que repetir la lógica de conexión en cada modelo.

## Código completo

```python
# ==========================================================
# MYSQL CONNECTION
# ==========================================================
#
# Esta clase centraliza la conexión entre Python y MySQL.
#
# La idea es que nuestros modelos no tengan que encargarse
# directamente de crear una conexión cada vez que necesitan
# ejecutar una consulta.
#
# ==========================================================


import pymysql.cursors


# ==========================================================
# CLASE MYSQL CONNECTION
# ==========================================================

class MySQLConnection:
    """
    Administra la conexión con una base de datos MySQL.
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
            Retorna una lista de diccionarios.

        INSERT:
            Retorna el ID generado.

        UPDATE / DELETE:
            No retornan registros.

        Error:
            Retorna False.
        """

        with self.connection.cursor() as cursor:

            try:

                # --------------------------------------------------
                # Mostrar la consulta durante el desarrollo.
                # --------------------------------------------------

                print("Running Query:")

                print(query)


                # --------------------------------------------------
                # Ejecutar consulta.
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
    Recibe el nombre de una base de datos y devuelve
    una instancia de MySQLConnection.
    """

    return MySQLConnection(db)
```

---

# 🔍 ¿Qué estamos encapsulando?

La clase:

```python
class MySQLConnection:
```

encapsula la lógica necesaria para:

1. Conectarse a MySQL.
2. Crear un cursor.
3. Ejecutar una consulta.
4. Recuperar resultados.
5. Cerrar la conexión.

De esta manera, el resto de la aplicación puede trabajar con:

```python
connectToMySQL(...)
```

sin preocuparse por todos los detalles internos.

---

# 🧾 `DictCursor`

Esta configuración es especialmente importante:

```python
cursorclass=pymysql.cursors.DictCursor
```

Gracias a ella, una consulta como:

```sql
SELECT * FROM mascotas;
```

entregará los resultados con una estructura similar a:

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

Es decir:

```text
LISTA
  │
  ├── DICCIONARIO
  ├── DICCIONARIO
  └── DICCIONARIO
```

Esto se relaciona directamente con las estructuras que ya hemos utilizado en Jinja2.

---

# 📊 Resultado de las consultas

Nuestra clase trabaja con el siguiente comportamiento:

| Consulta | Resultado |
|---|---|
| `SELECT` | Lista de diccionarios |
| `INSERT` | ID generado |
| `UPDATE` | `None` |
| `DELETE` | `None` |
| Error | `False` |

---

# 🐕 `mascota.py`

Ahora crearemos una clase que represente los registros de la tabla:

```text
mascotas
```

Cada registro de la base de datos se convertirá en un objeto:

```python
Mascota
```

---

# 📄 Código completo de `mascota.py`

```python
# ==========================================================
# MODELO MASCOTA
# ==========================================================
#
# Este archivo representa la tabla "mascotas"
# mediante una clase de Python.
#
# ==========================================================


# Importamos la función encargada de crear
# una conexión con MySQL.

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
        y transforma sus datos en atributos del objeto.
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
        # Consulta SQL
        # --------------------------------------------------

        query = """
            SELECT *
            FROM mascotas;
        """


        # --------------------------------------------------
        # Ejecutar consulta
        # --------------------------------------------------

        resultados = connectToMySQL(
            "primera_flask"
        ).query_db(query)


        # --------------------------------------------------
        # Crear lista de objetos
        # --------------------------------------------------

        mascotas = []


        # --------------------------------------------------
        # Convertir cada diccionario en Mascota
        # --------------------------------------------------

        for mascota in resultados:

            mascotas.append(
                cls(mascota)
            )


        # --------------------------------------------------
        # Retornar resultado
        # --------------------------------------------------

        return mascotas
```

---

# 🧠 ¿Qué hace el constructor?

La base de datos entrega algo como:

```python
{
    "id": 1,
    "nombre": "Firulais",
    "tipo": "Perro",
    "color": "Café",
    "created_at": "...",
    "updated_at": "..."
}
```

El constructor recibe ese diccionario:

```python
def __init__(self, data):
```

y crea:

```python
self.id
self.nombre
self.tipo
self.color
```

Por lo tanto, pasamos de:

```text
Diccionario
```

a:

```text
Objeto Mascota
```

---

# 🔄 Transformación de datos

El proceso puede visualizarse así:

```text
MYSQL
  │
  ▼
REGISTRO
  │
  ▼
DICCIONARIO
  │
  ▼
Mascota(data)
  │
  ▼
OBJETO MASCOTA
```

---

# 🏷️ ¿Por qué utilizamos `@classmethod`?

Observa:

```python
@classmethod
def get_all(cls):
```

`get_all()` no necesita que exista una mascota específica para ejecutarse.

No tendría sentido hacer:

```python
mascota = Mascota(...)
```

solo para preguntar:

```python
mascota.get_all()
```

La operación pertenece a la **clase**, porque consulta la colección completa.

Por eso posteriormente podremos hacer:

```python
Mascota.get_all()
```

---

# 🌐 `app.py`

Ahora Flask utilizará nuestro modelo.

## Código completo

```python
# ==========================================================
# SERVIDOR FLASK + MYSQL
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
    Consulta todas las mascotas de la base de datos
    y las envía hacia la plantilla HTML.
    """

    # ------------------------------------------------------
    # Consultar base de datos mediante el modelo.
    # ------------------------------------------------------

    mascotas = Mascota.get_all()


    # ------------------------------------------------------
    # Mostrar resultados en la terminal.
    # ------------------------------------------------------

    print(mascotas)


    # ------------------------------------------------------
    # Enviar resultados a Jinja2.
    # ------------------------------------------------------

    return render_template(
        "index.html",
        mascotas=mascotas
    )


# ==========================================================
# EJECUTAR SERVIDOR
# ==========================================================

if __name__ == "__main__":

    app.run(debug=True)
```

---

# 📄 `templates/index.html`

Ahora podemos utilizar los objetos `Mascota` enviados por Flask.

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

# 🔍 ¿Qué ocurre en esta plantilla?

Flask envía:

```python
mascotas=mascotas
```

Jinja2 recibe:

```text
mascotas
```

Luego:

```jinja
{% for mascota in mascotas %}
```

recorre todos los objetos.

Finalmente:

```jinja
{{ mascota.nombre }}
```

muestra el atributo:

```python
mascota.nombre
```

---

# 🔗 Flujo completo

Cuando el usuario visita:

```text
http://127.0.0.1:5000/
```

ocurre:

```text
┌──────────────────────┐
│      NAVEGADOR       │
└──────────┬───────────┘
           │
           │ GET /
           ▼
┌──────────────────────┐
│        FLASK         │
│       app.py         │
└──────────┬───────────┘
           │
           │ Mascota.get_all()
           ▼
┌──────────────────────┐
│      mascota.py      │
│   Clase Mascota      │
└──────────┬───────────┘
           │
           │ connectToMySQL()
           ▼
┌──────────────────────┐
│ mysqlconnection.py   │
│ MySQLConnection      │
└──────────┬───────────┘
           │
           │ SQL
           ▼
┌──────────────────────┐
│        MYSQL         │
│     mascotas         │
└──────────┬───────────┘
           │
           │ resultados
           ▼
┌──────────────────────┐
│ Lista de diccionarios│
└──────────┬───────────┘
           │
           │ cls(mascota)
           ▼
┌──────────────────────┐
│ Lista de objetos     │
│ Mascota              │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   render_template()  │
│     index.html       │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│       Jinja2         │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│       HTML final     │
└──────────────────────┘
```

---

# 🧠 Comprendiendo cada capa

## 1. Flask

```python
@app.route("/")
```

recibe la solicitud del navegador.

---

## 2. Modelo

```python
Mascota.get_all()
```

indica:

> "Necesito todas las mascotas."

---

## 3. Conexión

```python
connectToMySQL("primera_flask")
```

establece la conexión con la base de datos.

---

## 4. SQL

Se ejecuta:

```sql
SELECT *
FROM mascotas;
```

---

## 5. MySQL

Devuelve los registros.

```python
[
    {...},
    {...},
    {...}
]
```

---

## 6. POO

Cada registro se convierte en:

```python
Mascota(...)
```

---

## 7. Jinja2

Finalmente:

```jinja
{% for mascota in mascotas %}
```

recorre los objetos y muestra:

```jinja
{{ mascota.nombre }}
```

```jinja
{{ mascota.tipo }}
```

```jinja
{{ mascota.color }}
```

---

# 🧪 Comprobación

Si la base de datos contiene:

```text
Firulais   | Perro   | Café
Michi      | Gato    | Negro
Luna       | Perro   | Blanco
Nala       | Gato    | Naranjo
Coco       | Conejo  | Blanco
```

la aplicación deberá mostrar:

```text
Listado de Mascotas

• Firulais - Perro - Café
• Michi - Gato - Negro
• Luna - Perro - Blanco
• Nala - Gato - Naranjo
• Coco - Conejo - Blanco
```

En la terminal también podremos encontrar los objetos recuperados:

```text
[
    <mascota.Mascota object at ...>,
    <mascota.Mascota object at ...>,
    ...
]
```

Esto ocurre porque ahora ya no estamos trabajando directamente con diccionarios, sino con **objetos de la clase `Mascota`**.

---

# ⚠️ Configuración de MySQL

En:

```text
mysqlconnection.py
```

encontrarás:

```python
host="localhost"

user="root"

password="root"

database=db
```

Debes cambiar:

```python
password="root"
```

por la contraseña correspondiente a tu instalación de MySQL.

Por ejemplo:

```python
password="MiClave123"
```

---

# 🔐 Importante sobre las credenciales

Nunca deberíamos publicar credenciales reales en un repositorio público.

Para esta primera aproximación utilizamos:

```python
password="root"
```

con fines educativos.

Posteriormente reemplazaremos esto por **variables de entorno**, por ejemplo:

```text
MYSQL_HOST
MYSQL_USER
MYSQL_PASSWORD
MYSQL_DATABASE
```

Esto permitirá mantener las credenciales fuera del código fuente.

---

# 🧩 ¿Por qué no hacemos la conexión directamente desde `app.py`?

Podríamos escribir todo en un único archivo:

```python
@app.route("/")
def index():

    # conexión

    # cursor

    # SQL

    # resultados

    # objetos

    # render_template
```

Pero entonces `app.py` tendría demasiadas responsabilidades.

Nuestra separación permite:

```text
app.py
    ↓
Rutas

mascota.py
    ↓
Modelo

mysqlconnection.py
    ↓
Conexión

MySQL
    ↓
Datos
```

Esta separación será cada vez más importante cuando nuestras aplicaciones crezcan.

---

# 📊 Resultado de cada tipo de operación

La clase `MySQLConnection` está pensada para ser reutilizable.

## SELECT

```sql
SELECT * FROM mascotas;
```

Resultado:

```python
[
    {
        "id": 1,
        "nombre": "Firulais"
    }
]
```

---

## INSERT

```sql
INSERT INTO mascotas (...);
```

Resultado:

```python
cursor.lastrowid
```

Por ejemplo:

```text
6
```

Es el ID generado por MySQL.

---

## UPDATE

```sql
UPDATE mascotas
SET color = "Negro"
WHERE id = 1;
```

No necesitamos una lista de resultados.

---

## DELETE

```sql
DELETE FROM mascotas
WHERE id = 1;
```

Tampoco necesitamos una lista de resultados.

---

# 🚀 Ideas clave que debes recordar

## `MySQLConnection`

Se encarga de:

```text
Conectar
Consultar
Obtener resultados
Cerrar conexión
```

---

## `Mascota`

Se encarga de:

```text
Representar la tabla mascotas
Consultar datos relacionados con mascotas
Convertir registros en objetos
```

---

## `app.py`

Se encarga de:

```text
Recibir solicitudes
Invocar modelos
Enviar información a las plantillas
```

---

## `index.html`

Se encarga de:

```text
Mostrar la información al usuario
```

---

# 📝 Ejercicio de consolidación

Crea un segundo modelo llamado:

```text
Usuario
```

y una tabla llamada:

```text
usuarios
```

con los siguientes campos:

```text
id
nombre
email
edad
created_at
updated_at
```

El modelo deberá tener:

```python
class Usuario:
```

y un método:

```python
@classmethod
def get_all(cls):
```

que consulte todos los usuarios.

Posteriormente muestra los resultados en:

```text
templates/usuarios.html
```

---

# 🚀 Desafío

Agrega al modelo `Mascota` un método:

```python
@classmethod
def get_by_id(cls, id):
```

El método deberá buscar una mascota específica mediante:

```sql
SELECT *
FROM mascotas
WHERE id = %(id)s;
```

y recibir el identificador mediante un diccionario:

```python
{
    "id": id
}
```

La llamada debería verse así:

```python
Mascota.get_by_id(3)
```

y devolver una instancia de:

```python
Mascota
```

---

# 🏁 Conclusión

En esta lección dejamos atrás las aplicaciones que dependen exclusivamente de datos escritos dentro de Python y comenzamos a trabajar con **persistencia de datos mediante MySQL**.

La arquitectura obtenida es:

```text
NAVEGADOR
    ↓
FLASK
    ↓
MODELO
    ↓
MYSQL CONNECTION
    ↓
PYMYSQL
    ↓
MYSQL
    ↓
DATOS
    ↓
OBJETOS PYTHON
    ↓
JINJA2
    ↓
HTML
    ↓
NAVEGADOR
```

Lo más importante no es memorizar cada línea, sino comprender **qué responsabilidad tiene cada componente**.

La aplicación ahora tiene una separación clara:

```text
app.py
→ controla las rutas

mascota.py
→ representa y consulta mascotas

mysqlconnection.py
→ administra la conexión con MySQL

schema.sql
→ define la estructura de la base de datos

index.html
→ presenta la información
```

Esta estructura será la base para comenzar a construir aplicaciones Flask conectadas a bases de datos reales y, posteriormente, implementar operaciones completas de **CRUD: crear, consultar, actualizar y eliminar información**.
Mostrando README.md 