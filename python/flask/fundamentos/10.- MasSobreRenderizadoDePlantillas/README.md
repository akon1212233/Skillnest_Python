# 📚 Lección 9 - Renderizando Colecciones de Datos con Jinja2

> **Curso:** Desarrollo Web con Flask desde Cero  
> **Unidad:** Motor de Plantillas (Jinja2)  
> **Tema:** Envío de listas y diccionarios desde Flask hacia HTML.

---

# 📖 Descripción General

En las lecciones anteriores aprendimos a enviar **variables individuales** desde Flask hacia nuestras plantillas HTML utilizando la función `render_template()`.

Por ejemplo:

```python
nombre = "Daniel"

edad = 31

ciudad = "Santiago"
```

Cada una de estas variables representa un único dato.

Sin embargo, una aplicación web real rara vez trabaja con un solo dato. Lo habitual es mostrar **colecciones de información**, por ejemplo:

- Un listado de estudiantes.
- Un catálogo de productos.
- Una lista de videojuegos.
- Un ranking de jugadores.
- Los resultados de una consulta a una base de datos.

Para resolver este problema utilizaremos **listas** y **listas de diccionarios**, recorriéndolas mediante el motor de plantillas **Jinja2**.

---

# 🎯 Objetivos

Al finalizar esta lección serás capaz de:

- Enviar listas desde Flask hacia una plantilla HTML.
- Enviar listas de diccionarios.
- Recorrer colecciones utilizando un ciclo `for`.
- Mostrar información almacenada dentro de un diccionario.
- Comprender cómo Jinja2 procesa colecciones de datos.

---

# 🧠 ¿Qué aprenderemos?

En esta lección incorporaremos un nuevo concepto:

## Hasta ahora

Enviábamos una sola variable.

```python
return render_template(
    "index.html",
    nombre="Daniel"
)
```

En el HTML:

```html
<h1>{{ nombre }}</h1>
```

Resultado:

```
Daniel
```

---

## Ahora

Enviaremos una colección completa.

```python
numeros = [7, 15, 22]
```

o

```python
estudiantes = [
    {"nombre":"Florencia","edad":25},
    {"nombre":"Valentina","edad":30},
    {"nombre":"José","edad":27}
]
```

Como existen varios elementos, necesitaremos recorrerlos utilizando un ciclo **for**.

---

# 📂 Estructura del proyecto

Trabajaremos sobre el proyecto desarrollado en las lecciones anteriores.

```text
hola_flask/

│

├── server.py

│

├── templates/

│   ├── index.html
│   └── listas.html

│

└── static/
```

---

# 📝 Paso 1 - Crear una nueva ruta

Abre tu archivo **server.py** y agrega la siguiente ruta.

```python
@app.route("/listas")
def renderizar_listas():

    # Lista de números

    numeros = [7, 15, 22]

    # Lista de diccionarios

    listado_estudiantes = [

        {
            "nombre":"Florencia",
            "edad":25
        },

        {
            "nombre":"Valentina",
            "edad":30
        },

        {
            "nombre":"José",
            "edad":27
        },

        {
            "nombre":"Patricio",
            "edad":21
        }

    ]

    return render_template(

        "listas.html",

        numeros=numeros,

        estudiantes=listado_estudiantes

    )
```

---

# 🔍 Analizando el código

Observemos la primera variable.

```python
numeros = [7, 15, 22]
```

Es una **lista**.

Visualmente podríamos imaginarla así.

```
┌────┬────┬────┐
│ 7  │15  │22  │
└────┴────┴────┘
```

Cada posición contiene un número.

---

Ahora observemos la segunda variable.

```python
listado_estudiantes = [

    {
        "nombre":"Florencia",
        "edad":25
    },

    {
        "nombre":"Valentina",
        "edad":30
    }

]
```

Aquí ya no tenemos números.

Tenemos una **lista de diccionarios**.

Cada elemento de la lista representa un estudiante.

Visualmente.

```
Lista

│

├── Estudiante

│      ├── nombre

│      └── edad

│

├── Estudiante

│      ├── nombre

│      └── edad

│

└── Estudiante
```

Esta estructura será muy común cuando trabajemos con bases de datos.

---

# 📝 Paso 2 - Enviar las listas al HTML

Observa la siguiente instrucción.

```python
return render_template(

    "listas.html",

    numeros=numeros,

    estudiantes=listado_estudiantes

)
```

Estamos enviando dos variables hacia la plantilla.

| Variable | Contenido |
|----------|-----------|
| numeros | Lista de enteros |
| estudiantes | Lista de diccionarios |

Ahora ambas estarán disponibles dentro del archivo HTML.

---

# 📝 Paso 3 - Crear la plantilla

Dentro de la carpeta **templates**, crea un archivo llamado:

```text
listas.html
```

Agrega el siguiente código.

```html
<!DOCTYPE html>

<html lang="es">

<head>

    <meta charset="UTF-8">

    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">

    <title>Renderizando Listas</title>

</head>

<body>

    <h1>Números Aleatorios</h1>

    {% for numero in numeros %}

        <p>{{ numero }}</p>

    {% endfor %}

    <hr>

    <h1>Listado de Estudiantes</h1>

    <ul>

        {% for estudiante in estudiantes %}

            <li>

                {{ estudiante["nombre"] }}

                -

                {{ estudiante["edad"] }}

            </li>

        {% endfor %}

    </ul>

</body>

</html>
```

---

# 🔁 El ciclo **for** en Jinja2

