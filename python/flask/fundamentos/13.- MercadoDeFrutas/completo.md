# 🍎 Mercado de Frutas — Flask

Aplicación web desarrollada con **Flask, Jinja2, HTML, CSS y Bootstrap** que permite seleccionar frutas, generar una orden y visualizar un resumen de compra.

---

## 📁 Estructura completa del proyecto

```text
mercado_frutas_app/
│
├── app.py
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── frutas.html
│   └── checkout.html
│
└── static/
    │
    ├── css/
    │   └── style.css
    │
    └── images/
        ├── manzana.png
        ├── platano.png
        ├── naranja.png
        ├── fresa.png
        ├── uva.png
        ├── pina.png
        ├── sandia.png
        └── mango.png
```

---

# 🖼️ Imágenes requeridas

Las imágenes deben estar dentro de:

```text
static/images/
```

Utiliza estos nombres exactamente:

```text
manzana.png
platano.png
naranja.png
fresa.png
uva.png
pina.png
sandia.png
mango.png
```

## Recomendaciones

Para obtener una apariencia uniforme:

- Formato: `PNG`
- Tamaño recomendado: `500 × 500 px`
- Fondo: transparente
- Fruta centrada
- Proporción visual similar entre todas las imágenes

La aplicación utilizará CSS para mantener las imágenes dentro de un espacio uniforme sin deformarlas.

---

# 🐍 `app.py`

```python
# ==========================================================
# MERCADO DE FRUTAS
# Aplicación web desarrollada con Flask
# ==========================================================


# ----------------------------------------------------------
# IMPORTACIONES
# ----------------------------------------------------------

from flask import Flask, render_template, request


# ----------------------------------------------------------
# CREACIÓN DE LA APLICACIÓN
# ----------------------------------------------------------

app = Flask(__name__)


# ----------------------------------------------------------
# DATOS DE LAS FRUTAS
# ----------------------------------------------------------
#
# Por ahora utilizamos una lista de diccionarios.
#
# Cada diccionario representa una fruta.
#
# En una aplicación real estos datos podrían almacenarse
# posteriormente en una base de datos.
# ----------------------------------------------------------

frutas = [

    {
        "id": "manzana",
        "nombre": "Manzana",
        "precio": 2.5,
        "imagen": "manzana.png",
        "descripcion": (
            "Fruta dulce y crujiente, "
            "rica en fibra y vitamina C."
        )
    },

    {
        "id": "platano",
        "nombre": "Plátano",
        "precio": 1.8,
        "imagen": "platano.png",
        "descripcion": (
            "Fruta energética rica en potasio, "
            "perfecta para deportistas."
        )
    },

    {
        "id": "naranja",
        "nombre": "Naranja",
        "precio": 3.0,
        "imagen": "naranja.png",
        "descripcion": (
            "Cítrico jugoso con alto contenido "
            "de vitamina C y antioxidantes."
        )
    },

    {
        "id": "fresa",
        "nombre": "Fresa",
        "precio": 4.5,
        "imagen": "fresa.png",
        "descripcion": (
            "Baya dulce y aromática, rica "
            "en antioxidantes y vitamina C."
        )
    },

    {
        "id": "uva",
        "nombre": "Uva",
        "precio": 3.8,
        "imagen": "uva.png",
        "descripcion": (
            "Fruta pequeña y dulce, ideal "
            "para snacks y postres."
        )
    },

    {
        "id": "pina",
        "nombre": "Piña",
        "precio": 5.0,
        "imagen": "pina.png",
        "descripcion": (
            "Fruta tropical dulce y ácida, "
            "ideal para consumir fresca."
        )
    },

    {
        "id": "sandia",
        "nombre": "Sandía",
        "precio": 4.2,
        "imagen": "sandia.png",
        "descripcion": (
            "Fruta refrescante, ideal "
            "para los días de verano."
        )
    },

    {
        "id": "mango",
        "nombre": "Mango",
        "precio": 3.5,
        "imagen": "mango.png",
        "descripcion": (
            "Fruta tropical dulce y aromática, "
            "rica en vitaminas A y C."
        )
    }

]


# ----------------------------------------------------------
# RUTA PRINCIPAL
# ----------------------------------------------------------

@app.route("/")
def index():
    """
    Muestra la página principal.

    Envía la lista de frutas hacia index.html.
    """

    return render_template(
        "index.html",
        frutas=frutas
    )


# ----------------------------------------------------------
# RUTA DEL CATÁLOGO
# ----------------------------------------------------------

@app.route("/frutas")
def catalogo():
    """
    Muestra el catálogo de frutas.
    """

    return render_template(
        "frutas.html",
        frutas=frutas
    )


# ----------------------------------------------------------
# RUTA PARA PROCESAR LA ORDEN
# ----------------------------------------------------------

@app.route("/checkout", methods=["POST"])
def checkout():
    """
    Recibe los datos enviados desde el formulario.

    Esta ruta utiliza POST porque el usuario
    está enviando información al servidor.
    """

    # ------------------------------------------------------
    # DATOS DEL CLIENTE
    # ------------------------------------------------------

    nombre = request.form["nombre"]

    email = request.form["email"]

    direccion = request.form["direccion"]


    # ------------------------------------------------------
    # VARIABLES PARA CONSTRUIR EL PEDIDO
    # ------------------------------------------------------

    pedido = []

    total = 0

    total_frutas = 0


    # ------------------------------------------------------
    # RECORRER LAS FRUTAS
    # ------------------------------------------------------

    for fruta in frutas:

        # Los datos provenientes de un formulario
        # llegan como cadenas de texto.
        #
        # Por eso convertimos la cantidad a entero.

        cantidad = int(
            request.form[fruta["id"]]
        )


        # --------------------------------------------------
        # VERIFICAR SI LA FRUTA FUE SELECCIONADA
        # --------------------------------------------------

        if cantidad > 0:

            # Calcular subtotal de la fruta.

            subtotal = cantidad * fruta["precio"]


            # Agregar la fruta al pedido.

            pedido.append({

                "nombre": fruta["nombre"],

                "precio": fruta["precio"],

                "cantidad": cantidad,

                "subtotal": subtotal,

                "imagen": fruta["imagen"]

            })


            # Acumular dinero.

            total += subtotal


            # Acumular cantidad de frutas.

            total_frutas += cantidad


    # ------------------------------------------------------
    # ENVIAR INFORMACIÓN AL CHECKOUT
    # ------------------------------------------------------

    return render_template(

        "checkout.html",

        nombre=nombre,

        email=email,

        direccion=direccion,

        pedido=pedido,

        total=total,

        total_frutas=total_frutas

    )


# ----------------------------------------------------------
# EJECUTAR SERVIDOR
# ----------------------------------------------------------

if __name__ == "__main__":

    app.run(debug=True)
```

---

# 🔍 Análisis de `app.py`

## Lista de frutas

La información se encuentra en:

```python
frutas = [...]
```

Es una **lista de diccionarios**.

Cada fruta posee:

```python
{
    "id": "manzana",
    "nombre": "Manzana",
    "precio": 2.5,
    "imagen": "manzana.png",
    "descripcion": "..."
}
```

El `id` se utilizará para identificar el campo del formulario.

---

## Rutas

La aplicación tendrá tres rutas:

