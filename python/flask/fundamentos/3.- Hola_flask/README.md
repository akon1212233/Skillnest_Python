# 🚀 Lección 3 - ¡Hola, Flask!

> **Curso:** Desarrollo Web con Flask desde Cero  
> **Lección 3:** Creando nuestro primer servidor web con Flask.

---

# 📖 Descripción General

¡Ha llegado el momento de crear nuestra primera aplicación web con Flask!

Hasta ahora hemos preparado nuestro entorno de desarrollo e instalado todas las herramientas necesarias. En esta lección construiremos un servidor web muy sencillo que responderá con el clásico mensaje:

> **¡Hola Mundo!**

Aunque parezca un ejemplo muy simple, este proyecto representa el punto de partida de prácticamente cualquier aplicación desarrollada con Flask.

A partir de aquí comprenderemos cómo recibe solicitudes un servidor, cómo responde a un navegador y cómo comienza a construirse una aplicación web profesional.

---

# 🎯 Objetivos

Al finalizar esta lección serás capaz de:

- Crear tu primer servidor utilizando Flask.
- Comprender la estructura mínima de una aplicación Flask.
- Entender qué es una ruta (Route).
- Comprender qué es un decorador.
- Ejecutar una aplicación Flask.
- Acceder al servidor desde el navegador.
- Comprender cómo ocurre la comunicación entre el navegador y el servidor.

---

# 📂 Estructura del proyecto

Dentro de la carpeta creada en la lección anterior (**hola_flask**) crearemos nuestro primer archivo de Python.

```text
hola_flask/
│
├── Pipfile
├── Pipfile.lock
└── server.py
```

> **¿Por qué `server.py`?**
>
> Este archivo será el punto de entrada de nuestra aplicación. Aquí escribiremos la lógica principal del servidor y definiremos las rutas que responderán a las solicitudes de los usuarios.

---

# 💻 Nuestro primer servidor

Crea un archivo llamado:

```text
server.py
```

Y escribe el siguiente código:

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hola_mundo():
    return "¡Hola Mundo!"

if __name__ == "__main__":
    app.run(debug=True)
```

---

# 🔍 Analizando el código paso a paso

Veamos qué hace cada línea del programa.

---

## 1️⃣ Importar Flask

```python
from flask import Flask
```

Aquí importamos la clase **Flask**, que pertenece al framework.

Sin esta importación no podríamos crear una aplicación web.

Piensa en esta línea como cuando importamos una librería de Python para utilizar sus funciones.

---

## 2️⃣ Crear la aplicación

```python
app = Flask(__name__)
```

Aquí estamos creando un objeto llamado **app**.

Este objeto representa toda nuestra aplicación web.

A partir de este momento podremos utilizar métodos como:

- Crear rutas.
- Ejecutar el servidor.
- Configurar la aplicación.
- Registrar extensiones.

---

### ¿Qué significa `__name__`?

Python posee una variable especial llamada:

```python
__name__
```

Flask la utiliza para identificar dónde se encuentra el proyecto y localizar correctamente archivos como:

- HTML
- CSS
- JavaScript
- Imágenes

Por ahora basta con saber que **siempre utilizaremos esta instrucción** al crear una aplicación Flask.

---

## 3️⃣ Crear una ruta

```python
@app.route("/")
```

Esta línea indica que cuando un usuario visite la dirección:

```
http://localhost:5000/
```

Flask ejecutará la función ubicada inmediatamente debajo.

A esta línea se le conoce como **decorador**.

---

## 📌 ¿Qué es un decorador?

Un decorador es una instrucción especial de Python que modifica el comportamiento de una función.

En Flask, los decoradores se utilizan principalmente para asociar una **URL** con una función.

Por ejemplo:

```python
@app.route("/")
```

significa:

> "Cuando alguien visite la ruta `/`, ejecuta esta función."

Más adelante aprenderemos a crear muchas rutas diferentes.

---

## 4️⃣ Crear la función

```python
def hola_mundo():
```

Esta función será ejecutada únicamente cuando alguien visite la ruta `/`.

En Flask, cada ruta normalmente posee una función asociada.

---

## 5️⃣ Enviar una respuesta

```python
return "¡Hola Mundo!"
```

La palabra reservada `return` indica qué información enviará el servidor al navegador.

En este caso la respuesta será simplemente un texto.

Más adelante devolveremos:

- HTML
- JSON
- Imágenes
- Archivos
- Plantillas dinámicas

---

## 6️⃣ Ejecutar la aplicación

```python
if __name__ == "__main__":
    app.run(debug=True)
```

Esta sección inicia el servidor Flask.

Mientras el servidor esté ejecutándose permanecerá esperando solicitudes provenientes del navegador.

---

# 🐞 ¿Qué significa `debug=True`?

El modo **Debug** es una herramienta muy útil durante el desarrollo.

```python
app.run(debug=True)
```

Cuando está activado:

- Reinicia automáticamente el servidor cuando guardamos cambios.
- Muestra información detallada sobre errores.
- Facilita el proceso de desarrollo.

> **Importante:** El modo Debug solo debe utilizarse durante el desarrollo. En aplicaciones publicadas en producción debe estar desactivado por motivos de seguridad.

---

# ▶️ Ejecutar nuestra aplicación

Antes de ejecutar el proyecto debemos activar el entorno virtual.

```bash
pipenv shell
```

Luego ejecutamos el servidor.

## Windows

```bash
python server.py
```

## macOS

```bash
python3 server.py
```

Si todo salió correctamente veremos un resultado similar a este:

```text
* Serving Flask app 'server'
* Debug mode: on

