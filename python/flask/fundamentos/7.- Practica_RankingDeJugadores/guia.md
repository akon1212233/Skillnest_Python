# 📚 Diccionario de Elementos Jinja2 Utilizados

Durante este desafío utilizamos varias características propias de **Jinja2**, el motor de plantillas de Flask.

El objetivo de este diccionario es comprender **qué hace cada elemento, cuándo utilizarlo y cómo funciona**.

---

# 📌 1. `{{ }}` — Mostrar información

## ¿Qué es?

Las dobles llaves `{{ }}` permiten **mostrar el valor de una variable** dentro del HTML.

Jinja2 reemplaza automáticamente la variable por su contenido antes de enviar la página al navegador.

---

## Sintaxis

```jinja
{{ variable }}
```

---

## Ejemplo

En Flask enviamos:

```python
nombre = "Daniel"

return render_template(
    "index.html",
    nombre=nombre
)
```

En el HTML:

```html
<h1>{{ nombre }}</h1>
```

El navegador finalmente recibe:

```html
<h1>Daniel</h1>
```

---

## Otro ejemplo

```jinja
{{ jugador.nombre }}
```

Si el jugador es:

```python
{
    "nombre":"Alex",
    "puntaje":5000
}
```

El resultado será:

```html
Alex
```

---

# 📌 2. `{% %}` — Ejecutar lógica

## ¿Qué es?

Las etiquetas `{% %}` permiten ejecutar lógica dentro de la plantilla.

No muestran información directamente.

Se utilizan para:

- Condicionales
- Bucles
- Bloques
- Herencia de plantillas
- Macros
- Entre otros

---

## Sintaxis

```jinja
{% instrucción %}
```

---

## Ejemplo

```jinja
{% if edad >= 18 %}

<p>Mayor de edad</p>

{% endif %}
```

---

# 📌 3. `{% if %}` — Condicional

## ¿Qué es?

Permite mostrar contenido únicamente cuando una condición se cumple.

Funciona prácticamente igual que un `if` de Python.

---

## Sintaxis

```jinja
{% if condición %}

...

{% endif %}
```

---

## Ejemplo

```jinja
{% if color %}

{{ color }}

{% else %}

#f4f4f4

{% endif %}
```

---

## ¿Qué hace este código?

Pregunta:

> ¿Existe una variable llamada **color**?

Si existe:

```text
lightblue
```

Se utilizará ese valor.

Si no existe:

```text
#f4f4f4
```

Se utilizará el color por defecto.

---

## Equivalente en Python

```python
if color:

    print(color)

else:

    print("#f4f4f4")
```

---

# 📌 4. `{% else %}`

## ¿Qué es?

Permite ejecutar una alternativa cuando la condición del `if` es falsa.

---

## Sintaxis

```jinja
{% if condición %}

...

{% else %}

...

{% endif %}
```

---

## Ejemplo

```jinja
{% if profesor %}

<p>Bienvenido Profesor</p>

{% else %}

<p>Bienvenido Estudiante</p>

{% endif %}
```

---

# 📌 5. `{% endif %}`

## ¿Qué es?

Marca el final de un bloque `if`.

Toda estructura condicional debe finalizar con:

```jinja
{% endif %}
```

---

## Ejemplo

```jinja
{% if activo %}

<p>Usuario activo</p>

{% endif %}
```

---

# 📌 6. `{% for %}` — Recorrer listas

## ¿Qué es?

Permite recorrer listas, tuplas o cualquier colección enviada desde Flask.

Es equivalente al `for` de Python.

---

## Sintaxis

```jinja
{% for elemento in lista %}

...

{% endfor %}
```

---

## Ejemplo

En Flask:

```python
jugadores = [

    {"nombre":"Alex"},

    {"nombre":"Juan"},

    {"nombre":"María"}

]
```

En el HTML:

```jinja
{% for jugador in jugadores %}

<p>{{ jugador.nombre }}</p>

{% endfor %}
```

Resultado:

```text
Alex

Juan

María
```

---

## Equivalente en Python

```python
for jugador in jugadores:

    print(jugador["nombre"])
```

---

# 📌 7. `{% endfor %}`

## ¿Qué es?

Finaliza un ciclo `for`.

Siempre debe utilizarse al terminar el recorrido.

---

## Ejemplo

