from flask_app import app

from flask import (
    render_template,
    request,
    redirect,
    url_for
)

from flask_app.models.pedido import Pedido


# ==========================================================
# INICIO
# ==========================================================

@app.route("/")
def inicio():
    """
    La ruta raíz redirige al listado de pedidos.
    """

    return redirect(
        url_for("pedidos")
    )


# ==========================================================
# LISTADO DE PEDIDOS
# ==========================================================

@app.route("/pedidos")
def pedidos():
    """
    Recupera los pedidos desde MySQL
    y los envía a la vista.
    """

    todos_los_pedidos = Pedido.get_all()


    return render_template(
        "pedidos.html",
        pedidos=todos_los_pedidos
    )


# ==========================================================
# FORMULARIO NUEVO PEDIDO
# ==========================================================

@app.route("/pedidos/nuevo")
def nuevo_pedido():
    """
    Muestra el formulario de creación.
    """

    return render_template(
        "nuevo_pedido.html"
    )


# ==========================================================
# CREAR PEDIDO
# ==========================================================

@app.route(
    "/pedidos/crear",
    methods=["POST"]
)
def crear_pedido():
    """
    Recibe la información del formulario,
    valida los datos y, si son correctos,
    guarda el pedido.
    """

    # ------------------------------------------------------
    # Recuperamos los datos enviados por el formulario.
    # ------------------------------------------------------

    nombre = request.form.get(
        "nombre",
        ""
    ).strip()

    tipo_arepa = request.form.get(
        "tipo_arepa",
        ""
    ).strip()

    cantidad = request.form.get(
        "cantidad",
        ""
    ).strip()


    # ------------------------------------------------------
    # Creamos el diccionario que recibirá el modelo.
    # ------------------------------------------------------

    data = {
        "nombre": nombre,
        "tipo_arepa": tipo_arepa,
        "cantidad": cantidad
    }


    # ------------------------------------------------------
    # Validamos ANTES de guardar.
    # ------------------------------------------------------

    if not Pedido.validar_pedido(data):

        return redirect(
            url_for("nuevo_pedido")
        )


    # ------------------------------------------------------
    # Como la validación fue correcta, convertimos
    # cantidad a entero antes de guardarla.
    # ------------------------------------------------------

    data["cantidad"] = int(
        data["cantidad"]
    )


    # ------------------------------------------------------
    # Guardamos el pedido.
    # ------------------------------------------------------

    resultado = Pedido.save(
        data
    )


    # ------------------------------------------------------
    # En caso de error en la base de datos.
    # ------------------------------------------------------

    if resultado is False:

        from flask import flash

        flash(
            "No fue posible guardar el pedido.",
            "danger"
        )

        return redirect(
            url_for("nuevo_pedido")
        )


    # ------------------------------------------------------
    # Pedido creado correctamente.
    # ------------------------------------------------------

    from flask import flash

    flash(
        "Pedido creado correctamente.",
        "success"
    )


    return redirect(
        url_for("pedidos")
    )
