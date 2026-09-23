# 🔄 Redirección en Flask

## 🎯 Objetivo

Comprender qué es una **redirección** en Flask y por qué es recomendable utilizar `redirect()` después de procesar una solicitud `POST`.

Al finalizar esta actividad serás capaz de:

- Comprender la diferencia entre `POST` y `GET`.
- Utilizar `redirect()` en Flask.
- Crear una ruta encargada de procesar un formulario.
- Redirigir al usuario hacia otra ruta después de procesar los datos.
- Comprender por qué `request.form` ya no está disponible después de una redirección.
- Reconocer el patrón **POST → Redirect → GET (PRG)**.
- Identificar qué problema queda pendiente y que será solucionado posteriormente mediante persistencia de datos.

---

# 🧠 ¿Por qué necesitamos redireccionar?

En las lecciones anteriores aprendimos a recibir información desde un formulario utilizando:

```python
request.form
```

Por ejemplo:

```python
@app.route("/crear_usuario", methods=["POST"])
def crear_usuario():

    nombre = request.form["nombre"]

    email = request.form["email"]

    print(nombre)

    print(email)
```

Una primera aproximación podría ser mostrar inmediatamente una plantilla:

```python
return render_template(
    "mostrar.html",
    nombre=nombre,
    email=email
)
```

Esto funciona, pero existe un problema importante.

Si el usuario actualiza la página después de realizar el `POST`, el navegador puede intentar enviar nuevamente la información.

En una aplicación real esto podría provocar problemas como:

- Registros duplicados.
- Pedidos duplicados.
- Operaciones repetidas.
- Cobros duplicados.
- Envío múltiple de información.

Por esta razón, después de procesar una solicitud `POST`, normalmente realizaremos una **redirección**.

---

# 🔄 Patrón POST → Redirect → GET

La idea es separar el procesamiento de los datos de la visualización de la página.

El flujo será:

```text
Formulario
    │
    │ POST
    ▼
/crear_usuario
    │
    │ Procesa información
    │
    ▼
redirect()
    │
    │ GET
    ▼
/mostrar_usuario
    │
    ▼
mostrar.html
```

Este patrón se conoce como:

> **POST → Redirect → GET (PRG)**

---

# 📁 Estructura del proyecto

Continuaremos utilizando nuestro proyecto:

```text
formulario_prueba/

│
├── server.py
│
└── templates/
    │
    ├── index.html
    │
    └── mostrar.html
```

---

# 🐍 Paso 1 - Crear el servidor

Abre:

```text
server.py
```

y utiliza el siguiente código completo.

```python
# ==========================================
# IMPORTACIONES
# ==========================================

from flask import Flask, render_template, request, redirect


# ==========================================
# CREACIÓN DE LA APLICACIÓN
# ==========================================

app = Flask(__name__)


# ==========================================
# RUTA PRINCIPAL
# ==========================================

@app.route("/")
def index():
    """
    Muestra el formulario de creación de usuario.
    """

    return render_template("index.html")


# ==========================================
# PROCESAR FORMULARIO
# ==========================================

@app.route("/crear_usuario", methods=["POST"])
def crear_usuario():
    """
    Recibe la información enviada mediante POST.

    Esta función se encarga de procesar los datos
    antes de realizar la redirección.
    """

    # ------------------------------------------
    # Obtener los datos enviados por el formulario
    # ------------------------------------------

    nombre = request.form["nombre"]

    email = request.form["email"]


    # ------------------------------------------
    # Mostrar los datos en la terminal
    # ------------------------------------------

    print("===================================")

    print("Información recibida")

    print(f"Nombre: {nombre}")

    print(f"Email: {email}")

    print("===================================")


    # ------------------------------------------
    # Redireccionar al usuario
    # ------------------------------------------

    return redirect("/mostrar_usuario")


# ==========================================
# MOSTRAR RESULTADO
# ==========================================

@app.route("/mostrar_usuario")
def mostrar_usuario():
    """
    Esta ruta recibe una solicitud GET después
    de la redirección.
    """

    print("Usuario redirigido")

    # ------------------------------------------
    # request.form estará vacío
    # ------------------------------------------

    print(request.form)


    # ------------------------------------------
    # Mostrar la plantilla
    # ------------------------------------------

    return render_template("mostrar.html")


# ==========================================
# EJECUTAR SERVIDOR
# ==========================================

if __name__ == "__main__":

    app.run(debug=True)
```

