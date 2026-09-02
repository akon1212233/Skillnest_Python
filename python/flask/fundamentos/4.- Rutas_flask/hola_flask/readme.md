# 🌐 Lección 4 - Rutas en Flask

> **Curso:** Desarrollo Web con Flask desde Cero  
> **Lección 4:** Rutas (Routes) en Flask  
> **Duración estimada:** 60 - 90 minutos

---

# 📖 Descripción General

Hasta ahora hemos construido nuestro primer servidor web con Flask y aprendido cómo responder con el clásico **"¡Hola Mundo!"**.

Sin embargo, una aplicación web real no posee una única página. Un sistema web normalmente cuenta con decenas o incluso cientos de páginas diferentes.

Por ejemplo:

- Página de inicio
- Iniciar sesión
- Registro de usuarios
- Perfil del usuario
- Lista de productos
- Panel de administración
- Contacto
- Reportes

¿Cómo sabe Flask qué función ejecutar cuando un usuario visita una dirección determinada?

La respuesta son **las rutas (Routes).**

Las rutas son uno de los componentes más importantes de Flask. Cada vez que un usuario escribe una dirección en el navegador o hace clic sobre un enlace, Flask identifica la ruta solicitada y ejecuta la función correspondiente.

En esta lección aprenderemos a crear rutas estáticas, rutas dinámicas, recibir parámetros desde la URL y utilizar convertidores de tipo para validar automáticamente los datos recibidos.

Estos conceptos serán utilizados durante todo el curso.

---

# 🎯 Objetivos

Al finalizar esta lección serás capaz de:

- Comprender qué es una ruta dentro de una aplicación web.
- Crear múltiples rutas en Flask.
- Asociar una URL a una función.
- Recibir parámetros desde la URL.
- Crear rutas dinámicas.
- Utilizar convertidores de tipo.
- Comprender el flujo completo entre navegador y servidor.

---

# 📚 Antes de comenzar

En esta lección continuaremos trabajando sobre el proyecto creado en las clases anteriores.

Si vienes comenzando el curso o deseas crear el proyecto nuevamente, sigue el siguiente procedimiento desde cero.

---

# 🏗 Paso 1. Crear la carpeta del proyecto

Crea la siguiente estructura de carpetas.

```text
python/
│
└── flask/
      │
      └── fundamentos/
              │
              └── hola_flask/
```

La carpeta **hola_flask** será nuestro proyecto Flask.

---

# 🖥 Paso 2. Abrir el proyecto con Visual Studio Code

Abre **Visual Studio Code**.

Selecciona:

```
Archivo
    ↓
Abrir carpeta...
```

Luego selecciona la carpeta:

```text
hola_flask
```

---

# 💻 Paso 3. Abrir una terminal

Dentro de VS Code selecciona:

```
Terminal
      ↓
Nueva Terminal
```

La terminal debería ubicarse dentro del proyecto.

Puedes comprobarlo ejecutando.

### Windows

```bash
cd
```

### macOS / Linux

```bash
pwd
```

El resultado debería terminar en:

```text
hola_flask
```

---

# 📦 Paso 4. Instalar Flask (si aún no está instalado)

Si es la primera vez que trabajas con este proyecto ejecuta:

```bash
pipenv install flask
```

Esto realizará automáticamente:

- Creación del entorno virtual.
- Instalación de Flask.
- Creación del archivo `Pipfile`.
- Creación del archivo `Pipfile.lock`.

---

# 🟢 Paso 5. Activar el entorno virtual

Antes de ejecutar cualquier aplicación debemos activar el entorno virtual.

```bash
pipenv shell
```

Cuando esté activo aparecerá algo similar a:

```text
(hola_flask)
```

Eso significa que estamos trabajando dentro del entorno del proyecto.

---

# 📁 Paso 6. Verificar la estructura

Nuestra carpeta debería verse así.

```text
hola_flask/
│
├── Pipfile
├── Pipfile.lock
└── server.py
```

Si aún no tienes el archivo `server.py`, créalo ahora.

---

# 💻 Paso 7. Abrir el archivo server.py

Este archivo contiene nuestro servidor Flask.

Hasta este momento debería verse aproximadamente así.

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def inicio():
    return "¡Hola Mundo!"

if __name__ == "__main__":
    app.run(debug=True)