```text
/             → página principal

/frutas       → catálogo

/checkout     → procesamiento de la orden
```

Las primeras dos utilizan:

```python
render_template()
```

La tercera utiliza:

```python
request.form
```

para recibir la información enviada mediante `POST`.

---

## Procesamiento del formulario

La ruta:

```python
@app.route("/checkout", methods=["POST"])
```

solo acepta solicitudes `POST`.

Posteriormente:

```python
request.form["nombre"]
```

obtiene el valor enviado desde:

```html
name="nombre"
```

Lo mismo ocurre con:

```python
request.form["email"]
```

y:

```python
request.form["direccion"]
```

---

## Conversión de cantidades

Los formularios HTML entregan sus valores como texto.

Por eso:

```python
cantidad = int(
    request.form[fruta["id"]]
)
```

convierte, por ejemplo:

```text
"3"
```

en:

```python
3
```

Esto permite realizar operaciones matemáticas.

---

## Cálculo del subtotal

```python
subtotal = cantidad * fruta["precio"]
```

Ejemplo:

```text
2 manzanas × $2.50 = $5.00
```

---

## Cálculo del total

```python
total += subtotal
```

Cada subtotal se acumula en la variable `total`.

---

## Cálculo de la cantidad total

```python
total_frutas += cantidad
```

Permite mostrar posteriormente algo como:

```text
Total de frutas: 7
```

---

# 📚 Tecnologías utilizadas

| Tecnología | Uso |
|---|---|
| Python | Lógica de la aplicación |
| Flask | Servidor web |
| Jinja2 | Renderizado dinámico |
| HTML5 | Estructura |
| CSS3 | Diseño |
| Bootstrap | Componentes y responsive |
| PNG | Imágenes de productos |

---

# 📌 Estado de los archivos

En esta parte solamente se encuentra implementado:

```text
app.py
```

La estructura completa ya está definida para que el proyecto tenga una organización profesional.

Los siguientes archivos se completarán en las próximas partes:

```text
templates/
├── base.html
├── index.html
├── frutas.html
└── checkout.html

static/
└── css/
    └── style.css
```

---

# ➡️ PARTE 2

En la siguiente parte se entregarán **los códigos completos** de:

```text
templates/base.html
templates/index.html
```

Se implementará:

- Herencia de plantillas Jinja2.
- `url_for()`.
- Navbar.
- Bootstrap.
- Hero principal.
- Formulario `POST`.
- Tarjetas dinámicas de frutas.
- Selector de cantidades.
- Datos del cliente.
- Botón `Crear Orden`.
- Contenedor uniforme para las imágenes.

# 🍎 Mercado de Frutas — Flask

## 📦 PARTE 2/4 — Plantilla base y página principal

En esta parte se implementan las plantillas HTML principales de la aplicación.

Se utilizará **herencia de plantillas con Jinja2** para evitar repetir código común entre las diferentes páginas.

### Archivos implementados

```text
templates/
│
├── base.html
└── index.html
```

---

# 📁 Estructura del proyecto hasta este punto

```text
mercado_frutas_app/
│
├── app.py
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── frutas.html
│   └── checkout.html
│
└── static/
    │
    ├── css/
    │   └── style.css
    │
    └── images/
        ├── manzana.png
        ├── platano.png
        ├── naranja.png
        ├── fresa.png
        ├── uva.png
        ├── pina.png
        ├── sandia.png
        └── mango.png
```

> `frutas.html`, `checkout.html` y `style.css` ya forman parte de la estructura final, pero se completarán en las siguientes partes.

---

# 🧱 `templates/base.html`

Este archivo contiene los elementos comunes de todas las páginas:

- Configuración HTML.
- Bootstrap.
- Bootstrap Icons.
- Hoja de estilos.
- Barra de navegación.
- Footer.
- Bloques Jinja2.

```html
<!DOCTYPE html>
<html lang="es">

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>

        {% block title %}

        Mercado de Frutas

        {% endblock %}

    </title>


    <!-- ==================================================
         BOOTSTRAP
    =================================================== -->

    <link
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.7/dist/css/bootstrap.min.css"
        rel="stylesheet"
    >


    <!-- ==================================================
         BOOTSTRAP ICONS
    =================================================== -->

    <link
        rel="stylesheet"
        href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.13.1/font/bootstrap-icons.min.css"
    >


    <!-- ==================================================
         CSS PROPIO
    =================================================== -->

    <link
        rel="stylesheet"
        href="{{ url_for('static', filename='css/style.css') }}"
    >

</head>


<body>


    <!-- ==================================================
         BARRA DE NAVEGACIÓN
    =================================================== -->

    <nav class="navbar navbar-expand-lg navbar-dark bg-success">

        <div class="container">


            <!-- Logo / Nombre del sitio -->

            <a
                class="navbar-brand fw-bold"
                href="{{ url_for('index') }}"
            >

                <i class="bi bi-basket-fill"></i>

                Mercado de Frutas

            </a>


            <!-- Navegación -->

            <div class="d-flex align-items-center">


                <a
                    class="nav-link text-white me-3"
                    href="{{ url_for('index') }}"
                >

                    Inicio

                </a>


                <a
                    class="nav-link text-white"
                    href="{{ url_for('catalogo') }}"
                >

                    Frutas

                </a>


            </div>

        </div>

    </nav>


    <!-- ==================================================
         CONTENIDO PRINCIPAL
    =================================================== -->

    {% block content %}

    {% endblock %}


    <!-- ==================================================
         FOOTER
    =================================================== -->

    <footer class="bg-dark text-white text-center py-4 mt-5">

        <div class="container">

            <p class="mb-1">

                🍎 Mercado de Frutas

            </p>

            <small>

                Aplicación desarrollada con Flask y Jinja2.

            </small>

        </div>

    </footer>


    <!-- ==================================================
         BOOTSTRAP JAVASCRIPT
    =================================================== -->

    <script
        src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.7/dist/js/bootstrap.bundle.min.js"
    ></script>

</body>

</html>
```

---

# 🔍 Análisis de `base.html`

## `{% block title %}`

```jinja
{% block title %}

Mercado de Frutas

{% endblock %}
```

Este bloque permite que cada página pueda definir su propio título.

Por ejemplo, `index.html` podrá mostrar:

```text
Mercado de Frutas
```

mientras que `checkout.html` podrá mostrar:

```text
Resumen de la Orden
```

---

# 🧩 `{% block content %}`

```jinja
{% block content %}

{% endblock %}
```

Este es el espacio reservado para el contenido particular de cada página.

La estructura funciona así:

```text
base.html

├── <head>
├── Navbar
│
├── {% block content %}
│       ↑
│       │
│       └── Aquí entra index.html
│
└── Footer
```

De esta manera no necesitamos copiar el Navbar y Footer en cada HTML.

---

# 🔗 `url_for()` en la navegación

Por ejemplo:

```jinja
{{ url_for('index') }}
```

Flask busca:

```python
def index():
```

y genera automáticamente:

```text
/
```

Para el catálogo:

```jinja
{{ url_for('catalogo') }}
```

Flask encuentra:

```python
def catalogo():
```

y genera:

```text
/frutas
```

---

# 🎨 `url_for()` para CSS

También utilizamos:

```jinja
{{ url_for(
    'static',
    filename='css/style.css'
) }}
```

