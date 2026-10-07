from flask_app import app

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_app.models.usuario import Usuario
from flask_app.models.seguidor import Seguidor


# ==========================================================
# INICIO
# ==========================================================

@app.route("/")
def inicio():
    """
    Redirige la página principal hacia /usuarios.
    """

    return redirect(
        url_for("usuarios")
    )


# ==========================================================
# USUARIOS
# ==========================================================

@app.route("/usuarios")
def usuarios():
    """
    Obtiene todos los usuarios y todas las relaciones.
    """

    lista_usuarios = Usuario.get_all()

    relaciones = Seguidor.get_all()

    return render_template(
        "usuarios.html",
        usuarios=lista_usuarios,
        relaciones=relaciones
    )


# ==========================================================
# CREAR USUARIO
# ==========================================================

@app.route(
    "/usuarios/crear",
    methods=["POST"]
)
def crear_usuario():
    """
    Recibe los datos del formulario y crea un usuario.
    """

    nombre = request.form.get(
        "nombre",
        ""
    ).strip()

    apellido = request.form.get(
        "apellido",
        ""
    ).strip()

    email = request.form.get(
        "email",
        ""
    ).strip()


    if not nombre or not apellido or not email:

        flash(
            "Todos los campos son obligatorios.",
            "danger"
        )

        return redirect(
            url_for("usuarios")
        )


    data = {
        "nombre": nombre,
        "apellido": apellido,
        "email": email
    }


    resultado = Usuario.save(
        data
    )


    if resultado is False:

        flash(
            "No fue posible crear el usuario.",
            "danger"
        )

        return redirect(
            url_for("usuarios")
        )


    flash(
        "Usuario creado correctamente.",
        "success"
    )


    return redirect(
        url_for("usuarios")
    )


# ==========================================================
# CREAR RELACIÓN
# ==========================================================

@app.route(
    "/seguir",
    methods=["POST"]
)
def seguir():
    """
    Registra que un usuario sigue a otro.

    usuario_id:
        usuario que está siendo seguido.

    seguidor_id:
        usuario que lo sigue.
    """

    usuario_id_texto = request.form.get(
        "usuario_id"
    )

    seguidor_id_texto = request.form.get(
        "seguidor_id"
    )


    if not usuario_id_texto or not seguidor_id_texto:

        flash(
            "Debes seleccionar un usuario y un seguidor.",
            "danger"
        )

        return redirect(
            url_for("usuarios")
        )


    try:

        usuario_id = int(
            usuario_id_texto
        )

        seguidor_id = int(
            seguidor_id_texto
        )

    except ValueError:

        flash(
            "Los identificadores no son válidos.",
            "danger"
        )

        return redirect(
            url_for("usuarios")
        )


    # ------------------------------------------------------
    # Comprobar que el usuario exista.
    # ------------------------------------------------------

    usuario = Usuario.get_by_id(
        usuario_id
    )


    if usuario is None:

        flash(
            "El usuario seleccionado no existe.",
            "danger"
        )

        return redirect(
            url_for("usuarios")
        )


    # ------------------------------------------------------
    # Comprobar que el seguidor exista.
    # ------------------------------------------------------

    seguidor = Usuario.get_by_id(
        seguidor_id
    )


    if seguidor is None:

        flash(
            "El seguidor seleccionado no existe.",
            "danger"
        )

        return redirect(
            url_for("usuarios")
        )


    # ------------------------------------------------------
    # Crear diccionario de datos.
    # ------------------------------------------------------

    data = {
        "usuario_id": usuario_id,
        "seguidor_id": seguidor_id
    }


    # ------------------------------------------------------
    # Comprobar relación duplicada.
    # ------------------------------------------------------

    if Seguidor.existe(data):

        flash(
            "Esta relación ya existe.",
            "warning"
        )

        return redirect(
            url_for("usuarios")
        )


    # ------------------------------------------------------
    # Insertar relación.
    # ------------------------------------------------------

    resultado = Seguidor.seguir(
        data
    )


    if resultado is False:

        flash(
            "No fue posible registrar la relación.",
            "danger"
        )

        return redirect(
            url_for("usuarios")
        )


    flash(
        "Relación registrada correctamente.",
        "success"
    )


    return redirect(
        url_for("usuarios")
    )