# ==========================================================
# CONTROLADOR DE TACOS
# ==========================================================

from __init__ import app


from flask import (
    render_template,
    redirect,
    request,
    url_for
)


from models.taco import Taco


# ==========================================================
# INICIO
# ==========================================================

@app.route("/")
def index():
    """
    Muestra el formulario principal para crear un taco.
    """

    return render_template(
        "index.html"
    )


# ==========================================================
# CREATE
# CREAR TACO
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

        "tortilla": request.form["tortilla"],

        "guiso": request.form["guiso"],

        "salsa": request.form["salsa"]

    }


    Taco.save(
        datos
    )


    return redirect(
        url_for("tacos")
    )


# ==========================================================
# READ
# LISTAR TACOS
# ==========================================================

@app.route("/tacos")
def tacos():
    """
    Recupera todos los tacos
    y los envía a la vista.
    """

    todos_los_tacos = Taco.get_all()


    return render_template(
        "resultados.html",
        todos_tacos=todos_los_tacos
    )


# ==========================================================
# READ
# VER DETALLE
# ==========================================================

@app.route(
    "/mostrar/<int:taco_id>"
)
def detalle(taco_id):
    """
    Recupera un taco específico.
    """

    datos = {
        "id": taco_id
    }


    taco = Taco.get_one(
        datos
    )


    if taco is None:

        return (
            "Taco no encontrado",
            404
        )


    return render_template(
        "detalle.html",
        taco=taco
    )


# ==========================================================
# UPDATE
# MOSTRAR FORMULARIO
# ==========================================================

@app.route(
    "/editar/<int:taco_id>"
)
def editar(taco_id):
    """
    Recupera un taco y muestra
    el formulario de edición.
    """

    datos = {
        "id": taco_id
    }


    taco = Taco.get_one(
        datos
    )


    if taco is None:

        return (
            "Taco no encontrado",
            404
        )


    return render_template(
        "editar.html",
        taco=taco
    )


# ==========================================================
# UPDATE
# PROCESAR EDICIÓN
# ==========================================================

@app.route(
    "/actualizar/<int:taco_id>",
    methods=["POST"]
)
def actualizar(taco_id):
    """
    Actualiza la información del taco.
    """

    datos = {

        "id": taco_id,

        "tortilla": request.form["tortilla"],

        "guiso": request.form["guiso"],

        "salsa": request.form["salsa"]

    }


    Taco.update(
        datos
    )


    return redirect(
        url_for(
            "detalle",
            taco_id=taco_id
        )
    )


# ==========================================================
# DELETE
# ELIMINAR TACO
# ==========================================================

@app.route(
    "/borrar/<int:taco_id>"
)
def borrar(taco_id):
    """
    Elimina un taco.
    """

    datos = {
        "id": taco_id
    }


    Taco.delete(
        datos
    )


    return redirect(
        url_for("tacos")
    )