Flask genera:

```text
/static/css/style.css
```

Aquí `url_for()` no busca una función de nuestra aplicación.

La palabra:

```text
static
```

indica que queremos acceder a un archivo estático.

---

# 🏠 `templates/index.html`

Esta será la página principal de la aplicación.

Aquí el usuario podrá:

- Ver las frutas.
- Seleccionar cantidades.
- Ingresar sus datos.
- Enviar la orden.

```html
{% extends "base.html" %}


{% block title %}

Mercado de Frutas

{% endblock %}



{% block content %}


<!-- ==================================================
     HERO
=================================================== -->

<header class="hero text-center text-white">

    <div class="container">

        <h1 class="display-4 fw-bold">

            🍎 Mercado de Frutas

        </h1>

        <p class="lead">

            Frutas frescas y de calidad directamente
            hasta tu puerta.

        </p>

    </div>

</header>



<!-- ==================================================
     FORMULARIO PRINCIPAL
=================================================== -->

<form
    action="{{ url_for('checkout') }}"
    method="POST"
>


    <div class="container my-5">

        <div class="row g-4">


            <!-- ==================================================
                 PRODUCTOS
            =================================================== -->

            <div class="col-lg-8">

                <div class="card shadow border-0">


                    <div class="card-header bg-success text-white">

                        <h3 class="mb-0">

                            <i class="bi bi-basket-fill"></i>

                            Selecciona tus frutas

                        </h3>

                    </div>


                    <div class="card-body">

                        <div class="row g-4">


                            <!-- ==================================================
                                 RECORRER FRUTAS
                            =================================================== -->

                            {% for fruta in frutas %}


                            <div class="col-md-6">


                                <div class="card fruta-card h-100 shadow-sm">


                                    <!-- CONTENEDOR DE IMAGEN -->

                                    <div class="imagen-fruta">


                                        <img
                                            src="{{ url_for(
                                                'static',
                                                filename='images/' + fruta.imagen
                                            ) }}"
                                            alt="{{ fruta.nombre }}"
                                        >


                                    </div>


                                    <!-- INFORMACIÓN -->

                                    <div class="card-body">


                                        <h4 class="card-title">

                                            {{ fruta.nombre }}

                                        </h4>


                                        <h5 class="text-success fw-bold">

                                            ${{ "%.2f"|format(fruta.precio) }}

                                        </h5>


                                        <p class="card-text">

                                            {{ fruta.descripcion }}

                                        </p>


                                    </div>


                                    <!-- CANTIDAD -->

                                    <div class="card-footer bg-white border-0">


                                        <label
                                            for="{{ fruta.id }}"
                                            class="form-label fw-bold"
                                        >

                                            Cantidad

                                        </label>


                                        <input
                                            type="number"
                                            id="{{ fruta.id }}"
                                            name="{{ fruta.id }}"
                                            class="form-control"
                                            min="0"
                                            value="0"
                                        >


                                    </div>


                                </div>

                            </div>


                            {% endfor %}


                        </div>

                    </div>

                </div>

            </div>



            <!-- ==================================================
                 DATOS DEL CLIENTE
            =================================================== -->

            <div class="col-lg-4">


                <div class="card shadow border-0">


                    <div class="card-header bg-primary text-white">

                        <h3 class="mb-0">

                            <i class="bi bi-person-fill"></i>

                            Datos del Cliente

                        </h3>

                    </div>


                    <div class="card-body">


                        <!-- NOMBRE -->

                        <div class="mb-3">

                            <label
                                for="nombre"
                                class="form-label fw-bold"
                            >

                                Nombre

                            </label>


                            <input
                                type="text"
                                id="nombre"
                                name="nombre"
                                class="form-control"
                                placeholder="Ingresa tu nombre"
                                required
                            >

                        </div>



                        <!-- EMAIL -->

                        <div class="mb-3">

                            <label
                                for="email"
                                class="form-label fw-bold"
                            >

                                Correo electrónico

                            </label>


                            <input
                                type="email"
                                id="email"
                                name="email"
                                class="form-control"
                                placeholder="correo@ejemplo.com"
                                required
                            >

                        </div>



                        <!-- DIRECCIÓN -->

                        <div class="mb-4">

                            <label
                                for="direccion"
                                class="form-label fw-bold"
                            >

                                Dirección de entrega

                            </label>


                            <textarea
                                id="direccion"
                                name="direccion"
                                class="form-control"
                                rows="4"
                                placeholder="Ingresa tu dirección"
                                required
                            ></textarea>

                        </div>



                        <!-- SEPARADOR -->

                        <hr>



                        <!-- BOTÓN -->

                        <button
                            type="submit"
                            class="btn btn-success btn-lg w-100"
                        >

                            <i class="bi bi-cart-check-fill"></i>

                            Crear Orden

                        </button>


                    </div>

                </div>

            </div>


        </div>

    </div>


</form>


{% endblock %}
```

---

# 🔍 Análisis de `index.html`

## Herencia de plantillas

La primera instrucción es:

```jinja
{% extends "base.html" %}
```

Esto indica que `index.html` utilizará la estructura definida en:

```text
templates/base.html
```

No necesitamos volver a escribir:

```html
<!DOCTYPE html>
<html>
<head>
<body>
```

porque ya están en `base.html`.

---

# 🧩 Bloque `content`

Todo el contenido propio de esta página se encuentra entre:

```jinja
{% block content %}
```

y:

```jinja
{% endblock %}
```

Por lo tanto:

```text
base.html
│
├── Navbar
│
├── block content
│       │
│       └── index.html
│
└── Footer
```

---

# 🔄 Bucle Jinja2

Las frutas se generan mediante:

```jinja
{% for fruta in frutas %}
```

La variable:

```text
frutas
```

proviene de `app.py`:

```python
return render_template(
    "index.html",
    frutas=frutas
)
```

Cada elemento se almacena temporalmente en:

```text
fruta
```

Por ejemplo:

```jinja
{{ fruta.nombre }}
```

muestra:

```text
Manzana
```

---

# 🖼️ Imagen dinámica

La imagen se obtiene mediante:

```jinja
{{ url_for(
    'static',
    filename='images/' + fruta.imagen
) }}
```

Si:

```python
fruta["imagen"]
```

contiene:

```text
manzana.png
```

Flask genera:

```text
/static/images/manzana.png
```

Por lo tanto, no necesitamos escribir manualmente una ruta para cada fruta.

---

# 📐 Contenedor de imágenes

Cada imagen está dentro de:

```html
<div class="imagen-fruta">
```

Esto permitirá que nuestro CSS controle posteriormente:

- altura;
- ancho;
- alineación;
- espacio;
- proporción;
- efecto hover.

El objetivo es que todas las frutas ocupen un espacio visual similar.

---

# 🔢 Campo de cantidad

Cada fruta tiene:

```html
<input
    type="number"
    id="{{ fruta.id }}"
    name="{{ fruta.id }}"
    min="0"
    value="0"
>
```

Si la fruta es:

```python
{
    "id": "manzana",
    "nombre": "Manzana"
}
```

se genera:

```html
<input
    type="number"
    id="manzana"
    name="manzana"
>
```

Posteriormente Flask podrá recuperar:

```python
request.form["manzana"]
```

---

# 📤 Formulario POST

El formulario comienza con:

