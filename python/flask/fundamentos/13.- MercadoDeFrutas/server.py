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