```

A partir de este código comenzaremos a trabajar.

---

# 🌎 ¿Qué es una ruta?

Una ruta (**Route**) representa una dirección dentro de una aplicación web.

Cada vez que un usuario escribe una dirección en el navegador, Flask analiza esa URL y decide qué función ejecutar.

Por ejemplo.

| URL | Función |
|------|----------|
| `/` | Página principal |
| `/login` | Inicio de sesión |
| `/productos` | Catálogo |
| `/usuarios` | Lista de usuarios |
| `/contacto` | Página de contacto |

Cada una de estas páginas corresponde a una función diferente dentro del servidor.

---

# 🧩 Componentes de una ruta

Una ruta está formada por dos elementos.

## 🔤 Método HTTP

Indica qué acción desea realizar el cliente.

Los más utilizados son.

| Método | Uso |
|---------|---------------------------|
| GET | Obtener información |
| POST | Enviar información |
| PUT | Actualizar información |
| PATCH | Actualizar parcialmente |
| DELETE | Eliminar información |

Durante estas primeras clases utilizaremos únicamente **GET**.

---

## 🔗 URL

Es la dirección que visita el usuario.

Ejemplo.

```
http://localhost:5000/productos
```

Aquí:

Servidor

```
http://localhost:5000
```

Ruta

```
/productos
```

---

# 🏗 Creando nuestra segunda ruta

Debajo de la ruta principal agregaremos una nueva.

```python
@app.route("/exito")
def exito():
    return "¡Éxito!"
```

Ahora nuestro servidor completo será:

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def inicio():
    return "¡Hola Mundo!"

@app.route("/exito")
def exito():
    return "¡Éxito!"

if __name__ == "__main__":
    app.run(debug=True)
```

---

# ▶️ Paso 8. Ejecutar el servidor

Con el entorno virtual activo ejecuta:

## Windows

```bash
python server.py
```

## macOS

```bash
python3 server.py
```

Si todo salió correctamente aparecerá:

```text
* Running on http://127.0.0.1:5000
```

---

# 🌐 Paso 9. Probar la nueva ruta

Abre el navegador.

Visita:

```
http://localhost:5000/exito
```

El navegador responderá:

```text
¡Éxito!
```

---

# 🤔 ¿Y si queremos saludar a cualquier persona?

Podríamos crear:

```python
/saludo/juan
```

```python
/saludo/pedro
```

```python
/saludo/maria
```

Pero eso significaría crear cientos de funciones.

No sería una buena práctica.

Además estaríamos rompiendo el principio:

