# 🚨 Lección 5 - Manejo de Errores y Códigos de Estado HTTP en Flask

> **Curso:** Desarrollo Web con Flask desde Cero  
> **Lección 5:** Manejo de errores y respuestas HTTP personalizadas  
> **Duración estimada:** 60 - 90 minutos

---

# 📖 Descripción General

Hasta este momento hemos aprendido a construir un servidor web utilizando Flask, crear rutas estáticas y dinámicas, además de recibir parámetros desde la URL.

Sin embargo, ¿qué ocurre cuando un usuario intenta acceder a una página que no existe?

Por ejemplo:

```
http://localhost:5000/usuarios
```

cuando nuestro servidor solamente tiene las rutas:

```
/
```

y

```
/saludo/<nombre>
```

El servidor responde con un error.

Las aplicaciones profesionales no muestran únicamente un mensaje de error; normalmente presentan una página amigable que informa al usuario qué ocurrió y cómo continuar navegando.

En esta lección aprenderemos a detectar y controlar esos errores utilizando Flask, además de comprender qué son los **códigos de estado HTTP (HTTP Status Codes)** y por qué son tan importantes en el desarrollo web.

---

# 🎯 Objetivos

Al finalizar esta lección serás capaz de:

- Comprender qué es un código de estado HTTP.
- Identificar los códigos HTTP más utilizados.
- Entender el significado del error **404 Not Found**.
- Crear páginas de error personalizadas utilizando Flask.
- Utilizar el decorador `@app.errorhandler()`.
- Devolver códigos HTTP personalizados desde nuestras funciones.
- Mejorar la experiencia del usuario cuando ocurre un error.

---

# 🌎 ¿Qué ocurre cuando visitamos una página?

Cuando un usuario escribe una dirección en el navegador ocurre el siguiente proceso.

```text
Usuario
      │
      ▼
Escribe una URL

      │
      ▼
El navegador envía una solicitud HTTP

      │
      ▼
Flask recibe la solicitud

      │
      ▼
¿Existe esa ruta?

   Sí ─────────► Ejecuta la función
   │
   │
   No
   ▼
Devuelve Error 404
```

Cada vez que el servidor responde a una solicitud, además del contenido, también envía un **código de estado HTTP**.

---

# 📡 ¿Qué son los códigos HTTP?

Los códigos HTTP son números de **tres dígitos** que indican el resultado de una solicitud realizada al servidor.

Gracias a ellos, el navegador sabe si todo salió correctamente o si ocurrió algún problema.

---

# 📚 Códigos HTTP más utilizados

| Código | Significado | ¿Qué indica? |
|---------|-------------|--------------|
| **200** | OK | La solicitud fue exitosa. |
| **201** | Created | Se creó un nuevo recurso. |
| **301** | Moved Permanently | El recurso cambió de ubicación. |
| **400** | Bad Request | La solicitud enviada es incorrecta. |
| **401** | Unauthorized | El usuario no está autenticado. |
| **403** | Forbidden | El usuario no tiene permisos. |
| **404** | Not Found | La página o recurso no existe. |
| **500** | Internal Server Error | Ocurrió un error interno en el servidor. |

Durante esta lección trabajaremos principalmente con el código **404**.

---

# ❌ ¿Qué significa un Error 404?

El código **404 Not Found** indica que el servidor recibió correctamente la solicitud, pero no encontró el recurso solicitado.

Por ejemplo.

Si nuestro servidor posee únicamente la ruta:

```python
@app.route("/")
```

y el usuario visita:

```
http://localhost:5000/productos
```

Flask responderá automáticamente:

```text
404 Not Found
```

Esto no significa que el servidor esté apagado.

Simplemente significa que **esa ruta no existe**.

---

# 🔍 Probemos el error

Ejecuta tu servidor normalmente.

```
python server.py
```

Ahora escribe una dirección inexistente.

```
http://localhost:5000/cualquiercosa
```

Verás una página similar a esta.

```text
404 Not Found

The requested URL was not found on the server.
```

Aunque el mensaje cumple su función, no resulta muy amigable para el usuario.

---

# 🚀 Personalizando el Error 404

Flask permite interceptar los errores antes de enviarlos al navegador.

Para ello utilizaremos un nuevo decorador.

```python
@app.errorhandler(404)
```

Este decorador indica:

> "Cuando ocurra un Error 404, ejecuta esta función."

---

# ✨ Nuestro primer manejador de errores

Agrega el siguiente código antes del bloque:

```python
if __name__ == "__main__":
```

```python
@app.errorhandler(404)
def pagina_no_encontrada(error):
    return "⚠️ Error 404 - La página que buscas no existe.", 404
```

Observa que la función recibe un parámetro llamado `error`.

Aunque en esta lección no lo utilizaremos, Flask envía automáticamente información sobre el error ocurrido.

---

# ▶️ Ejecutar nuevamente el servidor

Guarda el archivo.

Si tienes activado el modo **Debug**, Flask reiniciará automáticamente.

Ahora vuelve a visitar una ruta inexistente.

```
http://localhost:5000/prueba
```

El navegador mostrará:

```text
⚠️ Error 404 - La página que buscas no existe.
```

Mucho más claro para el usuario.

---

# 🧐 ¿Qué significa el número 404 al final del return?

Observa esta línea.

```python
return "⚠️ Error 404", 404
```

Aquí estamos devolviendo dos elementos.

El primero:

```python
"⚠️ Error 404"
```

corresponde al contenido que verá el usuario.