```html
<form
    action="{{ url_for('checkout') }}"
    method="POST"
>
```

Esto significa:

```text
Usuario completa formulario
            ↓
        Presiona botón
            ↓
          POST
            ↓
       /checkout
            ↓
     función checkout()
```

La función correspondiente en Flask es:

```python
@app.route("/checkout", methods=["POST"])
def checkout():
```

---

# 👤 Datos del cliente

Los campos utilizan:

```html
name="nombre"
```

```html
name="email"
```

```html
name="direccion"
```

Por lo tanto Flask podrá recibir:

```python
request.form["nombre"]
```

```python
request.form["email"]
```

```python
request.form["direccion"]
```

El atributo `name` es fundamental porque identifica cada dato enviado por el formulario.

---

# 🧠 Flujo de esta página

```text
app.py
   │
   │ frutas=frutas
   ▼
index.html
   │
   ├── {% for fruta in frutas %}
   │
   ├── nombre
   ├── precio
   ├── descripción
   ├── imagen
   └── cantidad
   │
   │
   ├── nombre del cliente
   ├── email
   └── dirección
   │
   ▼
<form method="POST">
   │
   ▼
/checkout
```

---

# ✅ Archivos completos de esta parte

Al finalizar esta parte tendremos:

```text
templates/
│
├── base.html      ✅
└── index.html     ✅
```

El proyecto ya cuenta con:

```text
app.py              ✅
base.html           ✅
index.html          ✅
```

Todavía quedan:

```text
frutas.html         ⏳
checkout.html       ⏳
style.css           ⏳
```

---

# ➡️ PARTE 3/4

La siguiente parte implementará:

```text
templates/checkout.html
```

y se centrará en mostrar la información procesada por Flask.

Se utilizarán:

- `pedido`
- `for`
- `if`
- `fruta.nombre`
- `fruta.precio`
- `fruta.cantidad`
- `fruta.subtotal`
- `total_frutas`
- `total`
- `nombre`
- `email`
- `direccion`

También se mostrará una alternativa visual para cuando el usuario no seleccione ninguna fruta.

# 🍎 Mercado de Frutas — Flask

## 📦 PARTE 3/4 — Procesamiento y resumen de la orden

En esta parte se completa la vista:

```text
templates/checkout.html
```

Esta página recibirá los datos procesados por Flask desde la ruta:

```text
/checkout
```

El objetivo es mostrar de manera clara:

- Datos del cliente.
- Frutas seleccionadas.
- Cantidad de cada fruta.
- Precio unitario.
- Subtotal.
- Cantidad total de frutas.
- Total de la compra.
- Imágenes de los productos.
- Opción para volver a realizar una compra.
- Opción para volver al catálogo.

---

# 📁 Estructura del proyecto

```text
mercado_frutas_app/
│
├── app.py
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── frutas.html
│   └── checkout.html
│
└── static/
    │
    ├── css/
    │   └── style.css
    │
    └── images/
        ├── manzana.png
        ├── platano.png
        ├── naranja.png
        ├── fresa.png
        ├── uva.png
        ├── pina.png
        ├── sandia.png
        └── mango.png
```

---

# 🧾 `templates/checkout.html`

Esta plantilla recibe los datos enviados desde:

```python
return render_template(
    "checkout.html",
    nombre=nombre,
    email=email,
    direccion=direccion,
    pedido=pedido,
    total=total,
    total_frutas=total_frutas
)
```

Por lo tanto, dentro de Jinja2 podremos utilizar directamente:

```text
nombre
email
direccion
pedido
total
total_frutas
```

---

## Código completo

```html
{% extends "base.html" %}


{% block title %}

Resumen de la Orden

{% endblock %}



{% block content %}


<!-- ==================================================
     ENCABEZADO
=================================================== -->

<header class="hero text-center text-white">

    <div class="container">

        <h1 class="display-5 fw-bold">

            🧾 Resumen de tu Compra

        </h1>

        <p class="lead">

            Revisa los productos seleccionados antes
            de finalizar tu pedido.

        </p>

    </div>

</header>



<!-- ==================================================
     CONTENIDO PRINCIPAL
=================================================== -->

<div class="container my-5">


    <div class="row g-4">


        <!-- ==================================================
             INFORMACIÓN DEL CLIENTE
        =================================================== -->

        <div class="col-lg-4">


            <div class="card shadow border-0 h-100">


                <div class="card-header bg-primary text-white">

                    <h3 class="mb-0">

                        <i class="bi bi-person-fill"></i>

                        Datos del Cliente

                    </h3>

                </div>


                <div class="card-body">


                    <!-- NOMBRE -->

                    <div class="mb-3">

                        <p class="mb-1 text-muted">

                            Nombre

                        </p>

                        <h5>

                            {{ nombre }}

                        </h5>

                    </div>


                    <!-- EMAIL -->

                    <div class="mb-3">

                        <p class="mb-1 text-muted">

                            Correo electrónico

                        </p>

                        <h5>

                            {{ email }}

                        </h5>

                    </div>


                    <!-- DIRECCIÓN -->

                    <div class="mb-3">

                        <p class="mb-1 text-muted">

                            Dirección de entrega

                        </p>

                        <h5>

                            {{ direccion }}

                        </h5>

                    </div>


                </div>

            </div>

        </div>



        <!-- ==================================================
             DETALLE DE LA ORDEN
        =================================================== -->

        <div class="col-lg-8">


            <div class="card shadow border-0">


                <div class="card-header bg-success text-white">

                    <h3 class="mb-0">

                        <i class="bi bi-cart-check-fill"></i>

                        Detalle de la Orden

                    </h3>

                </div>


                <div class="card-body">


                    <!-- ==================================================
                         VERIFICAR SI EXISTEN PRODUCTOS
                    =================================================== -->

                    {% if pedido %}


                    <!-- ==================================================
                         TABLA
                    =================================================== -->

                    <div class="table-responsive">


                        <table class="table table-hover align-middle">


                            <thead class="table-success">

                                <tr>

                                    <th>

                                        Producto

                                    </th>

                                    <th>

                                        Precio

                                    </th>

                                    <th>

                                        Cantidad

                                    </th>

                                    <th>

                                        Subtotal

                                    </th>

                                </tr>

                            </thead>


                            <tbody>


                                <!-- ==================================================
                                     RECORRER PEDIDO
                                =================================================== -->

                                {% for fruta in pedido %}


                                <tr>


                                    <!-- PRODUCTO -->

                                    <td>


                                        <div
                                            class="d-flex align-items-center gap-3"
                                        >


                                            <img

                                                src="{{ url_for(
                                                    'static',
                                                    filename='images/' + fruta.imagen
                                                ) }}"

                                                alt="{{ fruta.nombre }}"

                                                class="checkout-fruta"

                                            >


                                            <strong>

                                                {{ fruta.nombre }}

                                            </strong>


                                        </div>


                                    </td>


                                    <!-- PRECIO -->

                                    <td>

                                        ${{ "%.2f"|format(fruta.precio) }}

                                    </td>


                                    <!-- CANTIDAD -->

                                    <td>

                                        <span class="badge bg-secondary">

                                            {{ fruta.cantidad }}

                                        </span>

                                    </td>


                                    <!-- SUBTOTAL -->

                                    <td>

                                        <strong class="text-success">

                                            ${{ "%.2f"|format(fruta.subtotal) }}

                                        </strong>

                                    </td>


                                </tr>


                                {% endfor %}


                            </tbody>


                        </table>


                    </div>



                    <!-- ==================================================
                         RESUMEN
                    =================================================== -->

                    <div class="order-summary mt-4">


                        <div
                            class="d-flex justify-content-between mb-2"
                        >

                            <span>

                                Productos seleccionados:

                            </span>

                            <strong>

                                {{ pedido|length }}

                            </strong>

                        </div>


                        <div
                            class="d-flex justify-content-between mb-3"
                        >

                            <span>

                                Cantidad total de frutas:

                            </span>

                            <strong>

                                {{ total_frutas }}

                            </strong>

                        </div>


                        <hr>


                        <div
                            class="d-flex justify-content-between align-items-center"
                        >

                            <h4 class="mb-0">

                                Total a pagar

                            </h4>


                            <h2 class="text-success fw-bold mb-0">

                                ${{ "%.2f"|format(total) }}

                            </h2>

                        </div>


                    </div>


                    {% else %}


                    <!-- ==================================================
                         PEDIDO VACÍO
                    =================================================== -->

                    <div class="alert alert-warning text-center">


                        <i
                            class="bi bi-exclamation-triangle-fill fs-1"
                        ></i>


                        <h4 class="mt-3">

                            No seleccionaste ninguna fruta.

                        </h4>


                        <p>

                            Regresa al mercado para seleccionar
                            los productos que deseas comprar.

                        </p>


                    </div>


                    {% endif %}


                </div>

            </div>

        </div>


    </div>



    <!-- ==================================================
         BOTONES DE NAVEGACIÓN
    =================================================== -->

    <div class="text-center mt-5">


        <a
            href="{{ url_for('index') }}"
            class="btn btn-success btn-lg me-2"
        >

            <i class="bi bi-cart-plus-fill"></i>

            Nueva Compra

        </a>


        <a
            href="{{ url_for('catalogo') }}"
            class="btn btn-outline-primary btn-lg"
        >

            <i class="bi bi-images"></i>

            Ver Catálogo

        </a>


    </div>


</div>


{% endblock %}
```