> **D.R.Y. (Don't Repeat Yourself)**

---

# 🚀 Rutas Variables

Flask permite recibir información directamente desde la URL.

Agreguemos una nueva ruta.

```python
@app.route("/saludo/<nombre>")
def saludo(nombre):

    return f"¡Hola {nombre}!"
```

Observa que:

```python
<nombre>
```

está entre `< >`.

Eso indica que Flask debe capturar ese valor desde la URL.

---

# ▶️ Probar la ruta

Ahora visita.

```
http://localhost:5000/saludo/Nestor
```

Flask ejecutará:

```python
saludo("Nestor")
```

Mostrando.

```text
¡Hola Nestor!
```

Tal como se observa en la siguiente imagen.

> *(Inserta aquí la imagen del saludo "¡Hola Nestor!")*

---

# 📥 Podemos utilizar cualquier nombre

Todas estas direcciones funcionarán.

```
/saludo/Carlos
```

```
/saludo/Maria
```

```
/saludo/Felipe
```

```
/saludo/Ana
```

Sin modificar el código.

---

# 🌈 Varias variables

También podemos recibir múltiples parámetros.

```python
@app.route("/color/<nombre>/<color>")
def color_favorito(nombre, color):

    return f"Hola {nombre}, tu color favorito es {color}"
```

Ejemplo.

```
http://localhost:5000/color/Nestor/Azul
```

Resultado.

```text
Hola Nestor, tu color favorito es Azul
```

---

# 🔁 Convertidores de tipo

Por defecto todos los parámetros llegan como texto.

Incluso:

```
5
```

es recibido como:

```python
"5"
```

Flask permite convertir automáticamente el tipo de dato.

---

## Convertidor entero

```python
@app.route("/saludo/<nombre>/<int:veces>")
def repetir(nombre, veces):

    return f"¡Hola {nombre}!" * veces
```

---

# 🌐 Probar

Visita.

```
http://localhost:5000/saludo/Nestor/5
```

Flask convierte automáticamente.

```python
"5"
```

en

```python
5
```

Por eso Python puede repetir el saludo cinco veces.

Resultado.

```text
¡Hola Nestor!
¡Hola Nestor!
¡Hola Nestor!
¡Hola Nestor!
¡Hola Nestor!
```

Como se muestra en la siguiente imagen.

> *(Inserta aquí la imagen donde el saludo aparece repetido cinco veces.)*

---

# 🚫 ¿Qué sucede si escribimos texto?

Intentemos.

```
http://localhost:5000/saludo/Nestor/cinco
```

Flask intentará convertir.

```text
cinco
```

a un entero.

Como no puede hacerlo responderá automáticamente con un:

```text
404 Not Found
```

Porque la ruta exige un número entero.

---

# 📚 Convertidores disponibles

| Convertidor | Tipo de dato |
|-------------|--------------|
| `string` | Texto (por defecto) |
| `int` | Número entero |
| `float` | Número decimal |
| `path` | Texto incluyendo "/" |
| `uuid` | Identificador UUID |

---

# 💼 Ejemplo en una aplicación real

Supongamos una tienda online.

El usuario visita:

```
/producto/15
```

Flask ejecuta.

```python
@app.route("/producto/<int:id>")
```

Recibe.

```python
id = 15
```

Luego consulta MySQL.

```sql
SELECT *
FROM productos
WHERE id = 15;
```

Finalmente genera la página del producto solicitado.

Así funcionan prácticamente todos los sitios web modernos.

---

# 🧠 Resumen

En esta lección aprendimos que:

- Una ruta representa una dirección dentro de una aplicación web.
- Cada ruta está asociada a una función mediante `@app.route()`.
- Podemos crear múltiples rutas dentro del mismo servidor.
- Flask permite recibir parámetros desde la URL mediante rutas dinámicas.
- Los convertidores validan automáticamente el tipo de dato recibido.
- Las rutas dinámicas permiten reutilizar código y seguir el principio **D.R.Y. (Don't Repeat Yourself)**.

Las rutas serán uno de los elementos más utilizados durante todo el desarrollo de aplicaciones con Flask.

---

# 📝 Tarea

## 🎯 Objetivo

Practicar la creación de rutas estáticas, rutas dinámicas y el uso de convertidores de tipo en Flask, fortaleciendo la comprensión sobre cómo el servidor responde a diferentes solicitudes realizadas desde el navegador.

---

## 📌 Instrucciones

Modifica tu archivo **`server.py`** para que implemente las siguientes rutas.

| Ruta | Resultado esperado |
|------|--------------------|
| `/` | Mostrar **"Bienvenido a Flask"**. |
| `/exito` | Mostrar **"¡Éxito!"**. |
| `/saludo/<nombre>` | Saludar utilizando el nombre recibido. Ejemplo: **"¡Hola Daniel!"** |
| `/color/<nombre>/<color>` | Mostrar el color favorito del usuario. Ejemplo: **"Hola Daniel, tu color favorito es Azul."** |
| `/saludo/<nombre>/<int:veces>` | Repetir el saludo la cantidad de veces indicada en la URL. |

---

## 🚀 Desafíos adicionales

Una vez completadas las rutas anteriores, crea las siguientes rutas utilizando los conceptos aprendidos en clase.

### 1️⃣ Ruta de despedida

Crea una ruta que reciba un nombre y despida al usuario.

**Ruta**

```text
/despedida/<nombre>
```

**Ejemplo**

```
http://localhost:5000/despedida/Camila
```

**Resultado esperado**

```text
¡Hasta luego Camila! ¡Esperamos verte pronto!
```

---

### 2️⃣ Ruta de presentación

Recibe el nombre y la edad de una persona.

La edad debe utilizar el convertidor **int**.

**Ruta**

```text
/presentacion/<nombre>/<int:edad>
```

**Ejemplo**

```
http://localhost:5000/presentacion/Juan/20
```

**Resultado esperado**

```text
Hola Juan, tienes 20 años.
```

---

### 3️⃣ Ruta de suma

Recibe dos números enteros y devuelve la suma.

**Ruta**

```text
/suma/<int:a>/<int:b>
```

**Ejemplo**

```
http://localhost:5000/suma/15/8
```

**Resultado esperado**

```text
La suma es: 23
```

---

### 4️⃣ Ruta de multiplicación

Recibe dos números enteros y devuelve el resultado de la multiplicación.

**Ruta**

```text
/multiplicar/<int:a>/<int:b>
```

**Ejemplo**

```
http://localhost:5000/multiplicar/7/9
```

**Resultado esperado**

```text
El resultado es: 63
```

---

### 5️⃣ Ruta de número par o impar

Recibe un número entero e indica si es par o impar.

**Ruta**

```text
/paridad/<int:numero>
```

**Ejemplo**

```
http://localhost:5000/paridad/18
```

**Resultado esperado**

```text
El número 18 es PAR.
```

Otro ejemplo:

```
http://localhost:5000/paridad/7
```

Resultado:

```text
El número 7 es IMPAR.
```

---

### Evidencias

Entrega capturas donde se observe:

- El código completo de `server.py`.
- La terminal ejecutando Flask.
- El navegador mostrando correctamente las siguientes rutas:

```
http://localhost:5000/exito
```

```
http://localhost:5000/saludo/TuNombre
```

```
http://localhost:5000/color/TuNombre/Azul
```

```
http://localhost:5000/saludo/TuNombre/5
```

---

# 🚀 Próxima Lección

En la siguiente clase aprenderemos a trabajar con **plantillas HTML utilizando Jinja2**, dejando atrás las respuestas de texto para comenzar a construir páginas web dinámicas con Flask, separando la lógica del servidor de la interfaz de usuario.
Mostrando README.md