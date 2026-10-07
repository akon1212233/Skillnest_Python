from flask_app import app

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_app.models.usuario import Usuario
from flask_app.models.cancion import Cancion
from flask_app.models.favorito import Favorito


# ==========================================================
# USUARIOS
# ==========================================================

@app.route("/")
def inicio():
    """
    La página principal redirige a Usuarios.
    """

    return redirect(
        url_for("usuarios")
    )


@app.route("/usuarios")
def usuarios():
    """
    Muestra todos los usuarios.
    """

    lista_usuarios = Usuario.get_all()

    return render_template(
        "usuarios.html",
        usuarios=lista_usuarios
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
    Crea un nuevo usuario.
    """

    nombre = request.form.get(
        "nombre",
        ""
    ).strip()

    email = request.form.get(
        "email",
        ""
    ).strip()

    contrasena = request.form.get(
        "contrasena",
        ""
    ).strip()


    if not nombre or not email or not contrasena:

        flash(
            "Todos los campos son obligatorios.",
            "danger"
        )

        return redirect(
            url_for("usuarios")
        )


    data = {
        "nombre": nombre,
        "email": email,
        "contrasena": contrasena
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
# MOSTRAR USUARIO
# ==========================================================

@app.route(
    "/usuarios/<int:id>"
)
def mostrar_usuario(id):
    """
    Muestra un usuario y sus canciones favoritas.
    """

    data = {
        "id": id
    }


    usuario = Usuario.get_by_id_with_favorites(
        data
    )


    if usuario is None:

        return (
            "Usuario no encontrado",
            404
        )


    canciones = Cancion.get_all()


    return render_template(
        "mostrar_usuario.html",
        usuario=usuario,
        canciones=canciones
    )


# ==========================================================
# CANCIONES
# ==========================================================

@app.route("/canciones")
def canciones():
    """
    Muestra todas las canciones.
    """

    lista_canciones = Cancion.get_all()

    return render_template(
        "canciones.html",
        canciones=lista_canciones
    )


# ==========================================================
# CREAR CANCIÓN
# ==========================================================

@app.route(
    "/canciones/crear",
    methods=["POST"]
)
def crear_cancion():
    """
    Crea una nueva canción.
    """

    titulo = request.form.get(
        "titulo",
        ""
    ).strip()

    artista = request.form.get(
        "artista",
        ""
    ).strip()


    if not titulo or not artista:

        flash(
            "Título y artista son obligatorios.",
            "danger"
        )

        return redirect(
            url_for("canciones")
        )


    data = {
        "titulo": titulo,
        "artista": artista
    }


    resultado = Cancion.save(
        data
    )


    if resultado is False:

        flash(
            "No fue posible crear la canción.",
            "danger"
        )

        return redirect(
            url_for("canciones")
        )


    flash(
        "Canción creada correctamente.",
        "success"
    )


    return redirect(
        url_for("canciones")
    )


# ==========================================================
# MOSTRAR CANCIÓN
# ==========================================================

@app.route(
    "/canciones/<int:id>"
)
def mostrar_cancion(id):
    """
    Muestra una canción y los usuarios
    que la marcaron como favorita.
    """

    data = {
        "id": id
    }


    cancion = Cancion.get_by_id_with_users(
        data
    )


    if cancion is None:

        return (
            "Canción no encontrada",
            404
        )


    usuarios = Cancion.get_users_not_favorited({
        "cancion_id": id
    })


    return render_template(
        "mostrar_cancion.html",
        cancion=cancion,
        usuarios=usuarios
    )


# ==========================================================
# AGREGAR FAVORITO
# ==========================================================

@app.route(
    "/favoritos/agregar",
    methods=["POST"]
)
def agregar_favorito():
    """
    Crea una relación entre un usuario y una canción.

    El formulario indica desde qué página se realizó
    la operación mediante el campo "origen".
    """

    usuario_id_texto = request.form.get(
        "usuario_id"
    )

    cancion_id_texto = request.form.get(
        "cancion_id"
    )

    origen = request.form.get(
        "origen"
    )


    if not usuario_id_texto or not cancion_id_texto:

        flash(
            "Debes seleccionar los datos necesarios.",
            "danger"
        )

        return redirect(
            url_for("usuarios")
        )


    try:

        usuario_id = int(
            usuario_id_texto
        )

        cancion_id = int(
            cancion_id_texto
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
    # Comprobar que la canción exista.
    # ------------------------------------------------------

    cancion = Cancion.get_by_id(
        cancion_id
    )


    if cancion is None:

        flash(
            "La canción seleccionada no existe.",
            "danger"
        )

        return redirect(
            url_for("canciones")
        )


    data = {
        "usuario_id": usuario_id,
        "cancion_id": cancion_id
    }


    # ------------------------------------------------------
    # Evitar favoritos duplicados.
    # ------------------------------------------------------

    if Favorito.existe(data):

        flash(
            "Esta canción ya está entre los favoritos del usuario.",
            "warning"
        )

    else:

        resultado = Favorito.agregar(
            data
        )


        if resultado is False:

            flash(
                "No fue posible agregar el favorito.",
                "danger"
            )

        else:

            flash(
                "Favorito agregado correctamente.",
                "success"
            )


    # ------------------------------------------------------
    # Volver a la página desde donde se realizó la acción.
    # ------------------------------------------------------

    if origen == "usuario":

        return redirect(
            url_for(
                "mostrar_usuario",
                id=usuario_id
            )
        )


    if origen == "cancion":

        return redirect(
            url_for(
                "mostrar_cancion",
                id=cancion_id
            )
        )


    return redirect(
        url_for("usuarios")
    )