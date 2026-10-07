# 🔐 Práctica: Registro e inicio de sesión seguro con Flask

> **Flask + Bcrypt + MySQL + `.env` + Bootstrap + MVC**
>
> Proyecto práctico para implementar un sistema de **registro, autenticación y control de acceso**, aplicando buenas prácticas de seguridad y arquitectura modular.

## 🧰 Tecnologías utilizadas

| Tecnología | Uso |
|---|---|
| **Python** | Lenguaje principal |
| **Flask** | Framework web |
| **MySQL** | Base de datos relacional |
| **PyMySQL** | Conexión Python ↔ MySQL |
| **Bcrypt** | Hash seguro de contraseñas |
| **python-dotenv** | Gestión de variables de entorno |
| **Bootstrap** | Interfaz visual |
| **Jinja2** | Plantillas HTML |
| **MVC** | Organización modular del proyecto |

---

## 📚 Contenidos

- [1. Objetivo](#1-objetivo)
- [2. ¿Qué vamos a construir?](#2-qué-vamos-a-construir)
- [3. Conceptos fundamentales](#3-conceptos-fundamentales)
- [4. Hashing vs. cifrado](#4-hashing-vs-cifrado)
- [5. ¿Qué es Bcrypt?](#5-qué-es-bcrypt)
- [6. ¿Qué ocurre con el salt?](#6-qué-ocurre-con-el-salt)
- [7. Arquitectura del proyecto](#7-arquitectura-del-proyecto)
- [8. Base de datos](#8-base-de-datos)
- [9. Modelo de datos](#9-modelo-de-datos)
- [10. SQL completo](#10-sql-completo)
- [11. ¿Por qué cumple 3FN?](#11-por-qué-cumple-3fn)
- [12. Instalación del proyecto](#12-instalación-del-proyecto)
- [13. Archivo `.env`](#13-archivo-env)
- [14. `.env.example`](#14-envexample)
- [15. `.gitignore`](#15-gitignore)
- [16–49. Implementación, pruebas y arquitectura](#16-flask_appinitpy)
- [50. Preguntas de comprensión](#50-preguntas-de-comprensión)
- [51. Concepto final](#51-concepto-final)

---

## 1. Objetivo

Construir una aplicación Flask modularizada que permita **registrar usuarios e iniciar sesión de forma segura**, integrando los contenidos trabajados anteriormente.

En esta actividad se integran:

-  Validación de formularios. 
-  Expresiones regulares (`regex`). 
-  Mensajes `flash`. 
-  Conexión Flask + MySQL. 
-  Arquitectura modular/MVC. 
-  Sesiones. 
-  Hashing de contraseñas. 
-  Bcrypt. 
-  Variables de entorno mediante `.env`. 
-  Bootstrap. 
-  Base de datos normalizada en **3FN**. 
-  Rutas protegidas. 
-  Registro, login y logout. 

> [!IMPORTANT]
> **Regla fundamental:** una contraseña nunca debe almacenarse en texto plano en la base de datos.

---

## 2. ¿Qué vamos a construir?

La aplicación tendrá:

1.  Registro de usuario. 
2.  Validación de nombre y apellido. 
3.  Validación de email. 
4.  Validación de contraseña. 
5.  Validación de email único. 
6.  Hash de contraseña mediante Bcrypt. 
7.  Inicio de sesión. 
8.  Comparación de contraseña mediante Bcrypt. 
9.  Creación de sesión. 
10.  Dashboard protegido. 
11.  Cierre de sesión. 
12.  Configuración mediante `.env`. 
13.  Interfaz utilizando Bootstrap. 

### Flujo de registro

```
Formulario
    ↓
Validación
    ↓
¿Datos correctos?
    ↓ Sí
¿Email disponible?
    ↓ Sí
Generar hash Bcrypt
    ↓
Guardar usuario
    ↓
Crear sesión
    ↓
Dashboard
```

### Flujo de login

```
Formulario
    ↓
Buscar usuario por email
    ↓
¿Usuario existe?
   /       \
 NO         SÍ
 ↓           ↓
Flash       Bcrypt
              ↓
       ¿Contraseña correcta?
          /          \
        NO            SÍ
        ↓              ↓
      Flash          Session
                       ↓
                   Dashboard
```

---

# 3. Conceptos fundamentales

## 3.1 ¿Por qué no guardar la contraseña?

Incorrecto:

```
usuario: dany
password: 123456
```

Si un atacante obtiene acceso a la base de datos, puede leer directamente la contraseña.

Nunca debemos almacenar:

```
"password": "123456"
```

La base de datos debe almacenar algo similar a:

```
$2b$12$xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Ese valor corresponde a un **hash Bcrypt**.

---

# 4. Hashing vs. cifrado

## Hashing

El hashing está diseñado para ser **unidireccional**.

```
contraseña
    ↓
   HASH
    ↓
valor almacenado
```

No debemos diseñar nuestro sistema pensando:

```
hash → contraseña original
```

Para verificar una contraseña, Bcrypt permite comparar la contraseña ingresada con el hash almacenado.

---

## Cifrado

El cifrado funciona de manera diferente:

```
dato original
     ↓
  cifrado
     ↓
dato cifrado
     ↓
desencriptación
     ↓
dato original
```

El cifrado es apropiado cuando posteriormente necesitamos recuperar el dato original.

Para contraseñas, utilizamos **hashing**, no cifrado reversible.

---

# 5. ¿Qué es Bcrypt?

Bcrypt es un algoritmo diseñado específicamente para almacenar contraseñas de forma segura.

En Flask utilizaremos:

```
from flask_bcrypt import Bcrypt
```

Crearemos:

```
bcrypt = Bcrypt(app)
```

Para generar un hash:

```
bcrypt.generate_password_hash(password)
```

Para comprobar una contraseña:

```
bcrypt.check_password_hash(hash_guardado, password_ingresada)
```

---

# 6. ¿Qué ocurre con el salt?

Bcrypt incorpora automáticamente un valor aleatorio denominado **salt** dentro del proceso de hashing.

Por eso dos usuarios que utilicen:

```
123456
```

no necesariamente tendrán el mismo hash almacenado.

Esto dificulta ataques basados en tablas precalculadas.

> **Importante:** no necesitamos crear manualmente una columna `salt` cuando utilizamos Bcrypt correctamente.

---

# 7. Arquitectura del proyecto

Utilizaremos una estructura modular:

```
secure_users/
│
├── flask_app/
│   ├── __init__.py
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   └── mysqlconnection.py
│   │
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── usuarios.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── usuario.py
│   │
│   └── templates/
│       ├── base.html
│       ├── login.html
│       ├── registro.html
│       └── dashboard.html
│
├── server.py
├── Pipfile
├── Pipfile.lock
├── .env
├── .env.example
├── .gitignore
└── README.md
```

## ¿Por qué existen varios `__init__.py`?

Cada carpeta que utilizamos como **paquete Python** puede contener su propio:

```
__init__.py
```

Por ejemplo:

```
flask_app/
├── __init__.py
├── models/
│   ├── __init__.py
│   └── usuario.py
└── controllers/
    ├── __init__.py
    └── usuarios.py
```

No significa que cada carpeta del proyecto necesite obligatoriamente un `__init__.py`.

En este proyecto lo utilizaremos para mantener claramente definidos nuestros paquetes Python.

---

# 8. Base de datos

La base de datos se llamará:

```
esquema_loginreg
```

Tendremos una tabla principal:

```
usuarios
```

---

# 9. Modelo de datos

## Tabla `usuarios`

| Campo      | Tipo         | Restricción        |
| ---------- | ------------ | ------------------ |
| id         | INT          | PK, AUTO_INCREMENT |
| nombre     | VARCHAR(100) | NOT NULL           |
| apellido   | VARCHAR(100) | NOT NULL           |
| email      | VARCHAR(150) | NOT NULL, UNIQUE   |
| password   | VARCHAR(255) | NOT NULL           |
| created_at | DATETIME     | NOT NULL           |
| updated_at | DATETIME     | NOT NULL           |

### ¿Por qué `password` tiene 255 caracteres?

Porque no almacenaremos la contraseña original.

Almacenaremos el hash generado por Bcrypt:

```
$2b$12$...
```

Por eso debemos reservar suficiente espacio.

---

# 10. SQL completo

Crear la base de datos:

```
CREATE DATABASE esquema_loginreg;
USE esquema_loginreg;
```

Crear la tabla:

```
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

Verificar:

```
DESCRIBE usuarios;
```

---

# 11. ¿Por qué cumple 3FN?

La tabla almacena exclusivamente información correspondiente al usuario.

No tenemos grupos repetitivos.

Cada atributo depende directamente de:

```
id
```

Por ejemplo:

```
id → nombre
id → apellido
id → email
id → password
```

Además:

```
email
```

se establece como `UNIQUE`, porque no queremos dos cuentas con el mismo correo.

---

# 12. Instalación del proyecto

Crear carpeta:

```
mkdir secure_users
cd secure_users
```

Inicializar Pipenv:

```
pipenv install flask
```

Instalar MySQL:

```
pipenv install pymysql
```

Instalar Bcrypt:

```
pipenv install flask-bcrypt
```

Instalar dotenv:

```
pipenv install python-dotenv
```

Entrar al entorno:

```
pipenv shell
```

---

# 13. Archivo `.env`

Crear:

```
.env
```

Contenido:

```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=esquema_loginreg
SECRET_KEY=clave-secreta-cambiar-en-produccion
```

> **Nunca subir `.env` a GitHub.**

---

# 14. `.env.example`

Sí debemos subir un ejemplo:

```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=TU_PASSWORD
DB_NAME=esquema_loginreg
SECRET_KEY=TU_CLAVE_SECRETA
```

La diferencia es:

```
.env
```

contiene valores reales.

```
.env.example
```

contiene solamente la estructura necesaria.

---

# 15. `.gitignore`

Crear:

```
.gitignore
```

Contenido:

```
.env
__pycache__/
*.pyc
.Python
.venv/
venv/
```

Esto evita subir información sensible.

---

# 16. `flask_app/__init__.py`

```
from flask import Flask
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")

bcrypt = Bcrypt(app)

from flask_app.controllers import usuarios
```

### ¿Qué hacemos aquí?

Creamos la aplicación:

```
app = Flask(__name__)
```

Cargamos las variables del `.env`:

```
load_dotenv()
```

Configuramos la clave secreta:

```
app.secret_key = os.getenv("SECRET_KEY")
```

Inicializamos Bcrypt:

```
bcrypt = Bcrypt(app)
```

Finalmente cargamos los controladores:

```
from flask_app.controllers import usuarios
```

---

# 17. Configuración MySQL

Archivo:

```
flask_app/config/mysqlconnection.py
```

Código:

```
import pymysql
import pymysql.cursors
import os

class MySQLConnection:
    def __init__(self, db):
        self.connection = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=db,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )

    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(query, data or {})
                if query.strip().lower().startswith("select"):
                    return cursor.fetchall()
                return cursor.lastrowid
            except Exception as e:
                print(f"Error MySQL: {e}")
                return False
            finally:
                self.connection.close()

def connectToMySQL(db):
    return MySQLConnection(db)
```

---

# 18. Modelo Usuario

Archivo:

```
flask_app/models/usuario.py
```

```
import re
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

EMAIL_REGEX = re.compile(
    r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$'
)

class Usuario:
    def __init__(self, data):
        self.id = data["id"]
        self.nombre = data["nombre"]
        self.apellido = data["apellido"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @staticmethod
    def validar_usuario(datos):
        es_valido = True

        if not datos["nombre"].strip():
            flash("El nombre es obligatorio.", "nombre")
            es_valido = False

        elif len(datos["nombre"].strip()) < 2:
            flash("El nombre debe tener al menos 2 caracteres.", "nombre")
            es_valido = False

        if not datos["apellido"].strip():
            flash("El apellido es obligatorio.", "apellido")
            es_valido = False

        elif len(datos["apellido"].strip()) < 2:
            flash("El apellido debe tener al menos 2 caracteres.", "apellido")
            es_valido = False

        if not datos["email"].strip():
            flash("El email es obligatorio.", "email")
            es_valido = False

        elif not EMAIL_REGEX.match(datos["email"].strip()):
            flash("El email no tiene un formato válido.", "email")
            es_valido = False

        if not datos["password"]:
            flash("La contraseña es obligatoria.", "password")
            es_valido = False

        elif len(datos["password"]) < 8:
            flash("La contraseña debe tener al menos 8 caracteres.", "password")
            es_valido = False

        return es_valido

    @classmethod
    def guardar(cls, datos):
        query = """
            INSERT INTO usuarios
            (nombre, apellido, email, password)
            VALUES
            (%(nombre)s, %(apellido)s, %(email)s, %(password)s);
        """
        return connectToMySQL("esquema_loginreg").query_db(query, datos)

    @classmethod
    def buscar_por_email(cls, datos):
        query = """
            SELECT *
            FROM usuarios
            WHERE email = %(email)s;
        """
        resultados = connectToMySQL("esquema_loginreg").query_db(query, datos)

        if len(resultados) == 1:
            return cls(resultados[0])

        return False

    @classmethod
    def existe_email(cls, datos):
        query = """
            SELECT id
            FROM usuarios
            WHERE email = %(email)s;
        """
        resultados = connectToMySQL("esquema_loginreg").query_db(query, datos)
        return len(resultados) > 0
```

---

# 19. ¿Qué estamos aprendiendo en este modelo?

Tenemos un método de validación:

```
@staticmethod
def validar_usuario(datos):
```

Recibe:

```
datos
```

como diccionario.

Por ejemplo:

```
{
    "nombre": "Dany",
    "apellido": "Hernández",
    "email": "dany@email.com",
    "password": "12345678"
}
```

La función retorna:

```
True
```

o:

```
False
```

---

# 20. Validación de email

Utilizamos:

```
EMAIL_REGEX = re.compile(
    r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$'
)
```

Después:

```
if not EMAIL_REGEX.match(datos["email"]):
```

Si el patrón no coincide:

```
flash("El email no tiene un formato válido.", "email")
```

---

# 21. Controlador

Archivo:

```
flask_app/controllers/usuarios.py
```

Código completo:

```
from flask import render_template, redirect, request, session, flash
from flask_app import app, bcrypt
from flask_app.models.usuario import Usuario

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/registro")
def registro():
    return render_template("registro.html")

@app.route("/registrar", methods=["POST"])
def registrar():
    datos = {
        "nombre": request.form["nombre"].strip(),
        "apellido": request.form["apellido"].strip(),
        "email": request.form["email"].strip().lower(),
        "password": request.form["password"]
    }

    if not Usuario.validar_usuario(datos):
        return redirect("/registro")

    if Usuario.existe_email({"email": datos["email"]}):
        flash("El email ya está registrado.", "email")
        return redirect("/registro")

    password_hash = bcrypt.generate_password_hash(
        datos["password"]
    ).decode("utf-8")

    datos["password"] = password_hash

    usuario_id = Usuario.guardar(datos)

    if not usuario_id:
        flash("No fue posible registrar el usuario.", "general")
        return redirect("/registro")

    session["usuario_id"] = usuario_id

    return redirect("/dashboard")

@app.route("/login", methods=["POST"])
def login():
    datos = {
        "email": request.form["email"].strip().lower(),
        "password": request.form["password"]
    }

    usuario = Usuario.buscar_por_email({
        "email": datos["email"]
    })

    if not usuario:
        flash("Email o contraseña incorrectos.", "login")
        return redirect("/")

    if not bcrypt.check_password_hash(
        usuario.password,
        datos["password"]
    ):
        flash("Email o contraseña incorrectos.", "login")
        return redirect("/")

    session["usuario_id"] = usuario.id

    return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
    if "usuario_id" not in session:
        flash("Debes iniciar sesión.", "login")
        return redirect("/")

    usuario = Usuario.buscar_por_id({
        "id": session["usuario_id"]
    })

    return render_template(
        "dashboard.html",
        usuario=usuario
    )

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
```

---

# 22. Agregar `buscar_por_id`

Debemos completar nuestro modelo.

Agregar:

```
@classmethod
def buscar_por_id(cls, datos):
    query = """
        SELECT *
        FROM usuarios
        WHERE id = %(id)s;
    """

    resultados = connectToMySQL(
        "esquema_loginreg"
    ).query_db(query, datos)

    if len(resultados) == 1:
        return cls(resultados[0])

    return False
```

---

# 23. ¿Dónde ocurre el hashing?

En el controlador:

```
password_hash = bcrypt.generate_password_hash(
    datos["password"]
).decode("utf-8")
```

Antes:

```
password = "12345678"
```

Después:

```
password = "$2b$12$..."
```

Solo entonces se envía a MySQL.

---

# 24. ¿Dónde se verifica la contraseña?

Durante el login:

```
bcrypt.check_password_hash(
    usuario.password,
    datos["password"]
)
```

Tenemos:

```
usuario.password
```

que contiene el hash almacenado.

Y:

```
datos["password"]
```

que contiene la contraseña ingresada.

Bcrypt realiza la comparación.

---

# 25. Plantilla base

Archivo:

```
flask_app/templates/base.html
```

```
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Secure Users</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">

<nav class="navbar navbar-dark bg-dark mb-4">
    <div class="container">
        <a class="navbar-brand" href="/">Secure Users</a>

        {% if session.get("usuario_id") %}
            <a href="/logout" class="btn btn-outline-light">
                Cerrar sesión
            </a>
        {% endif %}
    </div>
</nav>

<main class="container">
    {% block contenido %}
    {% endblock %}
</main>

</body>
</html>
```

---

# 26. Página de Login

Archivo:

```
flask_app/templates/login.html
```

```
{% extends "base.html" %}

{% block contenido %}

<div class="row justify-content-center">
    <div class="col-md-6">

        <div class="card shadow">
            <div class="card-body">

                <h1 class="text-center mb-4">
                    Iniciar sesión
                </h1>

                {% with messages = get_flashed_messages(category_filter=["login"]) %}
                    {% if messages %}
                        {% for message in messages %}
                            <div class="alert alert-danger">
                                {{ message }}
                            </div>
                        {% endfor %}
                    {% endif %}
                {% endwith %}

                <form action="/login" method="POST">

                    <div class="mb-3">
                        <label class="form-label">
                            Email
                        </label>

                        <input
                            type="email"
                            name="email"
                            class="form-control"
                            required
                        >
                    </div>

                    <div class="mb-3">
                        <label class="form-label">
                            Contraseña
                        </label>

                        <input
                            type="password"
                            name="password"
                            class="form-control"
                            required
                        >
                    </div>

                    <button class="btn btn-primary w-100">
                        Iniciar sesión
                    </button>

                </form>

                <div class="text-center mt-3">
                    <a href="/registro">
                        Crear una cuenta
                    </a>
                </div>

            </div>
        </div>

    </div>
</div>

{% endblock %}
```

---

# 27. Página de registro

Archivo:

```
flask_app/templates/registro.html
```

```
{% extends "base.html" %}

{% block contenido %}

<div class="row justify-content-center">
    <div class="col-md-7">

        <div class="card shadow">
            <div class="card-body">

                <h1 class="mb-4">
                    Crear nuevo usuario
                </h1>

                {% with messages = get_flashed_messages() %}
                    {% if messages %}
                        {% for message in messages %}
                            <div class="alert alert-danger">
                                {{ message }}
                            </div>
                        {% endfor %}
                    {% endif %}
                {% endwith %}

                <form action="/registrar" method="POST">

                    <div class="mb-3">
                        <label class="form-label">
                            Nombre
                        </label>

                        <input
                            type="text"
                            name="nombre"
                            class="form-control"
                            required
                        >
                    </div>

                    <div class="mb-3">
                        <label class="form-label">
                            Apellido
                        </label>

                        <input
                            type="text"
                            name="apellido"
                            class="form-control"
                            required
                        >
                    </div>

                    <div class="mb-3">
                        <label class="form-label">
                            Email
                        </label>

                        <input
                            type="email"
                            name="email"
                            class="form-control"
                            required
                        >
                    </div>

                    <div class="mb-3">
                        <label class="form-label">
                            Contraseña
                        </label>

                        <input
                            type="password"
                            name="password"
                            class="form-control"
                            required
                        >

                        <div class="form-text">
                            Mínimo 8 caracteres.
                        </div>
                    </div>

                    <button class="btn btn-success">
                        Crear usuario
                    </button>

                    <a href="/" class="btn btn-secondary">
                        Volver
                    </a>

                </form>

            </div>
        </div>

    </div>
</div>

{% endblock %}
```

---

# 28. Dashboard

Archivo:

```
flask_app/templates/dashboard.html
```

```
{% extends "base.html" %}

{% block contenido %}

<div class="card shadow">
    <div class="card-body">

        <h1 class="mb-4">
            Bienvenido, {{ usuario.nombre }}
        </h1>

        <p>
            Has iniciado sesión correctamente.
        </p>

        <hr>

        <dl class="row">
            <dt class="col-sm-3">Nombre</dt>
            <dd class="col-sm-9">
                {{ usuario.nombre }}
            </dd>

            <dt class="col-sm-3">Apellido</dt>
            <dd class="col-sm-9">
                {{ usuario.apellido }}
            </dd>

            <dt class="col-sm-3">Email</dt>
            <dd class="col-sm-9">
                {{ usuario.email }}
            </dd>
        </dl>

        <a href="/logout" class="btn btn-danger">
            Cerrar sesión
        </a>

    </div>
</div>

{% endblock %}
```

---

# 29. `server.py`

En la raíz del proyecto:

```
from flask_app import app

if __name__ == "__main__":
    app.run(debug=True)
```

Ejecutar:

```
python server.py
```

La aplicación estará disponible en:

```
http://127.0.0.1:5000
```

---

# 30. Funcionamiento completo

## Registro correcto

El usuario ingresa:

```
Nombre: Dany
Apellido: Hernández
Email: dany@gmail.com
Password: 12345678
```

La aplicación:

```
request.form
    ↓
diccionario
    ↓
validar_usuario()
    ↓
existe_email()
    ↓
generate_password_hash()
    ↓
guardar()
    ↓
session
    ↓
dashboard
```

---

# 31. Registro incorrecto

Si el usuario deja:

```
Nombre:
Apellido:
Email:
Password:
```

el modelo genera mensajes:

```
flash("El nombre es obligatorio.", "nombre")
flash("El apellido es obligatorio.", "apellido")
flash("El email es obligatorio.", "email")
flash("La contraseña es obligatoria.", "password")
```

El controlador detecta:

```
if not Usuario.validar_usuario(datos):
```

y ejecuta:

```
return redirect("/registro")
```

---

# 32. Email incorrecto

Ejemplo:

```
danygmail.com
```

No cumple:

```
usuario@dominio.com
```

Entonces:

```
if not EMAIL_REGEX.match(datos["email"]):
```

genera:

```
El email no tiene un formato válido.
```

---

# 33. Email duplicado

Si el usuario intenta registrar:

```
dany@gmail.com
```

y ya existe:

```
if Usuario.existe_email({"email": datos["email"]}):
```

se muestra:

```
El email ya está registrado.
```

Esto también está protegido a nivel de base de datos mediante:

```
UNIQUE
```

---

# 34. ¿Por qué validamos en dos niveles?

Tenemos:

### Aplicación

```
Usuario.existe_email()
```

### Base de datos

```
email VARCHAR(150) UNIQUE
```

La aplicación entrega una mejor experiencia al usuario.

La base de datos proporciona una restricción adicional de integridad.

---

# 35. Seguridad de la sesión

Una vez autenticado:

```
session["usuario_id"] = usuario.id
```

Podemos saber quién inició sesión.

En una ruta protegida:

```
if "usuario_id" not in session:
    return redirect("/")
```

Esto evita que cualquier usuario acceda directamente al dashboard.

---

# 36. Logout

Cerrar sesión:

```
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
```

La sesión se elimina:

```
session.clear()
```

---

# 37. Prueba de seguridad fundamental

Registra:

```
Email:
dany@gmail.com

Password:
12345678
```

Después revisa MySQL:

```
SELECT id, nombre, email, password
FROM usuarios;
```

**La contraseña jamás debería aparecer como:**

```
12345678
```

Debe aparecer un hash Bcrypt similar a:

```
$2b$12$...
```

---

# 38. ¿Por qué no debemos usar MD5?

No debemos implementar:

```
md5(password)
```

ni:

```
sha1(password)
```

para almacenar contraseñas.

Son funciones rápidas y no están diseñadas para el almacenamiento moderno de contraseñas.

Para este proyecto utilizamos:

```
Bcrypt
```

---

# 39. `.env` y seguridad

Nunca debemos escribir directamente:

```
password = "123456"
```

dentro del código.

Tampoco:

```
SECRET_KEY = "mi-clave-secreta"
```

Utilizamos:

```
os.getenv("DB_PASSWORD")
```

y:

```
os.getenv("SECRET_KEY")
```

Los valores reales quedan en:

```
.env
```

---

# 40. Error común: subir `.env`

Antes de hacer:

```
git add .
```

verifica que `.gitignore` tenga:

```
.env
```

Puedes comprobarlo:

```
git status
```

El archivo `.env` no debería aparecer para ser enviado a GitHub.

---

# 41. Pruebas obligatorias

La aplicación debe probar como mínimo:

### Prueba 1 — Registro correcto

```
Nombre: Juan
Apellido: Pérez
Email: juan@gmail.com
Password: 12345678
```

Resultado:

```
Usuario creado.
Dashboard.
```

### Prueba 2 — Nombre vacío

Resultado:

```
El nombre es obligatorio.
```

### Prueba 3 — Apellido vacío

Resultado:

```
El apellido es obligatorio.
```

### Prueba 4 — Email vacío

Resultado:

```
El email es obligatorio.
```

### Prueba 5 — Email inválido

Ejemplo:

```
juangmail.com
```

Resultado:

```
El email no tiene un formato válido.
```

### Prueba 6 — Contraseña corta

Ejemplo:

```
123
```

Resultado:

```
La contraseña debe tener al menos 8 caracteres.
```

### Prueba 7 — Email duplicado

Resultado:

```
El email ya está registrado.
```

### Prueba 8 — Login correcto

Resultado:

```
Dashboard
```

### Prueba 9 — Contraseña incorrecta

Resultado:

```
Email o contraseña incorrectos.
```

### Prueba 10 — Usuario inexistente

Resultado:

```
Email o contraseña incorrectos.
```

### Prueba 11 — Dashboard sin sesión

Ingresar directamente:

```
/dashboard
```

sin iniciar sesión.

Resultado:

```
Redirección al login.
```

### Prueba 12 — Logout

Seleccionar:

```
Cerrar sesión
```

Resultado:

```
Session eliminada
→ Login
```

---

# 42. Flujo MVC completo

```
                 NAVEGADOR
                     │
                     ▼
              CONTROLLER
              usuarios.py
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
       MODEL                 TEMPLATE
     usuario.py              HTML/Jinja
          │                     ▲
          ▼                     │
       MySQL ───────────────────┘
```

El controlador coordina.

El modelo trabaja con los datos.

La plantilla muestra la información.

---

# 43. Responsabilidad de cada archivo

| Archivo              | Responsabilidad                |
| -------------------- | ------------------------------ |
| `server.py`          | Ejecutar aplicación            |
| `__init__.py`        | Configurar Flask y Bcrypt      |
| `mysqlconnection.py` | Conectar con MySQL             |
| `usuario.py`         | Datos y consultas del usuario  |
| `usuarios.py`        | Rutas y lógica del controlador |
| `base.html`          | Estructura general             |
| `login.html`         | Inicio de sesión               |
| `registro.html`      | Registro                       |
| `dashboard.html`     | Área protegida                 |
| `.env`               | Configuración privada          |
| `.env.example`       | Ejemplo de configuración       |
| `.gitignore`         | Archivos que Git no debe subir |

---

# 44. Errores frecuentes

## Error 1

```
ModuleNotFoundError: No module named 'flask_bcrypt'
```

Solución:

```
pipenv install flask-bcrypt
```

---

## Error 2

```
Access denied for user
```

Revisar:

```
DB_USER=
DB_PASSWORD=
```

---

## Error 3

```
Unknown database
```

Verificar que exista:

```
esquema_loginreg
```

---

## Error 4

La sesión no funciona.

Revisar:

```
app.secret_key = os.getenv("SECRET_KEY")
```

---

## Error 5

El `.env` no funciona.

Verificar:

```
from dotenv import load_dotenv

load_dotenv()
```

---

# 45. Punto importante sobre Bcrypt

No necesitamos guardar:

```
password
salt
hash
```

por separado.

Bcrypt genera un resultado que contiene la información necesaria para realizar posteriormente la verificación.

Por eso nuestra tabla solamente necesita:

```
password
```

con suficiente longitud:

```
VARCHAR(255)
```

---

# 46. ¿Qué aprendimos?

Al finalizar esta actividad debes comprender:

### Validación

```
Usuario.validar_usuario(datos)
```

### Regex

```
EMAIL_REGEX.match(email)
```

### Flash

```
flash("Mensaje", "categoria")
```

### Hash

```
bcrypt.generate_password_hash(password)
```

### Verificación

```
bcrypt.check_password_hash(hash, password)
```

### Sesión

```
session["usuario_id"] = usuario.id
```

### Logout

```
session.clear()
```

### Variables de entorno

```
os.getenv("DB_PASSWORD")
```

---

# 47. Checklist del estudiante

Antes de entregar, verifica:

-  La aplicación inicia correctamente. 
-  MySQL está funcionando. 
-  La base de datos está creada. 
-  La tabla `usuarios` está creada. 
-  La tabla utiliza `UNIQUE` para email. 
-  La contraseña no se almacena en texto plano. 
-  Bcrypt está instalado. 
-  Bcrypt se utiliza al registrar. 
-  Bcrypt se utiliza al iniciar sesión. 
-  Existe validación de campos. 
-  Existe validación mediante regex. 
-  Existen mensajes `flash`. 
-  Existe validación de email duplicado. 
-  Existe sesión. 
-  Existe logout. 
-  El dashboard está protegido. 
-  Existe `.env`. 
- `.env` está en `.gitignore`. 
-  Existe `.env.example`. 
-  Bootstrap está implementado. 
-  La aplicación está modularizada. 
-  El código está organizado. 
-  El proyecto funciona desde cero. 

---

# 48. Entregable

El estudiante debe entregar:

### 1. Proyecto

Repositorio de GitHub con:

```
flask_app/
server.py
Pipfile
Pipfile.lock
.env.example
.gitignore
README.md
```

### 2. Evidencia

Capturas que demuestren:

-  Registro correcto. 
-  Validación de errores. 
-  Email inválido. 
-  Email duplicado. 
-  Login correcto. 
-  Login incorrecto. 
-  Dashboard. 
-  Logout. 
-  Hash almacenado en MySQL. 

### 3. ERD

Dentro del proyecto crear:

```
resources/
└── ERD/
    └── esquema_loginreg.png
```

> **Regla del curso:** todo proyecto que utilice una base de datos debe incluir su ERD dentro de la carpeta `resources/`.

---

# 49. Estructura final esperada

```
secure_users/
│
├── flask_app/
│   ├── __init__.py
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   └── mysqlconnection.py
│   │
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── usuarios.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── usuario.py
│   │
│   └── templates/
│       ├── base.html
│       ├── login.html
│       ├── registro.html
│       └── dashboard.html
│
├── resources/
│   └── ERD/
│       └── esquema_loginreg.png
│
├── .env
├── .env.example
├── .gitignore
├── Pipfile
├── Pipfile.lock
├── README.md
└── server.py
```

---

## 📦 Resumen de entrega

Antes de entregar, el repositorio debe contener:

```text
secure_users/
├── flask_app/
├── resources/
│   └── ERD/
│       └── esquema_loginreg.png
├── .env.example
├── .gitignore
├── Pipfile
├── Pipfile.lock
├── README.md
└── server.py
```

> ⚠️ **Importante:** el archivo `.env` debe existir localmente, pero **no debe subirse a GitHub**.

---

# 50. Preguntas de comprensión

Responde en tu `README.md`:

### 1. ¿Cuál es la diferencia entre hashing y cifrado?

### 2. ¿Por qué no debemos guardar una contraseña en texto plano?

### 3. ¿Qué función cumple Bcrypt?

### 4. ¿Qué hace `generate_password_hash()`?

### 5. ¿Qué hace `check_password_hash()`?

### 6. ¿Por qué no necesitamos almacenar manualmente el `salt`?

### 7. ¿Qué función cumple `.env`?

### 8. ¿Por qué `.env` debe estar en `.gitignore`?

### 9. ¿Qué información guardamos en `session`?

### 10. ¿Qué ocurre si el usuario intenta acceder a `/dashboard` sin iniciar sesión?

### 11. ¿Por qué utilizamos `UNIQUE` en el email?

### 12. ¿Qué responsabilidad tiene el modelo?

### 13. ¿Qué responsabilidad tiene el controlador?

### 14. ¿Qué responsabilidad tiene la plantilla?

---

# 51. Concepto final

El flujo completo que debes comprender es:

```
                 USUARIO
                    │
                    ▼
               FORMULARIO
                    │
                    ▼
              CONTROLLER
                    │
                    ▼
             VALIDACIONES
                    │
             ┌──────┴──────┐
             │             │
          INVÁLIDO        VÁLIDO
             │             │
             ▼             ▼
           FLASH        ¿EMAIL ÚNICO?
                           │
                    ┌──────┴──────┐
                    │             │
                   NO            SÍ
                    │             │
                  FLASH          BCRYPT
                                  │
                                  ▼
                              HASH
                                  │
                                  ▼
                                MYSQL
                                  │
                                  ▼
                               SESSION
                                  │
                                  ▼
                              DASHBOARD
```

La idea central de esta actividad es comprender que **la seguridad no consiste únicamente en esconder una contraseña**, sino en diseñar correctamente todo el flujo:

```
VALIDAR
   ↓
PROTEGER
   ↓
HASHEAR
   ↓
ALMACENAR
   ↓
VERIFICAR
   ↓
AUTENTICAR
   ↓
CONTROLAR ACCESO
```

**Resultado esperado:** una aplicación Flask modularizada que permita registrar e iniciar sesión de usuarios utilizando **Bcrypt, MySQL, sesiones, validaciones, mensajes flash, `.env` y Bootstrap**, manteniendo las contraseñas protegidas y separando correctamente las responsabilidades mediante MVC.