---

# 🔍 Análisis de `checkout.html`

## 1. Herencia de plantilla

La primera línea es:

```jinja
{% extends "base.html" %}
```

Esto significa que `checkout.html` reutiliza toda la estructura de:

```text
base.html
```

Por lo tanto, automáticamente tendrá:

- Navbar.
- Bootstrap.
- Bootstrap Icons.
- CSS.
- Footer.

Solo necesitamos escribir el contenido específico del checkout.

---

# 🧩 2. Bloque `title`

```jinja
{% block title %}

Resumen de la Orden

{% endblock %}
```

Este contenido reemplaza el bloque:

```jinja
{% block title %}
```

que estaba definido en `base.html`.

Por lo tanto, el navegador mostrará:

```text
Resumen de la Orden
```

como título de la página.

---

# 📦 3. Recibir datos desde Flask

En `app.py` tenemos:

```python
return render_template(
    "checkout.html",
    nombre=nombre,
    email=email,
    direccion=direccion,
    pedido=pedido,
    total=total,
    total_frutas=total_frutas
)
```

Esto significa que Jinja2 recibe seis variables:

```text
nombre
email
direccion
pedido
total
total_frutas
```

Podemos utilizarlas directamente:

```jinja
{{ nombre }}
```

```jinja
{{ email }}
```

```jinja
{{ direccion }}
```

```jinja
{{ total }}
```

---

# 👤 4. Mostrar los datos del cliente

Por ejemplo:

```jinja
{{ nombre }}
```

mostrará el valor enviado desde:

```python
nombre = request.form["nombre"]
```

El flujo es:

```text
<input name="nombre">
        ↓
Formulario POST
        ↓
request.form["nombre"]
        ↓
nombre
        ↓
render_template()
        ↓
{{ nombre }}
```

---

# 🔄 5. Condicional `{% if pedido %}`

Utilizamos:

```jinja
{% if pedido %}
```

Esto permite verificar si existe información en el pedido.

Si contiene productos:

```text
pedido
 ↓
True
```

se muestra la tabla.

Si está vacío:

```text
pedido
 ↓
False
```

se muestra:

```text
No seleccionaste ninguna fruta.
```

---

# 🔁 6. Recorrer el pedido

La información del pedido es una lista.

Por eso podemos utilizar:

```jinja
{% for fruta in pedido %}
```

Cada elemento representa una fruta seleccionada.

Por ejemplo:

```python
{
    "nombre": "Manzana",
    "precio": 2.5,
    "cantidad": 2,
    "subtotal": 5.0,
    "imagen": "manzana.png"
}
```

Dentro del `for` podemos acceder a:

```jinja
{{ fruta.nombre }}
```

```jinja
{{ fruta.precio }}
```

```jinja
{{ fruta.cantidad }}
```

```jinja
{{ fruta.subtotal }}
```

```jinja
{{ fruta.imagen }}
```

---

# 🖼️ 7. Mostrar la imagen

La imagen se genera utilizando:

```jinja
{{ url_for(
    'static',
    filename='images/' + fruta.imagen
) }}
```

Si:

```text
fruta.imagen
```

contiene:

```text
manzana.png
```

Flask genera:

```text
/static/images/manzana.png
```

Esto permite reutilizar la misma imagen que se utilizó en el catálogo.

---

# 🔢 8. Mostrar la cantidad

Utilizamos:

```jinja
{{ fruta.cantidad }}
```

Por ejemplo:

```text
Manzana
Cantidad: 3
```

El valor proviene directamente de:

```python
cantidad = int(
    request.form[fruta["id"]]
)
```

---

# 💰 9. Mostrar el subtotal

Cada fruta tiene su propio subtotal:

```jinja
{{ fruta.subtotal }}
```

En Python se calculó mediante:

```python
subtotal = cantidad * fruta["precio"]
```

Por ejemplo:

```text
3 × $2.50 = $7.50
```

---

# 🔢 10. `pedido|length`

Esta expresión:

```jinja
{{ pedido|length }}
```

utiliza un **filtro de Jinja2**.

`length` permite conocer la cantidad de elementos de una colección.

Si:

```python
pedido = [
    manzana,
    platano,
    naranja
]
```

entonces:

```jinja
{{ pedido|length }}
```

produce:

```text
3
```

En este caso representa la cantidad de **productos diferentes seleccionados**.

---

# 🍎 11. `total_frutas`

Esta variable:

```jinja
{{ total_frutas }}
```

representa la cantidad total de unidades compradas.

Por ejemplo:

```text
2 manzanas
3 plátanos
1 naranja
```

Entonces:

```text
Productos diferentes: 3

Cantidad total de frutas: 6
```

Es importante distinguir ambos conceptos.

---

# 💵 12. Formatear precios

Para mostrar los precios utilizamos:

```jinja
{{ "%.2f"|format(fruta.precio) }}
```

Esto permite mostrar siempre dos decimales.

Por ejemplo:

```text
2.5
```

se mostrará como:

```text
2.50
```

Y:

```text
5
```

se mostrará como:

```text
5.00
```

---

# 🔗 13. Volver al formulario

El botón:

```jinja
<a
    href="{{ url_for('index') }}"
>
```

utiliza `url_for()`.

Flask busca:

```python
def index():
```

y genera:

```text
/
```

Por lo tanto, el usuario puede volver al formulario sin escribir manualmente:

```text
http://127.0.0.1:5000/
```

---

# 🖼️ 14. Visualización de las imágenes

Las imágenes del checkout utilizan:

```html
class="checkout-fruta"
```

Esto permitirá que posteriormente nuestro CSS controle su tamaño.

La idea es evitar que las imágenes originales tengan dimensiones diferentes y alteren el tamaño de las filas.

Por ejemplo:

```text
┌─────────────────────────────────────────┐
│ 🍎  Manzana     $2.50    2     $5.00   │
│                                         │
│ 🍌  Plátano     $1.80    3     $5.40   │
│                                         │
│ 🍊  Naranja     $3.00    1     $3.00   │
└─────────────────────────────────────────┘
```

---

# 🧠 Flujo completo hasta esta parte

```text
                       app.py
                         │
                         │
                  lista de frutas
                         │
                         ▼
                    index.html
                         │
                         │
                   Formulario
                         │
                         │ POST
                         ▼
                     /checkout
                         │
                         ▼
                  request.form
                         │
                         ▼
                    Procesamiento
                         │
              ┌──────────┴──────────┐
              │                     │
              ▼                     ▼
          subtotales              total
              │                     │
              └──────────┬──────────┘
                         │
                         ▼
                   checkout.html
                         │
              ┌──────────┴──────────┐
              │                     │
              ▼                     ▼
       Datos del cliente      Detalle del pedido
                                    │
                                    ▼
                             Total de la compra
```

---

# 📋 Ejemplo del resultado

Si el usuario selecciona:

```text
2 Manzanas
3 Plátanos
1 Naranja
```

la página deberá mostrar aproximadamente:

```text
┌──────────────────────────────────────────────────┐
│ 🧾 Resumen de tu Compra                          │
├────────────────────┬─────────────────────────────┤
│ Datos del Cliente  │ Detalle de la Orden         │
│                    │                             │
│ Nombre             │ 🍎 Manzana                  │
│ Dany               │ Precio: $2.50               │
│                    │ Cantidad: 2                 │
│ Correo             │ Subtotal: $5.00             │
│ dany@email.com     │                             │
│                    │ 🍌 Plátano                  │
│ Dirección          │ Precio: $1.80               │
│ Santiago           │ Cantidad: 3                 │
│                    │ Subtotal: $5.40             │
│                    │                             │
│                    │ 🍊 Naranja                  │
│                    │ Precio: $3.00               │
│                    │ Cantidad: 1                 │
│                    │ Subtotal: $3.00             │
│                    │                             │
│                    │ Total frutas: 6             │
│                    │                             │
│                    │ TOTAL: $13.40               │
└────────────────────┴─────────────────────────────┘
```

---

# 📚 Conceptos Jinja2 utilizados

| Elemento | Función |
|---|---|
| `{% extends %}` | Heredar una plantilla |
| `{% block %}` | Definir contenido de un bloque |
| `{{ variable }}` | Mostrar información |
| `{% if %}` | Evaluar una condición |
| `{% for %}` | Recorrer una colección |
| `|length` | Obtener cantidad de elementos |
| `|format()` | Formatear valores |
| `url_for()` | Generar rutas Flask |

---

# 📌 Archivos completados

Hasta este punto tenemos:

```text
app.py              ✅
templates/
├── base.html       ✅
├── index.html      ✅
└── checkout.html   ✅
```

Pendientes:

```text
templates/
└── frutas.html     ⏳

static/
└── css/
    └── style.css   ⏳
```

---

# ➡️ PARTE 4/4

La última parte completará:

```text
templates/frutas.html
static/css/style.css
```

También dejará definida la presentación visual final:

- Catálogo de frutas.
- Tarjetas uniformes.
- Imágenes centradas.
- Imágenes sin deformación.
- Efectos `hover`.
- Responsive.
- Navbar.
- Footer.
- Checkout.
- Botones.
- Tablas.
- Formularios.
- Adaptación para pantallas pequeñas.

Al finalizar esa parte, el proyecto estará **completo y ejecutable**.




# 🍎 Mercado de Frutas — Flask

## 📦 PARTE 4/4 — Catálogo, CSS y versión final

En esta última parte se completan los archivos:

```text
templates/frutas.html
static/css/style.css
```

Con esto quedará terminada la aplicación.

La interfaz incorporará:

- Catálogo de frutas.
- Imágenes uniformes.
- Diseño responsive.
- Tarjetas de productos.
- Efectos `hover`.
- Formularios.
- Tabla del checkout.
- Navbar.
- Footer.
- Botones.
- Adaptación para dispositivos móviles.

---

# 📁 Estructura final

```text
mercado_frutas_app/
│
├── app.py
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── frutas.html
│   └── checkout.html
│
└── static/
    │
    ├── css/
    │   └── style.css
    │
    └── images/
        ├── manzana.png
        ├── platano.png
        ├── naranja.png
        ├── fresa.png
        ├── uva.png
        ├── pina.png
        ├── sandia.png
        └── mango.png
```

---

# 🍓 `templates/frutas.html`

Esta página mostrará todas las frutas disponibles en forma de catálogo.

Los datos provienen de:

```python
return render_template(
    "frutas.html",
    frutas=frutas
)
```

Por lo tanto, podemos utilizar Jinja2 para recorrer la lista.

## Código completo

```html
{% extends "base.html" %}


{% block title %}

Catálogo de Frutas

{% endblock %}



{% block content %}


<!-- ==================================================
     ENCABEZADO
=================================================== -->

<header class="hero text-center text-white">

    <div class="container">

        <h1 class="display-5 fw-bold">

            🍎 Catálogo de Frutas

        </h1>

        <p class="lead">

            Descubre nuestras frutas frescas disponibles.

        </p>

    </div>

</header>



<!-- ==================================================
     CATÁLOGO
=================================================== -->

<div class="container my-5">


    <div class="row g-4">


        <!-- ==================================================
             RECORRER FRUTAS
        =================================================== -->

        {% for fruta in frutas %}


        <div class="col-lg-3 col-md-4 col-sm-6">


            <div class="card fruta-card h-100 shadow-sm">


                <!-- ==================================================
                     IMAGEN
                =================================================== -->

                <div class="imagen-fruta">


                    <img

                        src="{{ url_for(
                            'static',
                            filename='images/' + fruta.imagen
                        ) }}"

                        alt="{{ fruta.nombre }}"

                    >


                </div>



                <!-- ==================================================
                     INFORMACIÓN
                =================================================== -->

                <div class="card-body text-center">


                    <h4 class="card-title">

                        {{ fruta.nombre }}

                    </h4>


                    <h5 class="text-success fw-bold">

                        ${{ "%.2f"|format(fruta.precio) }}

                    </h5>


                    <p class="card-text">

                        {{ fruta.descripcion }}

                    </p>


                </div>



                <!-- ==================================================
                     FOOTER DE LA TARJETA
                =================================================== -->

                <div class="card-footer bg-white border-0 text-center pb-4">


                    <a
                        href="{{ url_for('index') }}"
                        class="btn btn-success"
                    >

                        <i class="bi bi-cart-plus-fill"></i>

                        Comprar

                    </a>


                </div>


            </div>


        </div>


        {% endfor %}


    </div>


</div>



<!-- ==================================================
     BOTÓN INFERIOR
=================================================== -->

<div class="container text-center mb-5">


    <a
        href="{{ url_for('index') }}"
        class="btn btn-success btn-lg"
    >

        <i class="bi bi-cart-fill"></i>

        Realizar una Compra

    </a>


</div>


{% endblock %}
```

