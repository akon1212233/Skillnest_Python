# 🎯 Adivina el Número — Flask + Session

> **Curso:** Desarrollo Web con Flask desde Cero  
> **Práctica:** Adivina el Número  
> **Nivel:** Core + funcionalidades complementarias  
> **Tecnologías:** Python · Flask · Jinja2 · HTML5 · CSS3

---

# 📖 Descripción

En esta práctica construiremos un pequeño juego web utilizando **Flask** y **sesiones**.

La aplicación generará un número secreto entre **1 y 10** y permitirá que el usuario intente descubrirlo.

El número secreto permanecerá almacenado en la sesión, por lo que no cambiará mientras el usuario continúe jugando.

Cada intento permitirá entregar retroalimentación:

- El número ingresado es menor.
- El número ingresado es mayor.
- El número ingresado es correcto.

Además, se contará la cantidad de intentos realizados y existirá una opción para reiniciar completamente el juego.

La interfaz estará diseñada para parecerse a la referencia entregada, incorporando:

- Indicaciones visuales.
- Botones rápidos del `1` al `10`.
- Campo numérico.
- Botón **Adivinar**.
- Botón **Reiniciar Juego**.
- Mensajes dinámicos.
- Contador de intentos.
- Sección de reglas.

---

# 🎯 Objetivos

Al finalizar esta práctica deberás ser capaz de:

- Utilizar `session` en Flask.
- Configurar `app.secret_key`.
- Inicializar información dentro de una sesión.
- Recuperar información desde `session`.
- Modificar valores almacenados en sesión.
- Eliminar la sesión con `session.clear()`.
- Generar números aleatorios con `random.randint()`.
- Procesar formularios utilizando `POST`.
- Utilizar `request.form`.
- Convertir datos recibidos desde HTML utilizando `int()`.
- Utilizar `redirect()` después de procesar un formulario.
- Enviar información dinámica hacia Jinja2.
- Mostrar mensajes diferentes utilizando `if`.
- Construir una interfaz interactiva con HTML y CSS.

---

# 📁 Estructura del proyecto

```text
adivina_numero/
│
├── server.py
│
├── templates/
│   └── index.html
│
└── static/
    └── style.css
```

---

# 🧠 Funcionamiento general

El juego seguirá este flujo:

```text
Usuario
   │
   ▼
GET /
   │
   ▼
¿Existe número secreto?
   │
   ├── NO → Generar número aleatorio
   │
   └── SÍ → Recuperar número existente
   │
   ▼
Mostrar formulario
   │
   │
   │ POST
   ▼
/adivinar
   │
   ▼
request.form
   │
   ▼
Convertir a int
   │
   ▼
Comparar con número secreto
   │
   ├── Menor
   ├── Mayor
   └── Correcto
   │
   ▼
Guardar información en session
   │
   ▼
redirect("/")
   │
   ▼
GET /
   │
   ▼
Mostrar resultado
```

---

# 🐍 `server.py`

Este archivo contiene toda la lógica del juego.