---

# 📝 Paso 2 - Crear el formulario

Dentro de:

```text
templates/
```

crea:

```text
index.html
```

Utiliza el siguiente código completo.

```html
<!DOCTYPE html>

<html lang="es">

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0">

    <title>Crear Usuario</title>

</head>

<body>

    <h1>Crear Usuario</h1>

    <form
        action="{{ url_for('crear_usuario') }}"
        method="POST">

        <!-- Nombre -->

        <label for="nombre">

            Nombre:

        </label>

        <input
            type="text"
            id="nombre"
            name="nombre"
            required>

        <br><br>


        <!-- Email -->

        <label for="email">

            Email:

        </label>

        <input
            type="email"
            id="email"
            name="email"
            required>

        <br><br>


        <!-- Botón de envío -->

        <button type="submit">

            Crear Usuario

        </button>

    </form>

</body>

</html>
```

---

# 📝 Paso 3 - Crear la página de destino

Dentro de:

```text
templates/
```

crea:

```text
mostrar.html
```

Utiliza el siguiente código.

```html
<!DOCTYPE html>

<html lang="es">

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0">

    <title>Usuario Procesado</title>

</head>

<body>

    <h1>Usuario procesado correctamente</h1>

    <p>

        La información fue recibida por el servidor.

    </p>

    <p>

        El servidor procesó la solicitud
        y posteriormente realizó una redirección.

    </p>

    <hr>

    <a href="{{ url_for('index') }}">

        Volver al formulario

    </a>

</body>

</html>
```

---

# ▶️ Paso 4 - Ejecutar la aplicación

Abre una terminal dentro de:

```text
formulario_prueba
```

Ejecuta:

```bash
python server.py
```

Deberías observar algo similar a:

```text
* Running on http://127.0.0.1:5000
```

Abre en el navegador:

```text
http://127.0.0.1:5000/
```

---

# 🧪 Paso 5 - Probar el formulario

Completa:

```text
Nombre:

Juan Pérez
```

y:

```text
Email:

juan@gmail.com
```

Presiona:

```text
Crear Usuario
```

El navegador será enviado automáticamente a:

```text
/mostrar_usuario
```

Es decir:

```text
http://127.0.0.1:5000/mostrar_usuario
```

---

# 🔍 ¿Qué ocurrió?

Observemos el proceso completo.

## 1. El usuario visita `/`

Flask ejecuta:

```python
@app.route("/")
def index():
```

y muestra:

```text
index.html
```

---

## 2. El usuario envía el formulario

El formulario contiene:

```html
<form
    action="{{ url_for('crear_usuario') }}"
    method="POST">
```

Por lo tanto, el navegador realiza:

```text
POST /crear_usuario
```

---

## 3. Flask recibe la información

La ruta:

```python
@app.route("/crear_usuario", methods=["POST"])
```

permite recibir solicitudes `POST`.

Dentro de la función podemos utilizar:

```python
request.form
```

Por ejemplo:

```python
nombre = request.form["nombre"]

email = request.form["email"]
```

En este momento los datos están disponibles.

---

# 🔄 4. Se realiza la redirección

Después de procesar la información ejecutamos:

```python
return redirect("/mostrar_usuario")
```

Flask le indica al navegador:

> "Ahora realiza una nueva solicitud a `/mostrar_usuario`."

El navegador realiza entonces una nueva solicitud:

```text
GET /mostrar_usuario
```

---

# 🌐 5. Flask ejecuta otra función

Ahora entra en funcionamiento:

```python
@app.route("/mostrar_usuario")
def mostrar_usuario():
```

Esta ruta devuelve:

```python
return render_template("mostrar.html")
```

Por eso aparece:

```text
Usuario procesado correctamente
```

---

# ⚠️ ¿Por qué `request.form` está vacío?

Este punto es **fundamental**.

En:

```python
@app.route("/crear_usuario", methods=["POST"])
def crear_usuario():
```

tenemos:

```python
request.form
```

con información.

Por ejemplo:

```python
{
    "nombre": "Juan Pérez",
    "email": "juan@gmail.com"
}
```

Pero después hacemos:

```python
redirect("/mostrar_usuario")
```

y comienza una **nueva solicitud**.

Esta nueva solicitud es:

```text
GET
```

No es:

```text
POST
```

Por lo tanto:

```python
request.form
```

está vacío.

Podemos comprobarlo mediante:

```python
print(request.form)
```

La terminal mostrará:

```text
ImmutableMultiDict([])
```

---

# 🧠 Concepto fundamental

Debemos comprender que:

> **Una redirección no transporta automáticamente los datos de `request.form` hacia la nueva ruta.**

Tenemos:

```text
POST
│
├── nombre
├── email
│
▼
/crear_usuario
│
│
└── redirect()
       │
       ▼
      GET
       │
       ▼
/mostrar_usuario
```

La información del formulario pertenecía a la primera solicitud.

La segunda solicitud comienza nuevamente.

---

# ❌ Un error muy común

Podríamos intentar hacer esto:

```python
@app.route("/crear_usuario", methods=["POST"])
def crear_usuario():

    nombre = request.form["nombre"]

    return redirect("/mostrar_usuario")
```

y después:

```python
@app.route("/mostrar_usuario")
def mostrar_usuario():

    return render_template(
        "mostrar.html",
        nombre=nombre
    )
```

Esto **no funcionará**.

¿Por qué?

Porque `nombre` pertenece a la función:

```python
crear_usuario()
```

Cuando termina esa función, esa variable local deja de estar disponible.

Además, `/mostrar_usuario` corresponde a una solicitud diferente.

---

# 🔐 Entonces, ¿para qué sirve `redirect()`?

La redirección permite separar dos responsabilidades.

### `/crear_usuario`

Se encarga de:

```text
RECIBIR

↓

PROCESAR

↓

GUARDAR

↓

REDIRECCIONAR
```

### `/mostrar_usuario`

Se encarga de:

```text
RECIBIR GET

↓

OBTENER información almacenada

↓

MOSTRAR
```

Esta separación será especialmente importante cuando comencemos a trabajar con bases de datos.

---

# 🏆 Regla fundamental

Cuando recibamos información mediante `POST`:

```python
@app.route("/crear_usuario", methods=["POST"])
def crear_usuario():
```

la recomendación general será:

```python
return redirect(...)
```

en lugar de:

```python
return render_template(...)
```

Por ejemplo:

```python
@app.route("/crear_usuario", methods=["POST"])
def crear_usuario():

    # Procesar información

    return redirect("/mostrar_usuario")
```

---

# 🧩 Actividad práctica

## Desafío - Registro de productos

Ahora aplica exactamente el mismo concepto en un nuevo escenario.

Crea una aplicación llamada:

```text
registro_productos/
```

con esta estructura:

```text
registro_productos/

│
├── server.py
│
└── templates/
    │
    ├── index.html
    │
    └── resultado.html
```

---

## 🎯 Objetivo del desafío

Crear un formulario que permita ingresar:

```text
Nombre del producto

Precio

Categoría
```

Por ejemplo:

```text
Producto:

Teclado Gamer

Precio:

35000

Categoría:

Periféricos
```

---

# 📋 Requisitos

### 1. Crear la ruta `/`

Debe mostrar el formulario.

---

### 2. Crear la ruta `/registrar`

Debe aceptar únicamente:

```text
POST
```