---

# 🔍 Análisis de `frutas.html`

## Herencia

Al igual que las demás páginas:

```jinja
{% extends "base.html" %}
```

permite reutilizar:

```text
base.html
```

Por lo tanto no necesitamos repetir:

- `<!DOCTYPE html>`
- `<head>`
- Bootstrap
- CSS
- Navbar
- Footer

---

# 🔄 Recorrer las frutas

Utilizamos:

```jinja
{% for fruta in frutas %}
```

La lista viene desde Flask:

```python
return render_template(
    "frutas.html",
    frutas=frutas
)
```

Cada fruta se transforma automáticamente en una tarjeta.

---

# 🖼️ Imagen dinámica

Utilizamos:

```jinja
{{ url_for(
    'static',
    filename='images/' + fruta.imagen
) }}
```

Por ejemplo:

```text
fruta.imagen
```

puede contener:

```text
manzana.png
```

Entonces Flask genera:

```text
/static/images/manzana.png
```

---

# 💰 Precio

El precio se muestra mediante:

```jinja
{{ "%.2f"|format(fruta.precio) }}
```

Esto permite mostrar siempre dos decimales.

Por ejemplo:

```text
2.5
```

se muestra como:

```text
2.50
```

---

# 🛒 Botón comprar

El botón utiliza:

```jinja
{{ url_for('index') }}
```

Esto genera:

```text
/
```

Por lo tanto, al seleccionar:

```text
Comprar
```

el usuario vuelve al formulario principal.

---

# 🎨 `static/css/style.css`

Este archivo contiene los estilos visuales de toda la aplicación.

Será utilizado por:

```text
index.html
frutas.html
checkout.html
```

mediante:

```jinja
{{ url_for(
    'static',
    filename='css/style.css'
) }}
```

---

# 📄 Código completo de `style.css`

```css
/* ==========================================================
   MERCADO DE FRUTAS
   Hoja de estilos principal
========================================================== */


/* ==========================================================
   VARIABLES
========================================================== */

:root {

    --color-principal: #198754;

    --color-principal-hover: #157347;

    --color-fondo: #f4f6f8;

    --color-texto: #333;

    --color-blanco: #ffffff;

}


/* ==========================================================
   ESTILOS GENERALES
========================================================== */

body {

    font-family: Arial, Helvetica, sans-serif;

    background-color: var(--color-fondo);

    color: var(--color-texto);

    margin: 0;

}


/* ==========================================================
   NAVBAR
========================================================== */

.navbar {

    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);

}


.navbar-brand {

    font-size: 1.4rem;

}


.nav-link {

    transition: 0.2s ease;

}


.nav-link:hover {

    opacity: 0.8;

}


/* ==========================================================
   HERO
========================================================== */

.hero {

    background: linear-gradient(
        135deg,
        #198754,
        #157347
    );

    padding: 70px 20px;

}


.hero h1 {

    font-weight: bold;

}


.hero p {

    font-size: 20px;

}


/* ==========================================================
   TARJETAS GENERALES
========================================================== */

.card {

    border: none;

    border-radius: 15px;

    overflow: hidden;

}


.card-header {

    font-weight: bold;

}


.card-footer {

    border-top: none;

}


/* ==========================================================
   TARJETAS DE FRUTAS
========================================================== */

.fruta-card {

    transition: transform 0.3s ease,
                box-shadow 0.3s ease;

}


.fruta-card:hover {

    transform: translateY(-8px);

    box-shadow:
        0 15px 30px rgba(0, 0, 0, 0.15);

}


/* ==========================================================
   CONTENEDOR DE IMÁGENES
========================================================== */

/*
   Todas las frutas utilizan el mismo espacio.

   Esto evita que una imagen grande deforme
   el tamaño de la tarjeta.
*/

.imagen-fruta {

    width: 100%;

    height: 230px;

    display: flex;

    justify-content: center;

    align-items: center;

    background-color: #ffffff;

    padding: 20px;

    overflow: hidden;

}


/* ==========================================================
   IMÁGENES DE FRUTAS
========================================================== */

.imagen-fruta img {

    max-width: 85%;

    max-height: 190px;

    width: auto;

    height: auto;

    object-fit: contain;

    transition: transform 0.3s ease;

}


/* ==========================================================
   EFECTO HOVER DE IMÁGENES
========================================================== */

.fruta-card:hover .imagen-fruta img {

    transform: scale(1.08);

}


/* ==========================================================
   INFORMACIÓN DE PRODUCTOS
========================================================== */

.card-title {

    font-weight: bold;

}


.card-text {

    color: #666;

    font-size: 15px;

    line-height: 1.5;

}


/* ==========================================================
   FORMULARIOS
========================================================== */

.form-control {

    border-radius: 8px;

    padding: 10px;

}


.form-control:focus {

    border-color: var(--color-principal);

    box-shadow:
        0 0 0 0.2rem rgba(25, 135, 84, 0.15);

}


/* ==========================================================
   INPUTS DE CANTIDAD
========================================================== */

input[type="number"] {

    text-align: center;

}


/* ==========================================================
   BOTONES
========================================================== */

.btn {

    border-radius: 10px;

    transition:
        transform 0.2s ease,
        box-shadow 0.2s ease;

}


.btn:hover {

    transform: translateY(-2px);

}


/* ==========================================================
   TABLAS
========================================================== */

.table {

    margin-bottom: 0;

}


.table thead {

    font-size: 15px;

}


.table tbody tr {

    transition: background-color 0.2s ease;

}


.table tbody tr:hover {

    background-color: #f3fff7;

}


/* ==========================================================
   IMÁGENES DEL CHECKOUT
========================================================== */

.checkout-fruta {

    width: 60px;

    height: 60px;

    object-fit: contain;

    border-radius: 10px;

    background-color: #ffffff;

    padding: 5px;

}


/* ==========================================================
   RESUMEN DEL PEDIDO
========================================================== */

.order-summary {

    background-color: #f8f9fa;

    border-radius: 12px;

    padding: 20px;

}


/* ==========================================================
   ALERTAS
========================================================== */

.alert {

    border-radius: 12px;

}


/* ==========================================================
   BADGES
========================================================== */

.badge {

    font-size: 13px;

    padding: 8px 12px;

}


/* ==========================================================
   FOOTER
========================================================== */

footer {

    margin-top: 80px;

}


/* ==========================================================
   RESPONSIVE — TABLETS
========================================================== */

@media (max-width: 992px) {


    .hero {

        padding: 55px 20px;

    }


    .hero h1 {

        font-size: 36px;

    }


}


/* ==========================================================
   RESPONSIVE — CELULARES
========================================================== */

@media (max-width: 768px) {


    .hero {

        padding: 45px 15px;

    }


    .hero h1 {

        font-size: 30px;

    }


    .hero p {

        font-size: 17px;

    }


    .imagen-fruta {

        height: 210px;

    }


    .imagen-fruta img {

        max-height: 170px;

    }


}


/* ==========================================================
   RESPONSIVE — CELULARES PEQUEÑOS
========================================================== */

@media (max-width: 576px) {


    .hero {

        padding: 40px 15px;

    }


    .hero h1 {

        font-size: 26px;

    }


    .hero p {

        font-size: 16px;

    }


    .navbar-brand {

        font-size: 1.15rem;

    }


    .imagen-fruta {

        height: 200px;

    }


    .imagen-fruta img {

        max-width: 80%;

        max-height: 160px;

    }


    .btn-lg {

        width: 100%;

        margin-bottom: 10px;

    }


}
```