```python
# ==========================================================
# ADIVINA EL NÚMERO
# Juego desarrollado con Flask
# ==========================================================


# ----------------------------------------------------------
# IMPORTACIONES
# ----------------------------------------------------------

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session
)

import random


# ----------------------------------------------------------
# CREAR APLICACIÓN
# ----------------------------------------------------------

app = Flask(__name__)


# ----------------------------------------------------------
# SECRET KEY
# ----------------------------------------------------------
#
# Flask necesita una clave secreta para utilizar session.
#
# Esta clave permite firmar y proteger la información
# relacionada con la sesión del usuario.
#
# En una aplicación real debe mantenerse fuera del código
# fuente, por ejemplo utilizando variables de entorno.
#
# Para esta práctica utilizaremos una clave sencilla.
# ----------------------------------------------------------

app.secret_key = "clave-secreta-adivina-numero"


# ----------------------------------------------------------
# RUTA PRINCIPAL
# ----------------------------------------------------------

@app.route("/")
def index():
    """
    Muestra la página principal del juego.

    Si todavía no existe un número secreto dentro
    de la sesión, lo generamos aleatoriamente.

    También inicializamos la cantidad de intentos
    y un mensaje para el usuario.
    """

    # ------------------------------------------------------
    # INICIALIZAR NÚMERO SECRETO
    # ------------------------------------------------------

    if "numero_secreto" not in session:

        session["numero_secreto"] = random.randint(1, 10)


    # ------------------------------------------------------
    # INICIALIZAR INTENTOS
    # ------------------------------------------------------

    if "intentos" not in session:

        session["intentos"] = 0


    # ------------------------------------------------------
    # INICIALIZAR MENSAJE
    # ------------------------------------------------------

    if "mensaje" not in session:

        session["mensaje"] = (
            "Adivina un número entre 1 y 10."
        )


    # ------------------------------------------------------
    # INICIALIZAR ESTADO DEL JUEGO
    # ------------------------------------------------------

    if "resultado" not in session:

        session["resultado"] = ""


    # ------------------------------------------------------
    # ENVIAR INFORMACIÓN A LA PLANTILLA
    # ------------------------------------------------------

    mensaje = session["mensaje"]

    resultado = session["resultado"]

    intentos = session["intentos"]


    # ------------------------------------------------------
    # MOSTRAR PÁGINA
    # ------------------------------------------------------

    return render_template(
        "index.html",
        mensaje=mensaje,
        resultado=resultado,
        intentos=intentos
    )


# ----------------------------------------------------------
# PROCESAR INTENTO
# ----------------------------------------------------------

@app.route("/adivinar", methods=["POST"])
def adivinar():
    """
    Procesa el número ingresado por el usuario
    y lo compara con el número secreto.
    """

    # ------------------------------------------------------
    # RECIBIR DATO DEL FORMULARIO
    # ------------------------------------------------------

    numero = int(request.form["numero"])


    # ------------------------------------------------------
    # OBTENER NÚMERO SECRETO
    # ------------------------------------------------------

    numero_secreto = session["numero_secreto"]


    # ------------------------------------------------------
    # AUMENTAR INTENTOS
    # ------------------------------------------------------

    session["intentos"] += 1


    # ------------------------------------------------------
    # COMPARAR NÚMEROS
    # ------------------------------------------------------

    if numero < numero_secreto:

        session["mensaje"] = (
            f"El número secreto es mayor que {numero}."
        )

        session["resultado"] = "mayor"


    elif numero > numero_secreto:

        session["mensaje"] = (
            f"El número secreto es menor que {numero}."
        )

        session["resultado"] = "menor"


    else:

        session["mensaje"] = (
            f"¡Correcto! El número secreto era {numero_secreto}."
        )

        session["resultado"] = "correcto"


    # ------------------------------------------------------
    # VOLVER A LA PÁGINA PRINCIPAL
    # ------------------------------------------------------
    #
    # Aplicamos POST → Redirect → GET.
    #
    # El formulario se procesa aquí y luego el navegador
    # vuelve a realizar una solicitud GET hacia "/".
    # ------------------------------------------------------

    return redirect(url_for("index"))


# ----------------------------------------------------------
# REINICIAR JUEGO
# ----------------------------------------------------------

@app.route("/reiniciar")
def reiniciar():
    """
    Elimina la información actual de la sesión
    y redirige al inicio.

    Al volver a "/", se generará un nuevo número secreto.
    """

    # ------------------------------------------------------
    # ELIMINAR SESIÓN
    # ------------------------------------------------------

    session.clear()


    # ------------------------------------------------------
    # VOLVER AL INICIO
    # ------------------------------------------------------

    return redirect(url_for("index"))


# ----------------------------------------------------------
# EJECUTAR SERVIDOR
# ----------------------------------------------------------

if __name__ == "__main__":

    app.run(debug=True)
```