Por lo tanto deberá utilizar:

```python
methods=["POST"]
```

---

### 3. Obtener los datos

Utiliza:

```python
request.form
```

para obtener:

```text
nombre
precio
categoria
```

---

### 4. Mostrar la información en la terminal

Por ejemplo:

```text
============================

Producto recibido

Nombre: Teclado Gamer

Precio: 35000

Categoría: Periféricos

============================
```

---

### 5. Utilizar `redirect()`

Después de procesar los datos:

```python
return redirect("/resultado")
```

---

### 6. Crear `/resultado`

Esta ruta deberá ser de tipo:

```text
GET
```

y mostrar una página indicando:

```text
Producto registrado correctamente

La información fue procesada por el servidor.

[Volver al formulario]
```

---

# ⭐ Desafío adicional

Agrega una tercera ruta:

```text
/ayuda
```

que explique brevemente:

- Qué es una solicitud `POST`.
- Qué es una solicitud `GET`.
- Para qué sirve `redirect()`.
- Por qué `request.form` no está disponible después de la redirección.

Puedes crear una navegación sencilla:

```text
Inicio | Ayuda
```

utilizando:

```jinja
{{ url_for('index') }}
```

y:

```jinja
{{ url_for('ayuda') }}
```

---

# 🧠 Preguntas de reflexión

Antes de continuar con la siguiente lección, responde:

### 1.

¿Por qué no deberíamos renderizar directamente una plantilla después de procesar un formulario `POST`?

### 2.

¿Qué diferencia existe entre estas dos instrucciones?

```python
return render_template("resultado.html")
```

y:

```python
return redirect("/resultado")
```

### 3.

¿Por qué `request.form` está disponible en `/registrar`, pero no en `/resultado`?

### 4.

Si necesitamos mostrar en `/resultado` el nombre del producto enviado desde `/registrar`, ¿cómo podríamos conservar esa información?

---

# 🚧 El problema que queda pendiente

Ya sabemos utilizar:

```python
request.form
```

y ahora sabemos utilizar:

```python
redirect()
```

Pero aparece una nueva pregunta:

> **¿Cómo podemos conservar la información entre una solicitud y otra?**

Tenemos:

```text
POST
│
│ Datos
▼
/registrar
│
│
└── redirect()
       │
       ▼
      GET
       │
       ▼
/resultado
```

El problema es que los datos recibidos en `request.form` pertenecen a la primera solicitud.

Necesitamos algún mecanismo que permita **mantener información entre solicitudes**.

En las siguientes lecciones estudiaremos mecanismos de **persistencia de datos**, que permitirán resolver este problema.

---

# 📚 Conceptos aprendidos

| Concepto | Función |
|---|---|
| `request.form` | Obtener información enviada mediante un formulario POST |
| `redirect()` | Redirigir al navegador hacia otra ruta |
| `GET` | Solicitar/obtener una página o recurso |
| `POST` | Enviar información al servidor |
| `render_template()` | Renderizar una plantilla HTML |
| `@app.route()` | Definir una ruta |
| `methods=["POST"]` | Permitir solicitudes POST |
| `url_for()` | Generar automáticamente URLs de Flask |
| PRG | Patrón Post → Redirect → Get |

---

# 🏁 Resultado esperado

Al finalizar esta lección deberás comprender el siguiente flujo:

```text
                  FORMULARIO
                      │
                      │ POST
                      ▼
              /crear_usuario
                      │
                      │
              Procesar datos
                      │
                      ▼
                 redirect()
                      │
                      │ GET
                      ▼
              /mostrar_usuario
                      │
                      ▼
               mostrar.html
```

Y, sobre todo, recordar:

> **Después de procesar correctamente un `POST`, una práctica recomendada es redirigir al usuario hacia una ruta que responda mediante `GET`.**

La información del `POST` **no se conserva automáticamente** después de la redirección. Ese será precisamente el problema que resolveremos al estudiar la persistencia de datos.
Mostrando README.md