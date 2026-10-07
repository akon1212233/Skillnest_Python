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


from mascota import Mascota


# ==========================================================
# CREAR APLICACIÓN
# ==========================================================

app = Flask(__name__)


# ==========================================================
# READ
# MOSTRAR MASCOTAS
# ==========================================================

@app.route("/")
def index():
    """
    Recupera todas las mascotas y las envía
    a index.html.
    """

    mascotas = Mascota.get_all()


    return render_template(
        "index.html",
        mascotas=mascotas
    )


# ==========================================================
# CREATE
# CREAR MASCOTA
# ==========================================================

@app.route(
    "/crear_mascota",
    methods=["POST"]
)
def crear_mascota():
    """
    Recibe la información del formulario
    y crea una nueva mascota.
    """

    # ------------------------------------------------------
    # RECIBIR INFORMACIÓN
    # ------------------------------------------------------

    datos = {

        "nombre": request.form["nombre"],

        "tipo": request.form["tipo"],

        "color": request.form["color"]

    }


    # ------------------------------------------------------
    # ENVIAR DATOS AL MODELO
    # ------------------------------------------------------

    Mascota.save(datos)


    # ------------------------------------------------------
    # REDIRECCIONAR
    # ------------------------------------------------------
    #
    # Después de recibir un POST utilizamos redirect()
    # para volver a la ruta principal.
    #
    # Flujo:
    #
    # POST /crear_mascota
    #       ↓
    # INSERT
    #       ↓
    # redirect
    #       ↓
    # GET /
    #
    # ------------------------------------------------------

    return redirect(
        url_for("index")
    )


# ==========================================================
# EJECUTAR SERVIDOR
# ==========================================================

if __name__ == "__main__":

    app.run(debug=True)