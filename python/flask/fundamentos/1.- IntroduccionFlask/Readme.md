# 🚀 Lección 1 - Introducción a Flask

> **Curso:** Desarrollo Web con Flask desde Cero  
> **Nivel:** Intermedio  
> **Prerrequisitos:** Python, Programación Orientada a Objetos (POO) y MySQL.

---

# 📖 Descripción General

¡Bienvenido al módulo de **Flask**!

Hasta este momento has adquirido una base sólida en programación con Python. Ya eres capaz de crear programas utilizando variables, estructuras de control, funciones, Programación Orientada a Objetos (POO) y bases de datos relacionales con MySQL.

Ahora es momento de dar el siguiente paso: **crear aplicaciones web dinámicas**.

Durante este curso aprenderás a desarrollar aplicaciones web utilizando **Flask**, un microframework de Python ampliamente utilizado tanto para proyectos personales como para aplicaciones profesionales.

A diferencia de los programas de consola que hemos desarrollado hasta ahora, las aplicaciones web permiten que cualquier usuario interactúe con ellas desde un navegador como Google Chrome, Microsoft Edge o Firefox.

Al finalizar este módulo serás capaz de desarrollar aplicaciones completas que incluyan:

- Interfaces web con HTML.
- Estilos mediante CSS.
- Interactividad con JavaScript.
- Programación del servidor utilizando Python.
- Conexión con bases de datos MySQL.
- Registro e inicio de sesión de usuarios.
- Operaciones CRUD (Crear, Leer, Actualizar y Eliminar).
- Organización profesional del código.

> **Importante:** Flask no reemplaza los conocimientos de Python. Todo lo que has aprendido hasta ahora seguirá siendo utilizado constantemente durante este curso.

---

# 🎯 Objetivos de la Lección

Al finalizar esta lección serás capaz de:

- Comprender qué es Flask.
- Recordar los conocimientos previos que utilizaremos durante el curso.
- Identificar los principales componentes de una aplicación Flask.
- Comprender el flujo básico de una aplicación web.
- Entender cómo interactúan el navegador, el servidor y la base de datos.

---

# 📚 ¿Qué conocimientos ya tenemos?

Antes de comenzar con Flask, repasemos todo lo que ya sabemos y que será utilizado constantemente.

---

## 🐍 Python

Python será el lenguaje principal del servidor.

Toda la lógica de negocio seguirá siendo escrita en Python.

Ejemplo:

```python
nombre = "Daniel"

if nombre == "Daniel":
    print("Bienvenido")
```

---

## 🔤 Variables

Las variables almacenan información.

```python
nombre = "Carlos"
edad = 25
activo = True
```

---

## 📋 Listas

Nos permiten almacenar múltiples elementos.

```python
productos = [
    "Notebook",
    "Mouse",
    "Teclado"
]
```

---

## 🔁 Bucles

Permiten recorrer colecciones de datos.

```python
for producto in productos:
    print(producto)
```

---

## 🔀 Condicionales

Permiten tomar decisiones.

```python
edad = 18

if edad >= 18:
    print("Mayor de edad")
else:
    print("Menor de edad")
```

---

## 🛠 Funciones

Nos ayudan a reutilizar código.

```python
def saludar(nombre):
    return f"Hola {nombre}"
```

---

## 🏗 Programación Orientada a Objetos (POO)

Durante este curso trabajaremos constantemente con clases y objetos.

Ejemplo:

```python
class Usuario:

    def __init__(self, nombre):
        self.nombre = nombre

    def saludar(self):
        return f"Hola soy {self.nombre}"
```

---

## 🗄 Bases de Datos MySQL

Más adelante conectaremos Flask con MySQL para almacenar información.

Ejemplo:

```sql
SELECT * FROM usuarios;
```

---

# 🚀 ¿Qué es Flask?

Flask es un **microframework** para Python diseñado para crear aplicaciones web.

Un framework es un conjunto de herramientas que facilita el desarrollo de software.

En lugar de construir todo desde cero, Flask proporciona componentes ya preparados para desarrollar aplicaciones de forma mucho más rápida.

Con Flask podremos:

- Crear sitios web.
- Crear sistemas de administración.
- Desarrollar APIs REST.
- Conectar aplicaciones con MySQL.
- Gestionar usuarios.
- Crear sistemas de autenticación.
- Construir aplicaciones completas.

---

## 🤔 ¿Por qué se llama Microframework?

Se denomina **microframework** porque incluye únicamente las herramientas esenciales para crear aplicaciones web.

Esto significa que:

- Es ligero.
- Es sencillo de aprender.
- Es muy flexible.
- Podemos agregar únicamente las herramientas que realmente necesitamos.

A diferencia de otros frameworks más grandes, Flask no obliga al desarrollador a seguir una estructura específica.

---

# 🌎 ¿Qué es una aplicación web?

Una aplicación web es un programa que funciona desde un navegador.

Algunos ejemplos conocidos son:

- Gmail
- Facebook
- Instagram
- YouTube
- Mercado Libre
- BancoEstado en Línea

Todas estas aplicaciones reciben solicitudes del usuario, procesan información en un servidor y devuelven una respuesta al navegador.

Eso mismo aprenderemos a construir con Flask.

---

# 🧩 Componentes que utilizaremos durante el curso

Durante las próximas unidades aprenderemos a trabajar con los siguientes componentes.

---

## 🖼 Renderizado de Plantillas

Permite enviar archivos HTML al navegador.