---

# 🔍 Análisis de `server.py`

## `random.randint(1, 10)`

La función:

```python
random.randint(1, 10)
```

genera un número entero aleatorio entre `1` y `10`.

Por ejemplo:

```text
3
```

o:

```text
8
```

o:

```text
10
```

Este número será nuestro número secreto.

---

# 🔐 Número secreto en `session`

No hacemos esto:

```python
numero_secreto = random.randint(1, 10)
```

cada vez que se visita `/`.

Eso provocaría que el número cambiara continuamente.

En su lugar utilizamos:

```python
if "numero_secreto" not in session:
    session["numero_secreto"] = random.randint(1, 10)
```

La idea es:

```text
Primera visita
        ↓
Generar número
        ↓
Guardar en session

Siguiente visita
        ↓
Ya existe
        ↓
Utilizar el mismo número
```

---

# 🔢 Contador de intentos

Inicializamos:

```python
session["intentos"] = 0
```

y después de cada intento:

```python
session["intentos"] += 1
```

De esta manera:

```text
Primer intento → 1
Segundo intento → 2
Tercer intento → 3
```

---

# 📨 `request.form`

El formulario tendrá un campo:

```html
name="numero"
```

Por lo tanto podremos obtenerlo con:

```python
request.form["numero"]
```

Como HTML entrega el valor como texto, utilizamos:

```python
int(request.form["numero"])
```

Por ejemplo:

```text
"7"
```

se convierte en:

```python
7
```

---

# ⚖️ Comparación

El servidor utiliza:

```python
if numero < numero_secreto:
```

para comprobar si el usuario ingresó un número menor.

Luego:

```python
elif numero > numero_secreto:
```

comprueba si ingresó un número mayor.

Finalmente:

```python
else:
```

significa que ambos valores son iguales.

---

# 🔄 `redirect()`

Después de procesar el formulario:

```python
return redirect(url_for("index"))
```

Esto implementa:

```text
POST
 ↓
Procesar intento
 ↓
Modificar session
 ↓
redirect()
 ↓
GET /
 ↓
Mostrar resultado
```

De esta manera evitamos renderizar directamente la página después del POST.

---

# 📝 `templates/index.html`

Esta plantilla contiene toda la interfaz del juego.

Utiliza Jinja2 para mostrar dinámicamente:

- cantidad de intentos;
- mensaje;
- estado del resultado.

