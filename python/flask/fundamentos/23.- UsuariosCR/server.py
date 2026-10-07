# ==========================================================
# SERVIDOR FLASK
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
    Recupera todos los usuarios desde MySQL
    y los envía a la plantilla.
    """

    # ------------------------------------------------------
    # CONSULTAR MODELO
    # ------------------------------------------------------

    todos_los_usuarios = Usuario.get_all()


    # ------------------------------------------------------
    # ENVIAR RESULTADO A JINJA2
    # ------------------------------------------------------

    return render_template(
        "usuarios.html",
        usuarios=todos_los_usuarios
    )


# ==========================================================
# MOSTRAR FORMULARIO
# ==========================================================

@app.route("/usuarios/nuevo")
def nuevo_usuario():
    """
    Muestra el formulario de creación.
    """

    return render_template(
        "usuario_nuevo.html"
    )


# ==========================================================
# CREATE
# CREAR USUARIO
# ==========================================================

@app.route("/usuarios/crear", methods=["POST"])
def crear_usuario():
    """
    Recibe la información del formulario
    y crea un nuevo usuario.
    """

    # ------------------------------------------------------
    # RECUPERAR DATOS DEL FORMULARIO
    # ------------------------------------------------------

    nombre = request.form["nombre"].strip()

    apellido = request.form["apellido"].strip()

    email = request.form["email"].strip()


    # ------------------------------------------------------
    # VALIDACIÓN BÁSICA
    # ------------------------------------------------------

    if not nombre or not apellido or not email:

        return render_template(
            "usuario_nuevo.html",
            error="Todos los campos son obligatorios."
        )


    # ------------------------------------------------------
    # CREAR DICCIONARIO
    # ------------------------------------------------------

    data = {

        "nombre": nombre,

        "apellido": apellido,

        "email": email

    }


    # ------------------------------------------------------
    # CREAR USUARIO
    # ------------------------------------------------------

    resultado = Usuario.save(data)


    # ------------------------------------------------------
    # COMPROBAR ERROR
    # ------------------------------------------------------

    if resultado is False:

        return render_template(
            "usuario_nuevo.html",
            error="No fue posible crear el usuario."
        )


    # ------------------------------------------------------
    # REDIRECT
    # ------------------------------------------------------
    #
    # Después de crear el usuario aplicamos:
    #
    # POST → Redirect → GET
    #
    # ------------------------------------------------------

    return redirect(
        url_for("usuarios")
    )


# ==========================================================
# EJECUTAR SERVIDOR
# ==========================================================

if __name__ == "__main__":

    app.run(debug=True)
