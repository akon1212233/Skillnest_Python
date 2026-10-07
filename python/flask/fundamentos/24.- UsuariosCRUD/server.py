# ==========================================================
# SERVIDOR FLASK — CRUD USUARIOS
# ==========================================================

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for
)


from controllers.usuario import Usuario


# ==========================================================
# CREAR APLICACIÓN
# ==========================================================

app = Flask(__name__)


# ==========================================================
# READ
# LISTADO DE USUARIOS
# ==========================================================

@app.route("/usuarios")
def usuarios():
    """
    Muestra todos los usuarios.
    """

    todos_los_usuarios = Usuario.get_all()


    return render_template(
        "usuarios.html",
        usuarios=todos_los_usuarios
    )


# ==========================================================
# CREATE
# MOSTRAR FORMULARIO
# ==========================================================

@app.route("/usuarios/nuevo")
def nuevo_usuario():
    """
    Muestra el formulario para crear un usuario.
    """

    return render_template(
        "usuario_nuevo.html"
    )


# ==========================================================
# CREATE
# PROCESAR FORMULARIO
# ==========================================================

@app.route(
    "/usuarios/crear",
    methods=["POST"]
)
def crear_usuario():
    """
    Recibe y guarda los datos del formulario.
    """

    nombre = request.form["nombre"].strip()

    apellido = request.form["apellido"].strip()

    email = request.form["email"].strip()


    if not nombre or not apellido or not email:

        return render_template(
            "usuario_nuevo.html",
            error="Todos los campos son obligatorios."
        )


    data = {
        "nombre": nombre,
        "apellido": apellido,
        "email": email
    }


    resultado = Usuario.save(data)


    if resultado is False:

        return render_template(
            "usuario_nuevo.html",
            error="No fue posible crear el usuario."
        )


    return redirect(
        url_for("usuarios")
    )


# ==========================================================
# READ
# VER USUARIO
# ==========================================================

@app.route("/usuarios/<int:id>")
def ver_usuario(id):
    """
    Muestra la información completa de un usuario.
    """

    usuario = Usuario.get_by_id(id)


    if usuario is None:

        return "Usuario no encontrado", 404


    return render_template(
        "usuario.html",
        usuario=usuario
    )


# ==========================================================
# UPDATE
# MOSTRAR FORMULARIO DE EDICIÓN
# ==========================================================

@app.route("/usuarios/editar/<int:id>")
def editar_usuario(id):
    """
    Recupera un usuario y carga sus datos
    dentro del formulario de edición.
    """

    usuario = Usuario.get_by_id(id)


    if usuario is None:

        return "Usuario no encontrado", 404


    return render_template(
        "usuario_editar.html",
        usuario=usuario
    )


# ==========================================================
# UPDATE
# PROCESAR EDICIÓN
# ==========================================================

@app.route(
    "/usuarios/<int:id>/actualizar",
    methods=["POST"]
)
def actualizar_usuario(id):
    """
    Recibe los nuevos datos y actualiza
    el usuario correspondiente.
    """

    nombre = request.form["nombre"].strip()

    apellido = request.form["apellido"].strip()

    email = request.form["email"].strip()


    if not nombre or not apellido or not email:

        usuario = Usuario.get_by_id(id)


        return render_template(
            "usuario_editar.html",
            usuario=usuario,
            error="Todos los campos son obligatorios."
        )


    data = {
        "id": id,
        "nombre": nombre,
        "apellido": apellido,
        "email": email
    }


    resultado = Usuario.update(data)


    if resultado is False:

        usuario = Usuario.get_by_id(id)


        return render_template(
            "usuario_editar.html",
            usuario=usuario,
            error="No fue posible actualizar el usuario."
        )


    return redirect(
        url_for("usuarios")
    )


# ==========================================================
# DELETE
# BORRAR USUARIO
# ==========================================================
#
# Para seguir la estructura original de la actividad,
# utilizaremos una ruta GET para el enlace "Borrar".
#
# En aplicaciones reales es preferible utilizar POST
# o DELETE para operaciones destructivas.
# ==========================================================

@app.route("/usuarios/borrar/<int:id>")
def borrar_usuario(id):
    """
    Elimina el usuario correspondiente al ID.
    """

    resultado = Usuario.delete(id)


    if resultado is False:

        return "No fue posible eliminar el usuario.", 500


    return redirect(
        url_for("usuarios")
    )


# ==========================================================
# EJECUTAR SERVIDOR
# ==========================================================

if __name__ == "__main__":

    app.run(debug=True)