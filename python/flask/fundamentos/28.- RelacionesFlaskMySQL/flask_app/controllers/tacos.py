# ==========================================================
# CONTROLADOR DE TACOS
# ==========================================================

from flask_app import app

from flask import (
    render_template,
    request,
    redirect,
    url_for
)

from flask_app.models.taco import Taco

from flask_app.models.restaurante import Restaurante


# ==========================================================
# INICIO
# ==========================================================

@app.route("/")
def index():
    """
    Muestra el formulario para crear un taco.

    También recupera todos los restaurantes para que
    el usuario pueda seleccionar uno.
    """

    todos_restaurantes = Restaurante.get_all()


    return render_template(
        "index.html",
        todos_restaurantes=todos_restaurantes
    )


# ==========================================================
# CREATE
# ==========================================================

@app.route(
    "/crear",
    methods=["POST"]
)
def crear():
    """
    Recibe el formulario y crea un taco.
    """

    datos = {

        "tortilla": request.form[
            "tortilla"
        ].strip(),

        "guiso": request.form[
            "guiso"
        ].strip(),

        "salsa": request.form[
            "salsa"
        ].strip(),

        "restaurante_id": request.form[
            "restaurante_id"
        ]

    }


    Taco.save(
        datos
    )


    return redirect(
        url_for("tacos")
    )


# ==========================================================
# READ
# LISTADO DE TACOS
# ==========================================================

@app.route("/tacos")
def tacos():
    """
    Muestra todos los tacos.
    """

    todos_los_tacos = Taco.get_all()


    return render_template(
        "index.html",
        tacos=todos_los_tacos
    )


# ==========================================================
# READ
# RESTAURANTE + TACOS
# ==========================================================

@app.route(
    "/restaurantes/<int:id>"
)
def restaurante(id):
    """
    Muestra un restaurante junto con
    todos sus tacos relacionados.
    """

    datos = {
        "id": id
    }


    restaurante = Restaurante.get_restaurante_y_tacos(
        datos
    )


    if restaurante is None:

        return (
            "Restaurante no encontrado",
            404
        )


    return render_template(
        "restaurante.html",
        restaurante=restaurante
    )


# ==========================================================
# LISTADO DE RESTAURANTES
# ==========================================================

@app.route("/restaurantes")
def restaurantes():
    """
    Muestra todos los restaurantes.
    """

    todos_restaurantes = Restaurante.get_all()


    return render_template(
        "restaurantes.html",
        restaurantes=todos_restaurantes
    )