```html
<!DOCTYPE html>
<html lang="es">

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>Adivina el Número</title>

    <link
        rel="stylesheet"
        href="{{ url_for('static', filename='style.css') }}"
    >

</head>

<body>

<div class="pagina">

    <!-- ==================================================
         TARJETA PRINCIPAL
    =================================================== -->

    <main class="juego">

        <!-- Encabezado -->

        <header class="juego-header">

            <div class="icono">

                🎯

            </div>

            <h1>Adivina el Número</h1>

            <p>

                Encuentra el número secreto entre 1 y 10

            </p>

        </header>


        <!-- ==================================================
             INFORMACIÓN DEL JUEGO
        =================================================== -->

        <section class="contenido">

            <div class="alerta">

                ℹ️

                {{ mensaje }}

            </div>


            <!-- Intentos -->

            <div class="intentos">

                Intentos:

                <strong>{{ intentos }}</strong>

            </div>


            <!-- ==================================================
                 NÚMEROS RÁPIDOS
            =================================================== -->

            <div class="numeros">

                {% for numero in range(1, 11) %}

                <button
                    type="button"
                    class="numero"
                    onclick="document.getElementById('numero').value = {{ numero }}"
                >

                    {{ numero }}

                </button>

                {% endfor %}

            </div>


            <!-- ==================================================
                 FORMULARIO
            =================================================== -->

            <form
                action="{{ url_for('adivinar') }}"
                method="POST"
            >

                <label for="numero">

                    Tu elección:

                </label>


                <input
                    type="number"
                    id="numero"
                    name="numero"
                    min="1"
                    max="10"
                    required
                >


                <button
                    type="submit"
                    class="btn btn-adivinar"
                >

                    🔍 Adivinar

                </button>

            </form>


            <!-- ==================================================
                 RESULTADO
            =================================================== -->

            {% if resultado == "correcto" %}

                <div class="resultado correcto">

                    🎉 ¡Has acertado!

                </div>

            {% elif resultado == "mayor" %}

                <div class="resultado mayor">

                    ⬆️ El número secreto es mayor.

                </div>

            {% elif resultado == "menor" %}

                <div class="resultado menor">

                    ⬇️ El número secreto es menor.

                </div>

            {% endif %}


            <!-- ==================================================
                 REINICIAR
            =================================================== -->

            <a
                href="{{ url_for('reiniciar') }}"
                class="btn btn-reiniciar"
            >

                ↻ Reiniciar Juego

            </a>

        </section>


        <!-- ==================================================
             PIE DEL JUEGO
        =================================================== -->

        <footer class="juego-footer">

            ¡Intenta adivinar el número secreto
            en la menor cantidad de intentos!

        </footer>

    </main>


    <!-- ==================================================
         REGLAS
    =================================================== -->

    <section class="reglas">

        <h2>

            📋 Reglas del juego

        </h2>

        <ul>

            <li>

                Se ha generado un número aleatorio
                entre 1 y 10.

            </li>

            <li>

                Debes intentar adivinar cuál es
                ese número.

            </li>

            <li>

                Después de cada intento recibirás
                una pista.

            </li>

            <li>

                ¡Trata de adivinarlo en la menor
                cantidad de intentos!

            </li>

        </ul>

    </section>

</div>

</body>

</html>
```

---

# 🔍 Análisis de `index.html`

## `extends`

En esta actividad no necesitamos herencia de plantillas porque únicamente trabajamos con una página.

Por lo tanto:

```text
templates/
└── index.html
```

es suficiente.

---

# 🔢 Botones del 1 al 10

Utilizamos:

```jinja
{% for numero in range(1, 11) %}
```

Esto genera automáticamente:

```text
1  2  3  4  5  6  7  8  9  10
```

No es necesario escribir los diez botones manualmente.

Cada botón cambia el valor del campo:

```javascript
document.getElementById('numero').value = 5
```

Por ejemplo, al presionar:

```text
5
```

el campo del formulario quedará automáticamente en:

```text
5
```

Luego el usuario puede presionar:

```text
Adivinar
```

---

# 🔄 Formulario

El formulario utiliza:

```html
<form
    action="{{ url_for('adivinar') }}"
    method="POST"
>
```

Esto indica que los datos serán enviados a:

```text
/adivinar
```

utilizando:

```text
POST
```

---

# 📌 El atributo `name`

El input posee:

```html
name="numero"
```

por lo que Flask puede recuperar el valor utilizando:

```python
request.form["numero"]
```

La relación es:

```text
HTML

name="numero"

        ↓

request.form["numero"]

        ↓

Python
```

---

# 🧠 Condicionales de Jinja2

Utilizamos:

```jinja
{% if resultado == "correcto" %}
```

para mostrar un mensaje diferente dependiendo del resultado.

Si:

```python
resultado = "correcto"
```

se muestra:

```text
🎉 ¡Has acertado!
```

Si:

```python
resultado = "mayor"
```

se muestra:

```text
⬆️ El número secreto es mayor.
```

Y si:

```python
resultado = "menor"
```

se muestra:

```text
⬇️ El número secreto es menor.
```

Esto demuestra cómo Jinja2 puede controlar qué contenido aparece en HTML dependiendo de la información enviada por Flask.

---

# 🎨 `static/style.css`

Esta hoja de estilos se utiliza para obtener una apariencia similar a la referencia.