Flask utiliza la función:

```python
render_template()
```

Ejemplo:

```python
return render_template("index.html")
```

Gracias a esto podremos separar la lógica del programa (Python) de la interfaz del usuario (HTML).

---

## ↪ Redirecciones

Permiten enviar automáticamente al usuario hacia otra página.

Ejemplo:

```python
return redirect("/dashboard")
```

Esto suele utilizarse después de:

- Iniciar sesión.
- Guardar un formulario.
- Actualizar un registro.
- Eliminar información.

---

## 📝 Formularios

Los formularios permiten que los usuarios envíen información al servidor.

Ejemplo:

```html
<form action="/guardar" method="POST">

    <input
        type="text"
        name="nombre"
    >

    <button>Guardar</button>

</form>
```

Cada vez que un usuario escribe información y presiona un botón, el formulario envía esos datos hacia Flask.

---

## 🔍 Solicitudes HTTP

La comunicación entre un navegador y un servidor se realiza mediante solicitudes HTTP.

Las dos más importantes serán:

### GET

Se utiliza para **solicitar información**.

Ejemplo:

```
GET /productos
```

Generalmente se utiliza para:

- Ver páginas.
- Buscar información.
- Mostrar registros.

---

### POST

Se utiliza para **enviar información**.

Ejemplo:

```
POST /usuarios
```

Generalmente se utiliza para:

- Registrar usuarios.
- Iniciar sesión.
- Guardar formularios.
- Actualizar datos.

---

## 🔐 Sesiones

Las sesiones permiten recordar información del usuario mientras navega por el sistema.

Por ejemplo:

```python
session["usuario"] = "Carlos"
```

Gracias a las sesiones podremos saber:

- Quién inició sesión.
- Qué permisos tiene.
- Qué productos tiene en un carrito de compras.

---

# 🌐 El flujo de una aplicación Flask

Todas las aplicaciones web funcionan siguiendo un flujo muy similar.

```text
Usuario
   │
   ▼
 Navegador
   │
Solicitud HTTP
   │
   ▼
Servidor Flask
(server.py)
   │
Procesa la información
   │
Consulta MySQL (si es necesario)
   │
Genera una respuesta
   │
   ▼
Navegador
```

---

# 🔄 Paso a paso del flujo

## 1️⃣ El usuario realiza una solicitud

Por ejemplo, escribe en el navegador:

```
http://localhost:5000/
```

El navegador envía una solicitud HTTP al servidor.

---

## 2️⃣ Flask recibe la solicitud

El archivo principal (`server.py` o `app.py`) recibe la petición.

Ejemplo:

```python
@app.route("/")
def inicio():
    return render_template("index.html")
```

---

## 3️⃣ Flask procesa la información

Aquí puede realizar diversas tareas:

- Ejecutar lógica de negocio.
- Consultar la base de datos.
- Crear objetos.
- Validar formularios.
- Realizar cálculos.

---

## 4️⃣ Flask prepara la respuesta

Una vez procesada la información, Flask responde al navegador.

La respuesta puede ser:

- Una página HTML.
- Un archivo JSON.
- Una imagen.
- Un archivo PDF.
- Una redirección.

---

## 5️⃣ El navegador muestra el resultado

Finalmente el navegador presenta la información al usuario.

Todo este proceso normalmente ocurre en pocos milisegundos.

---

# 💼 Ejemplo en un sistema real

Imaginemos una tienda online.

El usuario desea ver todos los productos.

El flujo sería el siguiente:

```text
Usuario
      │
      ▼
Escribe:

http://localhost:5000/productos

      │
      ▼
Flask recibe la solicitud

      │
      ▼
Consulta MySQL

      │
      ▼
Obtiene todos los productos

      │
      ▼
Genera la página HTML

      │
      ▼
Envía la respuesta

      │
      ▼
El navegador muestra la lista de productos
```

Este mismo flujo ocurrirá cuando el usuario:

- Inicie sesión.
- Registre una cuenta.
- Agregue un producto.
- Edite información.
- Elimine registros.
- Realice una compra.

---

# 📂 ¿Qué aprenderemos durante este curso?

Durante este módulo construiremos aplicaciones web paso a paso.

Entre los principales temas veremos:

- Instalación de Flask.
- Creación del primer proyecto.
- Rutas.
- Plantillas HTML (Jinja2).
- Archivos estáticos (CSS, JavaScript e imágenes).
- Formularios.
- Métodos GET y POST.
- Validaciones.
- Sesiones.
- CRUD completo.
- Conexión con MySQL.
- Arquitectura MVC.
- Modularización del proyecto.
- Buenas prácticas de desarrollo.

Al finalizar el curso tendrás las bases necesarias para desarrollar aplicaciones web completas utilizando Flask y Python.

---

# ✅ Resumen

En esta primera lección hemos comprendido que:

- Flask es un microframework para desarrollar aplicaciones web con Python.
- Todo el conocimiento previo de Python, POO y MySQL seguirá siendo utilizado.
- Una aplicación web funciona mediante solicitudes (Request) y respuestas (Response).
- Flask actúa como intermediario entre el navegador, la lógica del programa y la base de datos.
- Durante el curso construiremos proyectos utilizando una estructura profesional similar a la utilizada en empresas de desarrollo de software.

---

# 🚀 Próxima Lección

En la siguiente lección prepararemos el entorno de desarrollo e instalaremos Flask para crear nuestra primera aplicación web.