El segundo:

```python
404
```

corresponde al código HTTP que enviará el servidor.

Esto permite que el navegador y otras aplicaciones comprendan exactamente qué ocurrió.

---

# 📌 ¿Qué sucede si no escribimos el 404?

Por ejemplo.

```python
return "Página no encontrada"
```

Flask responderá con un código **200 OK**.

Eso sería incorrecto, porque realmente ocurrió un error.

Por esta razón siempre debemos devolver el código correspondiente.

---

# 💼 Ejemplo en una aplicación real

Imagina una tienda virtual.

Un usuario intenta ingresar a:

```
/producto/1500
```

Pero ese producto fue eliminado de la base de datos.

En lugar de mostrar un mensaje técnico, el sitio podría responder:

```text
Lo sentimos.

El producto que buscas ya no está disponible.

Puedes volver al catálogo principal.
```

Todo esto puede implementarse utilizando un manejador de errores.

---

# 🛠️ Personalizando aún más la respuesta

Nada impide que nuestro mensaje sea más amigable.

```python
@app.errorhandler(404)
def pagina_no_encontrada(error):

    return """
    <h1>⚠️ Página no encontrada</h1>

    <p>Lo sentimos, la página que intentas visitar no existe.</p>

    <a href="/">Volver al inicio</a>
    """, 404
```

Observa que Flask puede devolver incluso código HTML.

Más adelante aprenderemos a utilizar plantillas HTML con **Jinja2**, lo que hará este proceso mucho más ordenado.

---

# 📋 Nuestro servidor hasta ahora

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def inicio():
    return "Bienvenido a Flask"

@app.route("/saludo/<nombre>")
def saludo(nombre):
    return f"Hola {nombre}"

@app.errorhandler(404)
def pagina_no_encontrada(error):
    return "⚠️ Error 404 - Página no encontrada.", 404

if __name__ == "__main__":
    app.run(debug=True)
```

---

# 💡 Buenas prácticas

## ✅ Utiliza mensajes claros

En lugar de mostrar:

```text
404
```

es mejor mostrar:

```text
La página que buscas no existe.
```

---

## ✅ Conserva el código HTTP correcto

Siempre devuelve el código correspondiente.

```python
return "Página no encontrada", 404
```

---

## ✅ Ayuda al usuario

Siempre que sea posible ofrece una alternativa.

Ejemplo.

```
Volver al inicio

Ir al catálogo

Iniciar sesión
```

---

# 🧠 Resumen

En esta lección aprendimos que:

- Todo servidor responde utilizando códigos HTTP.
- El código **404** indica que la página solicitada no existe.
- Flask permite interceptar errores mediante `@app.errorhandler()`.
- Podemos crear respuestas mucho más amigables para el usuario.
- Es importante devolver el código HTTP correcto junto con el contenido.

El manejo de errores mejora significativamente la experiencia del usuario y es una práctica fundamental en cualquier aplicación profesional.

---

# 📝 Tarea

## 🎯 Objetivo

Practicar el manejo de errores HTTP y crear respuestas personalizadas utilizando Flask.

---

## 📌 Parte 1 - Error 404 personalizado

Agrega un manejador para el error **404**.

Debe mostrar un mensaje similar al siguiente:

```text
⚠️ La página que intentas visitar no existe.
```

Devuelve correctamente el código HTTP **404**.

---

## 📌 Parte 2 - Mensaje HTML

Modifica el manejador para que responda utilizando HTML.

Debe contener al menos:

- Un título (`<h1>`).
- Un párrafo (`<p>`).
- Un enlace para volver al inicio (`<a>`).

Ejemplo esperado:

```
⚠️ Página no encontrada

Lo sentimos, el recurso solicitado no existe.

Volver al inicio
```

---

## 📌 Parte 3 - Ruta inexistente

Prueba al menos **cinco** rutas inexistentes diferentes.

Por ejemplo.

```
/hola
```

```
/usuarios
```

```
/productos
```

```
/python
```

```
/flask
```

Comprueba que todas muestran tu página personalizada.

---

## 📌 Parte 4 - Investiga

Investiga y responde brevemente las siguientes preguntas.

1. ¿Qué significa el código HTTP **500**?
- Error interno en el servidor
2. ¿Qué diferencia existe entre un error **401** y un **403**?
- 401 es para cuando un usuario aun no tiene la autorizacion del servidor para ver eso y 403 es para cuando el usuario directamente no tiene acceso a esa informacion
3. ¿Qué código HTTP devuelve Flask cuando una página funciona correctamente?
- Codigo 200
---

## 📌 Parte 5 - Personaliza tu página

Diseña una página de error más atractiva.

Puedes incluir:

- Emojis.
- HTML.
- Colores mediante etiquetas HTML.
- Un mensaje humorístico.
- Una cita.
- Un enlace para volver al inicio.

Sé creativo.

---

## 📸 Evidencias

Entrega un documento con:

- Captura del código de `server.py`.
- Captura de la terminal ejecutando Flask.
- Captura de una ruta válida.
- Captura de una ruta inexistente mostrando el error personalizado.
- Respuestas a las preguntas de investigación.

---

# 🚀 Próxima Lección

Hasta ahora todas nuestras respuestas han sido simples cadenas de texto o pequeños fragmentos de HTML escritos directamente en Python.

En la siguiente clase aprenderemos a separar la lógica de la presentación utilizando el **motor de plantillas Jinja2**, permitiéndonos construir páginas HTML organizadas, reutilizables y mucho más profesionales.