```jinja
{% for jugador in jugadores %}

...

{% endfor %}
```

---

# 📌 8. `loop.index`

## ¿Qué es?

Es una variable especial creada automáticamente por Jinja2.

Representa la posición actual del ciclo.

Comienza en **1**.

---

## Ejemplo

```jinja
{% for jugador in jugadores %}

{{ loop.index }}

{% endfor %}
```

Resultado:

```text
1

2

3

4

5
```

---

## Ejemplo aplicado

```jinja
{{ loop.index }}.

{{ jugador.nombre }}
```

Resultado.

```text
1. Alex

2. Juan

3. María
```

---

## Equivalente en Python

```python
contador = 1

for jugador in jugadores:

    print(contador)

    contador += 1
```

En Jinja esto ya viene incorporado.

---

# 📌 9. `url_for()`

## ¿Qué es?

`url_for()` es una función proporcionada por Flask que genera automáticamente una URL válida para un recurso o una ruta.

Aunque se utiliza dentro de una plantilla Jinja2, **no pertenece a Jinja2**, sino que Flask la pone a disposición de las plantillas.

Su principal ventaja es evitar escribir rutas manualmente.

---

## Sintaxis

```jinja
{{ url_for(...) }}
```

---

## Ejemplo utilizado

```html
<link rel="stylesheet"

href="{{ url_for('static', filename='css/style.css') }}">
```

---

## ¿Qué hace?

Flask genera automáticamente la ruta correcta hacia el archivo.

Resultado:

```html
<link rel="stylesheet"

href="/static/css/style.css">
```

---

## ¿Por qué es mejor que escribir la ruta manualmente?

En lugar de escribir:

```html
<link rel="stylesheet"

href="/static/css/style.css">
```

utilizamos:

```jinja
{{ url_for('static', filename='css/style.css') }}
```

porque si en el futuro cambia la configuración del proyecto, Flask actualizará automáticamente la URL.

---

# 📌 10. `static`

## ¿Qué es?

Es el nombre reservado que Flask utiliza para acceder a la carpeta **static**.

Cuando escribimos:

```python
url_for("static", ...)
```

Flask entiende que debe buscar el archivo dentro de:

```text
static/
```

---

## Ejemplo

```text
static/

└── css/

    └── style.css
```

---

# 📌 11. `filename`

## ¿Qué es?

Es un argumento utilizado por `url_for()` para indicar qué archivo se desea obtener.

---

## Ejemplo

```jinja
{{ url_for(

    'static',

    filename='css/style.css'

) }}
```

Flask interpreta:

```
Busca el archivo:

static/css/style.css
```

---

# 📌 12. Variables CSS creadas con Jinja

## Código

```html
<style>

:root{

    --color-fondo:

    {% if color %}

        {{ color }}

    {% else %}

        #f4f4f4

    {% endif %}

}

</style>
```

---

## ¿Qué ocurre aquí?

Jinja2 procesa primero la plantilla.

Si desde Flask enviamos:

```python
color="lightblue"
```

El navegador finalmente recibe:

```css
:root{

    --color-fondo: lightblue;

}
```

Posteriormente, el archivo CSS utiliza esa variable.

```css
body{

    background-color: var(--color-fondo);

}
```

De esta forma mantenemos el CSS separado del HTML, pero permitimos que algunos valores cambien dinámicamente según la información enviada por Flask.

---

# 📝 Resumen

| Elemento | Función |
|----------|---------|
| `{{ }}` | Mostrar el valor de una variable. |
| `{% %}` | Ejecutar lógica dentro de la plantilla. |
| `{% if %}` | Evaluar una condición. |
| `{% else %}` | Ejecutar una alternativa. |
| `{% endif %}` | Finalizar un bloque `if`. |
| `{% for %}` | Recorrer listas u otras colecciones. |
| `{% endfor %}` | Finalizar un ciclo `for`. |
| `loop.index` | Obtener la posición actual del ciclo (comienza en 1). |
| `url_for()` | Generar automáticamente una URL válida. |
| `static` | Hace referencia a la carpeta `static` del proyecto Flask. |
| `filename` | Indica el archivo que se desea obtener desde `static`. |
| `var(--variable)` | Función propia de CSS que utiliza el valor de una variable CSS previamente definida. |
Mostrando guia.md