```css
/* ==========================================================
   ADIVINA EL NÚMERO
   Hoja de estilos principal
========================================================== */


/* ==========================================================
   VARIABLES
========================================================== */

:root {
    --azul: #2563eb;
    --azul-oscuro: #1d4ed8;
    --morado: #7c3aed;
    --rojo: #ef4444;
    --verde: #16a34a;
    --amarillo: #facc15;
    --gris: #f1f5f9;
    --texto: #334155;
    --blanco: #ffffff;
}


/* ==========================================================
   CONFIGURACIÓN GENERAL
========================================================== */

* {
    box-sizing: border-box;
}


body {
    margin: 0;
    min-height: 100vh;
    font-family: Arial, Helvetica, sans-serif;
    background: var(--gris);
    color: var(--texto);
}


/* ==========================================================
   CONTENEDOR
========================================================== */

.pagina {
    width: 100%;
    max-width: 700px;
    margin: 0 auto;
    padding: 30px 15px 50px;
}


/* ==========================================================
   TARJETA PRINCIPAL
========================================================== */

.juego {
    overflow: hidden;
    background: var(--blanco);
    border-radius: 12px;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
}


/* ==========================================================
   HEADER
========================================================== */

.juego-header {
    padding: 25px;
    text-align: center;
    color: var(--blanco);
    background: linear-gradient(
        135deg,
        var(--morado),
        var(--azul)
    );
}


.icono {
    font-size: 42px;
    margin-bottom: 5px;
}


.juego-header h1 {
    margin: 0;
    font-size: 34px;
}


.juego-header p {
    margin: 10px 0 0;
    font-size: 16px;
}


/* ==========================================================
   CONTENIDO
========================================================== */

.contenido {
    padding: 25px;
}


/* ==========================================================
   MENSAJE
========================================================== */

.alerta {
    margin-bottom: 15px;
    padding: 12px 15px;
    border: 1px solid #8bd0df;
    border-radius: 7px;
    background: #dff5f9;
    color: #0f6674;
    font-weight: bold;
}


/* ==========================================================
   INTENTOS
========================================================== */

.intentos {
    width: fit-content;
    margin: 0 auto 18px;
    padding: 7px 12px;
    border-radius: 7px;
    background: #475569;
    color: var(--blanco);
    font-size: 14px;
}


.intentos strong {
    margin-left: 3px;
}


/* ==========================================================
   BOTONES NUMÉRICOS
========================================================== */

.numeros {
    display: flex;
    justify-content: center;
    gap: 8px;
    flex-wrap: wrap;
    margin-bottom: 25px;
}


.numero {
    width: 36px;
    height: 36px;
    border: none;
    border-radius: 50%;
    background: #e2e8f0;
    color: #334155;
    font-weight: bold;
    cursor: pointer;
    transition: 0.2s ease;
}


.numero:hover {
    background: var(--azul);
    color: var(--blanco);
    transform: translateY(-2px);
}


/* ==========================================================
   FORMULARIO
========================================================== */

form {
    display: flex;
    flex-direction: column;
}


form label {
    margin-bottom: 7px;
    font-weight: bold;
}


form input {
    width: 100%;
    margin-bottom: 12px;
    padding: 12px;
    border: 1px solid #cbd5e1;
    border-radius: 7px;
    font-size: 16px;
    text-align: center;
}


form input:focus {
    outline: none;
    border-color: var(--azul);
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
}


/* ==========================================================
   BOTONES PRINCIPALES
========================================================== */

.btn {
    display: block;
    width: 100%;
    padding: 12px 15px;
    border-radius: 7px;
    color: var(--blanco);
    text-align: center;
    text-decoration: none;
    font-weight: bold;
    cursor: pointer;
    transition: 0.2s ease;
}


.btn:hover {
    transform: translateY(-1px);
}


.btn-adivinar {
    border: none;
    background: linear-gradient(
        135deg,
        var(--morado),
        var(--azul)
    );
}


.btn-adivinar:hover {
    opacity: 0.93;
}


/* ==========================================================
   RESULTADOS
========================================================== */

.resultado {
    margin-top: 15px;
    padding: 12px;
    border-radius: 7px;
    text-align: center;
    font-weight: bold;
}


.resultado.correcto {
    background: #dcfce7;
    color: #166534;
}


.resultado.mayor {
    background: #dbeafe;
    color: #1d4ed8;
}


.resultado.menor {
    background: #fee2e2;
    color: #b91c1c;
}


/* ==========================================================
   BOTÓN REINICIAR
========================================================== */

.btn-reiniciar {
    margin-top: 12px;
    background: var(--rojo);
}


.btn-reiniciar:hover {
    background: #dc2626;
}


/* ==========================================================
   FOOTER DEL JUEGO
========================================================== */

.juego-footer {
    padding: 10px 20px;
    background: linear-gradient(
        135deg,
        var(--morado),
        var(--azul)
    );
    color: var(--blanco);
    text-align: center;
    font-size: 13px;
}


/* ==========================================================
   REGLAS
========================================================== */

.reglas {
    margin-top: 18px;
    padding: 20px;
    background: var(--blanco);
    border-radius: 10px;
    box-shadow: 0 5px 18px rgba(0, 0, 0, 0.08);
}


.reglas h2 {
    margin-top: 0;
    color: var(--morado);
    font-size: 20px;
}


.reglas ul {
    margin-bottom: 0;
    padding-left: 20px;
}


.reglas li {
    margin-bottom: 10px;
    line-height: 1.4;
}


/* ==========================================================
   RESPONSIVE
========================================================== */

@media (max-width: 600px) {

    .pagina {
        padding: 15px 10px 35px;
    }


    .juego-header {
        padding: 20px 15px;
    }


    .juego-header h1 {
        font-size: 28px;
    }


    .contenido {
        padding: 20px;
    }


    .numero {
        width: 34px;
        height: 34px;
        font-size: 13px;
    }

}
```