---

# 🔍 Análisis del CSS

## 1. Contenedor de imágenes

Una de las partes más importantes es:

```css
.imagen-fruta {

    width: 100%;

    height: 230px;

    display: flex;

    justify-content: center;

    align-items: center;

}
```

Esto crea un espacio fijo para todas las imágenes.

Visualmente:

```text
┌──────────────────────────┐
│                          │
│          🍎              │
│                          │
└──────────────────────────┘
```

Todas las frutas disponen del mismo espacio.

---

# 📐 2. `max-width`

Utilizamos:

```css
max-width: 85%;
```

Esto impide que una imagen ocupe todo el ancho de la tarjeta.

---

# 📏 3. `max-height`

También utilizamos:

```css
max-height: 190px;
```

Esto impide que una imagen sea demasiado alta.

---

# 🖼️ 4. `object-fit: contain`

Utilizamos:

```css
object-fit: contain;
```

Su objetivo es mantener la proporción original de la imagen.

La imagen no se deforma.

Por ejemplo:

```text
❌ Incorrecto

🍌 → estirada


✅ Correcto

🍌 → mantiene sus proporciones
```

---

# 🎯 5. Centrado de las imágenes

Utilizamos:

```css
display: flex;

justify-content: center;

align-items: center;
```

Esto permite centrar la imagen:

```text
horizontalmente
      +
verticalmente
```

dentro del contenedor.

---

# ✨ 6. Efecto `hover`

Cuando el usuario pasa el mouse sobre una tarjeta:

```css
.fruta-card:hover
```

la tarjeta se eleva:

```css
transform: translateY(-8px);
```

Y la imagen aumenta ligeramente:

```css
transform: scale(1.08);
```

Esto genera una interacción visual sencilla sin necesidad de JavaScript.

---

# 📱 7. Responsive

Se utilizaron `media queries`:

```css
@media (max-width: 768px)
```

y:

```css
@media (max-width: 576px)
```

Esto permite adaptar la aplicación a:

- computadores;
- tablets;
- celulares.

Por ejemplo, en escritorio podemos mostrar varias tarjetas:

```text
┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐
│ 🍎    │ │ 🍌    │ │ 🍊    │ │ 🍓    │
└───────┘ └───────┘ └───────┘ └───────┘
```

Mientras que en una pantalla pequeña:

```text
┌───────────────┐
│      🍎       │
└───────────────┘

┌───────────────┐
│      🍌       │
└───────────────┘
```

---

# 🔗 8. Relación entre Flask, Jinja2 y CSS

La aplicación completa funciona de esta manera:

```text
                    app.py
                      │
                      │
              Lista de frutas
                      │
          ┌───────────┼───────────┐
          │           │           │
          ▼           ▼           ▼
         /          /frutas    /checkout
          │           │           │
          ▼           ▼           ▼
      index.html  frutas.html  checkout.html
          │           │           │
          └───────────┼───────────┘
                      │
                      ▼
                  base.html
                      │
                      ▼
                style.css
                      │
                      ▼
                  Navegador
```

---

# 🧠 Conceptos integrados

La actividad completa reúne los siguientes contenidos:

| Concepto | Aplicación |
|---|---|
| Flask | Servidor web |
| `@app.route()` | Creación de rutas |
| `render_template()` | Renderizar HTML |
| `request.form` | Recibir formularios |
| `POST` | Enviar información |
| Jinja2 | Datos dinámicos |
| `{% for %}` | Recorrer frutas |
| `{% if %}` | Comprobar condiciones |
| `{{ variable }}` | Mostrar datos |
| `url_for()` | Generar rutas |
| `extends` | Herencia de plantillas |
| `block` | Contenido dinámico |
| `int()` | Conversión de datos |
| Listas | Colección de frutas |
| Diccionarios | Información de productos |
| CSS | Diseño |
| Bootstrap | Componentes visuales |
| Media Queries | Responsive |
| Static | CSS e imágenes |

---

# 🧪 Rutas disponibles

Con el servidor ejecutándose:

```bash
python app.py
```

se pueden probar las siguientes rutas.

### 🏠 Página principal

```text
http://127.0.0.1:5000/
```

Permite seleccionar frutas y enviar una orden.

---

### 🍎 Catálogo

```text
http://127.0.0.1:5000/frutas
```

Muestra todas las frutas disponibles.

---

### 🧾 Checkout

La ruta:

```text
/checkout
```

se utiliza mediante `POST`.

No debe accederse directamente desde el navegador como una ruta GET.

El flujo correcto es:

```text
/
 ↓
Formulario
 ↓
POST /checkout
 ↓
Resumen de compra
```

---

# ✅ Resultado final esperado

La aplicación debe permitir:

```text
                 MERCADO DE FRUTAS
                         │
          ┌──────────────┴──────────────┐
          │                             │
          ▼                             ▼
       Comprar                       Catálogo
          │                             │
          ▼                             ▼
       Formulario                    Frutas
          │
          │ POST
          ▼
       Checkout
          │
          ▼
    Resumen de orden
```

El usuario podrá:

- seleccionar cantidades;
- ingresar nombre;
- ingresar correo;
- ingresar dirección;
- crear una orden;
- visualizar las frutas seleccionadas;
- revisar subtotales;
- revisar la cantidad total de frutas;
- revisar el total a pagar;
- volver al formulario;
- acceder al catálogo.

---

# 🏁 Proyecto terminado

La estructura final debe quedar:

```text
mercado_frutas_app/
│
├── app.py
│
├── templates/
│   │
│   ├── base.html
│   ├── index.html
│   ├── frutas.html
│   └── checkout.html
│
└── static/
    │
    ├── css/
    │   └── style.css
    │
    └── images/
        │
        ├── manzana.png
        ├── platano.png
        ├── naranja.png
        ├── fresa.png
        ├── uva.png
        ├── pina.png
        ├── sandia.png
        └── mango.png
```

---

# 💡 Pregunta guía

> ¿Qué estrategia implementarías para guardar las órdenes realizadas por los usuarios y permitir que posteriormente puedan consultar su historial de compras?

Actualmente la orden existe solamente durante la solicitud.

Si el usuario recarga la página o cierra el navegador, la información no queda almacenada.

Una solución futura podría utilizar:

```text
Flask
   ↓
Base de datos
   ↓
Usuarios
   ↓
Órdenes
   ↓
Detalle de órdenes
   ↓
Productos
```

Esto permitiría evolucionar este proyecto desde una práctica con datos temporales hacia una aplicación de comercio electrónico con persistencia de información.
Mostrando completo.md