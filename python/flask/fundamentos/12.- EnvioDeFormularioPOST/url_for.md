# 📚 ¿Cómo funciona `url_for()`?

A medida que nuestras aplicaciones crecen, comenzamos a navegar entre distintas páginas, cargar hojas de estilo, imágenes y archivos JavaScript.

Flask ofrece una función llamada **`url_for()`**, cuya principal función es **generar automáticamente las rutas (URL) de nuestra aplicación**.

En lugar de escribir las rutas manualmente, Flask las construye por nosotros.

---

# 🎯 ¿Por qué utilizar `url_for()`?

Supongamos que tenemos la siguiente ruta.

```python
@app.route("/")
def index():

    return render_template("index.html")
```

Podríamos crear un enlace así.

```html
<a href="/">Inicio</a>
```

Funciona.

Pero ahora imagina que decides cambiar la ruta.

```python
@app.route("/inicio")
def index():
```

Ahora todos los enlaces escritos manualmente dejarán de funcionar.

Tendrías que buscarlos y modificarlos uno por uno.

---

## La solución

En lugar de escribir la ruta manualmente, Flask puede construirla automáticamente.

```html
<a href="{{ url_for('index') }}">
    Inicio
</a>
```

Flask revisa todas las rutas registradas y busca una función llamada:

```python
def index():
```

Como esa función está asociada a:

```python
@app.route("/")
```

Flask genera automáticamente.

```text
/
```

Si más adelante cambiamos la ruta.

```python
@app.route("/inicio")
```

No será necesario modificar el HTML.

Flask ahora generará automáticamente.

```text
/inicio
```

---

# 🔍 ¿Qué recibe `url_for()`?

La función recibe el **nombre de la función**, **NO la URL**.

Por ejemplo.

```python
@app.route("/usuarios")
def mostrar_usuarios():
```

La función se llama:

```python
mostrar_usuarios
```

Entonces escribimos.

```jinja
{{ url_for('mostrar_usuarios') }}
```

Flask genera.

```text
/usuarios
```

---

# 📌 Ejemplo completo

Servidor.

```python
@app.route("/")
def index():

    return render_template("index.html")


@app.route("/contacto")
def contacto():

    return render_template("contacto.html")
```

HTML.

```html
<nav>

    <a href="{{ url_for('index') }}">

        Inicio

    </a>

    <a href="{{ url_for('contacto') }}">

        Contacto

    </a>

</nav>
```

Resultado generado por Flask.

```html
<a href="/">Inicio</a>

<a href="/contacto">Contacto</a>
```

---

# 🖼️ `url_for()` con archivos estáticos

`url_for()` también se utiliza para cargar archivos CSS, JavaScript e imágenes.

En este caso **no recibe el nombre de una función**.

Recibe la palabra reservada:

```python
static
```

---

## CSS

```html
<link
rel="stylesheet"
href="{{ url_for('static', filename='css/style.css') }}">
```

Flask genera.

```text
/static/css/style.css
```

---

## JavaScript

```html
<script
src="{{ url_for('static', filename='js/script.js') }}">
</script>
```

Resultado.

```text
/static/js/script.js
```

---

## Imagen

```html
<img
src="{{ url_for('static', filename='img/python.png') }}">
```

Resultado.

```text
/static/img/python.png
```

---

# 🧠 ¿Cómo sabe Flask qué ruta generar?

Cuando ejecutamos la aplicación.

```python
@app.route("/")
def index():
```

Flask registra internamente una relación similar a esta.

| Función | Ruta |
|----------|------|
| index | / |

---

Otro ejemplo.

```python
@app.route("/tabla")
def mostrar_tabla():
```

Flask registra.

| Función | Ruta |
|----------|------|
| mostrar_tabla | /tabla |

Cuando escribimos.

```jinja
{{ url_for('mostrar_tabla') }}
```

Flask busca la función.

```
mostrar_tabla
```

y responde.

```
/tabla
```

---

# 🚀 Flujo de funcionamiento

```text
url_for("index")

        │

        ▼

Busca una función llamada

index()

        │

        ▼

Encuentra

@app.route("/")

        │

        ▼

Genera

/
```

---

# ⚠️ Error común

Muchos principiantes escriben.

```jinja
{{ url_for('/') }}
```

❌ Incorrecto.

Porque `url_for()` **no recibe una URL**.

Debe recibir el nombre de la función.

Correcto.

```jinja
{{ url_for('index') }}
```

---

# 💡 Regla fácil de recordar

Cuando quieras navegar entre páginas:

```jinja
url_for("nombre_de_la_función")
```

Cuando quieras cargar archivos estáticos:

```jinja
url_for("static", filename="ruta/del/archivo")
```

---

# 🏁 Resumen

| ¿Qué quiero hacer? | Código |
|--------------------|--------|
| Ir a otra página | `url_for('index')` |
| Ir a la ruta `/usuarios` | `url_for('mostrar_usuarios')` |
| Cargar un CSS | `url_for('static', filename='css/style.css')` |
| Cargar un JS | `url_for('static', filename='js/script.js')` |
| Cargar una imagen | `url_for('static', filename='img/logo.png')` |

> **Recuerda:** `url_for()` nunca recibe una URL como parámetro. Siempre recibe el **nombre de la función** (para rutas) o la palabra reservada **`static`** (para archivos estáticos). Gracias a esto, si las rutas cambian en el futuro, Flask actualizará automáticamente todos los enlaces generados con `url_for()`.
Mostrando url_for.md