---

# 🔍 Análisis del CSS

## Contenedor de la aplicación

```css
.pagina {
    max-width: 700px;
}
```

Esto limita el ancho de la aplicación para que se parezca a la referencia y no ocupe toda la pantalla.

---

## Encabezado

El encabezado utiliza:

```css
background: linear-gradient(
    135deg,
    var(--morado),
    var(--azul)
);
```

Esto crea una transición entre morado y azul.

---

## Tarjeta principal

```css
.juego {
    background: var(--blanco);
    border-radius: 12px;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
}
```

Permite generar el panel blanco central visible en la referencia.

---

## Botones numéricos

Cada número se transforma en un círculo mediante:

```css
border-radius: 50%;
```

Por eso visualmente obtenemos:

```text
① ② ③ ④ ⑤ ⑥ ⑦ ⑧ ⑨ ⑩
```

---

# 📌 Rutas de la aplicación

| Ruta | Método | Función |
|---|---|---|
| `/` | GET | Mostrar el juego |
| `/adivinar` | POST | Procesar el intento |
| `/reiniciar` | GET | Eliminar sesión y comenzar nuevamente |

---

# 🔐 Información almacenada en `session`

Durante la ejecución podremos tener:

```python
session = {
    "numero_secreto": 7,
    "intentos": 3,
    "mensaje": "El número secreto es mayor que 5.",
    "resultado": "mayor"
}
```

Cada propiedad tiene una función diferente:

| Propiedad | Uso |
|---|---|
| `numero_secreto` | Número que debe descubrir el usuario |
| `intentos` | Cantidad de intentos realizados |
| `mensaje` | Pista mostrada al usuario |
| `resultado` | Permite controlar el mensaje visual |

---

# 🗑️ Reiniciar el juego

La ruta:

```python
@app.route("/reiniciar")
def reiniciar():
```