La siguiente estructura:

```jinja
{% for numero in numeros %}

    <p>{{ numero }}</p>

{% endfor %}
```

recorre automáticamente todos los elementos de la lista.

Internamente funciona de forma muy parecida a Python.

En Python escribiríamos:

```python
for numero in numeros:

    print(numero)
```

Jinja realiza exactamente el mismo recorrido, pero en lugar de imprimir los datos en la consola, genera código HTML.

---

# 🧠 ¿Qué ocurre durante cada iteración?

Si la lista contiene:

```python
[7, 15, 22]
```

Jinja realiza el siguiente proceso.

Primera vuelta.

```
numero = 7
```

Segunda vuelta.

```
numero = 15
```

Tercera vuelta.

```
numero = 22
```

Por ello se generan tres etiquetas `<p>`.

Resultado:

```
7

15

22
```

---

# 🔁 Recorriendo una lista de diccionarios

Ahora observemos este bloque.

```jinja
{% for estudiante in estudiantes %}
```

En cada iteración, la variable **estudiante** representa un diccionario diferente.

Primera vuelta.

```python
{
    "nombre":"Florencia",
    "edad":25
}
```

Segunda vuelta.

```python
{
    "nombre":"Valentina",
    "edad":30
}
```

Y así sucesivamente.

---

# 🔑 Accediendo a la información del diccionario

Cada estudiante contiene dos propiedades.

```python
{
    "nombre":"Florencia",
    "edad":25
}
```

Podemos acceder a ellas utilizando su clave.

```jinja
{{ estudiante["nombre"] }}
```

Resultado.

```
Florencia
```

Y para la edad.

```jinja
{{ estudiante["edad"] }}
```

Resultado.

```
25
```

Finalmente la plantilla mostrará.

```
Florencia - 25
```

---

# 💡 Otra forma de acceder a los datos

Jinja también permite acceder a los diccionarios utilizando la notación de punto.

Las siguientes expresiones producen el mismo resultado.

```jinja
{{ estudiante["nombre"] }}
```

```jinja
{{ estudiante.nombre }}
```

Para este curso utilizaremos principalmente la primera forma, ya que es más similar al acceso tradicional a diccionarios en Python.

---

# 📊 Resultado esperado

Al ejecutar el servidor y acceder a la siguiente ruta:

```
http://127.0.0.1:5000/listas
```

deberás visualizar una página similar a esta.

```
Número Aleatorios

7

15

22


Listado de Estudiantes

• Florencia - 25

• Valentina - 30

• José - 27

• Patricio - 21
```

---

# ⚠️ Errores comunes

## Error 1

Intentar recorrer una variable que no existe.

```jinja
{% for estudiante in alumnos %}
```

Si desde Flask enviaste la variable `estudiantes`, Jinja mostrará un error porque `alumnos` no existe.

---

## Error 2

Olvidar cerrar el ciclo.

Incorrecto.

```jinja
{% for numero in numeros %}

<p>{{ numero }}</p>
```

Correcto.

```jinja
{% for numero in numeros %}

<p>{{ numero }}</p>

{% endfor %}
```

---

## Error 3

Intentar acceder a una clave inexistente.

```jinja
{{ estudiante["apellido"] }}
```

Si el diccionario no posee la clave `apellido`, no se mostrará el resultado esperado.

---

# 💾 Relación con una Base de Datos

Muy pronto comenzaremos a trabajar con **MySQL**.

Cuando consultemos una tabla, el resultado será muy parecido a la estructura utilizada en esta actividad.

Por ejemplo, una consulta como:

```sql
SELECT nombre, edad
FROM estudiantes;
```

podría devolver una estructura similar a esta.

```python
[
    {
        "nombre":"Florencia",
        "edad":25
    },
    {
        "nombre":"Valentina",
        "edad":30
    },
    {
        "nombre":"José",
        "edad":27
    }
]
```

Observa que el HTML no cambiará.

La única diferencia será el origen de los datos.

Hoy los escribimos manualmente.

Más adelante serán obtenidos automáticamente desde la base de datos.

---

# 📝 Actividad

Crea una nueva ruta llamada:

```python
/videojuegos
```

La ruta deberá enviar una lista de **6 videojuegos**.

Cada videojuego deberá contener:

- Nombre
- Plataforma
- Año de lanzamiento

Ejemplo.

```python
{
    "nombre":"Minecraft",
    "plataforma":"PC",
    "anio":2011
}
```

Crea una nueva plantilla llamada:

```text
videojuegos.html
```

Utiliza un ciclo `for` para mostrar todos los videojuegos en una lista HTML.

---

# 🚀 Desafío

Modifica el listado de estudiantes para que aparezca numerado automáticamente utilizando la variable especial de Jinja:

```jinja
loop.index
```

Resultado esperado.

```
1. Florencia - 25

2. Valentina - 30

3. José - 27

4. Patricio - 21
```

---

# 🏁 Conclusión

En esta lección aprendiste a enviar **colecciones de datos** desde Flask hacia una plantilla HTML.

Ahora ya no estás limitado a mostrar una sola variable, sino que puedes renderizar listas completas de información utilizando **Jinja2**.

Este será uno de los conceptos más importantes del curso, ya que en las próximas unidades los datos dejarán de ser escritos manualmente y serán obtenidos directamente desde una base de datos MySQL, manteniendo exactamente la misma forma de recorrer y mostrar la información en tus plantillas HTML.
Mostrando README.md