* Running on http://127.0.0.1:5000
```

Esto significa que nuestro servidor está funcionando correctamente.

---

# 🌐 Abrir la aplicación en el navegador

Ahora abre tu navegador favorito e ingresa una de las siguientes direcciones.

```
http://127.0.0.1:5000/
```

o

```
http://localhost:5000/
```

El navegador mostrará:

```text
¡Hola Mundo!
```

🎉 **¡Acabas de crear tu primer servidor web con Flask!**

---

# 🤔 ¿Qué es `localhost`?

Cuando escribimos:

```
http://localhost:5000/
```

estamos indicando al navegador que se conecte a **nuestro propio computador**.

`localhost` siempre hace referencia al equipo desde donde estamos trabajando.

Su dirección IP equivalente es:

```
127.0.0.1
```

Por eso ambas direcciones funcionan exactamente igual:

```
http://localhost:5000/
```

```
http://127.0.0.1:5000/
```

---

# 🔢 ¿Qué es el puerto 5000?

Un computador puede ejecutar muchos servicios al mismo tiempo.

Cada servicio escucha en un número llamado **puerto**.

Ejemplos:

| Puerto | Servicio |
|---------|----------|
| 80 | HTTP |
| 443 | HTTPS |
| 3306 | MySQL |
| 5000 | Flask (por defecto) |

Cuando escribimos:

```
http://localhost:5000/
```

estamos indicando:

- Conéctate a mi computador.
- Utiliza el puerto 5000.
- Solicita la página principal.

---

# 🔄 ¿Qué ocurre cuando visitamos una página?

Cuando escribimos:

```
http://localhost:5000/
```

ocurre el siguiente proceso.

```text
Usuario
      │
      ▼
Escribe la URL

      │
      ▼
El navegador envía una solicitud HTTP

      │
      ▼
Flask recibe la solicitud

      │
      ▼
Busca la ruta "/"

      │
      ▼
Ejecuta la función hola_mundo()

      │
      ▼
Devuelve "¡Hola Mundo!"

      │
      ▼
El navegador muestra el resultado
```

Todo este proceso ocurre en apenas unos milisegundos.

---

# 📌 ¿Qué es una ruta?

Una ruta representa una dirección dentro de nuestra aplicación.

Ejemplo:

```python
@app.route("/")
```

Ruta principal.

---

```python
@app.route("/nosotros")
```

Página "Nosotros".

---

```python
@app.route("/contacto")
```

Página de contacto.

Cada ruta ejecutará una función distinta.

---

# 🧠 Resumen del código

Nuestro programa realiza cuatro acciones principales:

### 📥 Importa Flask

```python
from flask import Flask
```

---

### 🚀 Crea la aplicación

```python
app = Flask(__name__)
```

---

### 🛤 Define una ruta

```python
@app.route("/")
```

---

### ▶️ Inicia el servidor

```python
app.run(debug=True)
```

---

# 💼 Relación con un proyecto real

Imaginemos una tienda en línea.

Cuando un usuario escribe:

```
https://mitienda.cl/productos
```

Flask buscará una ruta similar a:

```python
@app.route("/productos")
```

Luego ejecutará una función que:

- Consultará la base de datos.
- Obtendrá todos los productos.
- Generará una página HTML.
- Enviará la respuesta al navegador.

Aunque hoy solo mostramos un texto, el funcionamiento será exactamente el mismo para aplicaciones mucho más grandes.

---

# ✅ Resumen

En esta lección aprendimos que:

- Toda aplicación Flask comienza creando un objeto `app`.
- Las rutas permiten asociar una URL con una función.
- El decorador `@app.route()` conecta una dirección web con una función de Python.
- `return` envía la respuesta al navegador.
- `app.run(debug=True)` inicia el servidor en modo desarrollo.
- Podemos acceder a nuestra aplicación desde `http://localhost:5000`.

Con estos conceptos ya hemos construido nuestra primera aplicación web funcional.

---

# 📝 Tarea

## Objetivo

Modificar el servidor para responder con un mensaje personalizado.

### Instrucciones

1. Ejecuta correctamente el servidor Flask.
2. Verifica que el navegador muestre `¡Hola Mundo!`.
3. Cambia el mensaje por uno personalizado. Por ejemplo:

```python
return "¡Bienvenido al curso de Flask!"
```

4. Guarda el archivo y observa cómo el servidor se reinicia automáticamente gracias al modo **Debug**.
5. Recarga el navegador y verifica que aparezca el nuevo mensaje.

### Evidencia

Realiza una captura de pantalla donde se observe:

- El archivo `server.py`.
- La terminal ejecutando Flask.
- El navegador mostrando tu mensaje personalizado.

---

# 🚀 Próxima Lección

En la siguiente clase aprenderemos a crear **múltiples rutas** dentro de una misma aplicación, permitiendo que cada URL ejecute una función diferente y responda con contenido específico.
Mostrando README.md 