realiza:

```python
session.clear()
```

Esto elimina:

```text
numero_secreto
intentos
mensaje
resultado
```

Luego:

```python
return redirect(url_for("index"))
```

lleva nuevamente al inicio.

Cuando `/` se ejecuta nuevamente, como ya no existe:

```python
"numero_secreto"
```

Flask genera un nuevo número.

---

# 🧠 Conceptos aplicados

Esta práctica reúne varios contenidos vistos previamente:

```text
Flask
 │
 ├── Rutas
 │
 ├── GET
 │
 ├── POST
 │
 ├── request.form
 │
 ├── redirect()
 │
 ├── url_for()
 │
 └── session
       │
       ├── inicialización
       ├── lectura
       ├── modificación
       └── eliminación
              │
              ▼
           Jinja2
              │
              ├── {{ variable }}
              ├── {% if %}
              └── {% for %}
```

---

# ✅ Requisitos cumplidos

## Core

- ✅ Crear una aplicación Flask.
- ✅ Generar un número aleatorio entre 1 y 10.
- ✅ Guardar el número secreto en sesión.
- ✅ Mostrar el formulario.
- ✅ Recibir un número mediante `POST`.
- ✅ Convertir el dato recibido a `int`.
- ✅ Comparar el número ingresado con el secreto.
- ✅ Indicar si el número es mayor o menor.
- ✅ Informar cuando el usuario acierta.
- ✅ Contabilizar intentos.
- ✅ Reiniciar el juego.
- ✅ Eliminar la sesión.

---

# ⭐ Funcionalidades complementarias

Además del Core, la implementación incluye:

- ✅ Botones rápidos del 1 al 10.
- ✅ Contador de intentos visible.
- ✅ Mensajes dinámicos con Jinja2.
- ✅ Indicadores visuales según el resultado.
- ✅ Diseño responsive.
- ✅ Botón de reinicio.
- ✅ Sección de reglas.
- ✅ `url_for()` para las rutas.
- ✅ `url_for()` para el archivo CSS.
- ✅ Patrón POST → Redirect → GET.

---

# 🧪 Ejemplo de ejecución

Supongamos que Flask genera:

```text
Número secreto = 7
```

El usuario ingresa:

```text
4
```

El servidor ejecutará:

```python
if 4 < 7:
```

y guardará:

```python
session["resultado"] = "mayor"
```

La página mostrará:

```text
⬆️ El número secreto es mayor.
```

---

Si posteriormente ingresa:

```text
9
```

obtendremos:

```text
⬇️ El número secreto es menor.
```

Finalmente:

```text
7
```

mostrará:

```text
🎉 ¡Has acertado!
```

---

# 🏁 Resultado final

Al ejecutar:

```bash
python server.py
```

y acceder a:

```text
http://127.0.0.1:5000/
```

se dispondrá de un juego funcional en Flask.

El usuario podrá:

```text
        🎯 ADIVINA EL NÚMERO

    ℹ️ Adivina un número entre 1 y 10

             Intentos: 0

       ① ② ③ ④ ⑤ ⑥ ⑦ ⑧ ⑨ ⑩

       Tu elección:
       ┌─────────────────────────┐
       │            5            │
       └─────────────────────────┘

       ┌─────────────────────────┐
       │       🔍 Adivinar        │
       └─────────────────────────┘

       ┌─────────────────────────┐
       │     ↻ Reiniciar Juego   │
       └─────────────────────────┘
```

---

# 💬 Pregunta de reflexión

> Actualmente el juego no tiene un límite de intentos. ¿Cómo modificarías la sesión y la lógica del servidor para permitir, por ejemplo, solamente **5 intentos** antes de finalizar la partida?

Una posible evolución sería almacenar:

```python
session["intentos"]
```

y utilizar una condición como:

```python
if session["intentos"] >= 5:
```

para determinar cuándo termina el juego.
Mostrando README.md