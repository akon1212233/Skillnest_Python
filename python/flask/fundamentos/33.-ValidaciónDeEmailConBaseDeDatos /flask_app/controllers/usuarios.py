from flask_app import app

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from flask_app.models.usuario import Usuario


# ==========================================================
# INICIO
# ==========================================================

@app.route("/")
def inicio():
    """
    La raíz redirige al listado de usuarios.
    """

    return redirect(
        url_for("usuarios")
    )


# ==========================================================
# LISTADO
# ==========================================================

@app.route("/usuarios")
def usuarios():
    """
    Obtiene todos los usuarios y los envía
    a la plantilla.
    """

    todos_los_usuarios = Usuario.get_all()

    return render_template(
        "usuarios.html",
        usuarios=todos_los_usuarios
    )


# ==========================================================
# FORMULARIO NUEVO USUARIO
# ==========================================================

@app.route("/usuarios/nuevo")
def nuevo_usuario():
    """
    Muestra el formulario de creación.

    Si existen datos guardados temporalmente
    por un error anterior, los recuperamos.
    """

    datos_formulario = session.pop(
        "datos_formulario",
        {}
    )


    return render_template(
        "nuevo_usuario.html",
        datos_formulario=datos_formulario
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
    Recibe, valida y guarda un usuario.
    """

    # ------------------------------------------------------
    # Recuperamos los datos del formulario.
    # ------------------------------------------------------

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


    # ------------------------------------------------------
    # Diccionario que será enviado al modelo.
    # ------------------------------------------------------

    data = {
        "nombre": nombre,
        "apellido": apellido,
        "email": email
    }


    # ------------------------------------------------------
    # VALIDACIÓN BÁSICA
    # ------------------------------------------------------

    if not Usuario.validar_usuario(data):

        # Guardamos temporalmente los datos para
        # recuperarlos después del redirect.
        session["datos_formulario"] = data

        return redirect(
            url_for("nuevo_usuario")
        )


    # ------------------------------------------------------
    # BONUS — EMAIL ÚNICO
    # ------------------------------------------------------

    if Usuario.email_existe(
        data["email"]
    ):

        flash(
            "El email ingresado ya está registrado.",
            "email"
        )

        # Conservamos los datos del formulario.
        session["datos_formulario"] = data

        return redirect(
            url_for("nuevo_usuario")
        )


    # ------------------------------------------------------
    # GUARDAR
    # ------------------------------------------------------

    resultado = Usuario.save(
        data
    )


    # ------------------------------------------------------
    # Error en la base de datos.
    # ------------------------------------------------------

    if resultado is False:

        flash(
            "No fue posible crear el usuario.",
            "error"
        )

        session["datos_formulario"] = data

        return redirect(
            url_for("nuevo_usuario")
        )


    # ------------------------------------------------------
    # ÉXITO
    # ------------------------------------------------------

    # Nos aseguramos de eliminar cualquier información
    # temporal que todavía pudiera existir.
    session.pop(
        "datos_formulario",
        None
    )


    flash(
        "Usuario creado correctamente.",
        "success"
    )


    # Después de un POST exitoso:
    # POST → INSERT → redirect → GET
    return redirect(
        url_for("usuarios")
    )
