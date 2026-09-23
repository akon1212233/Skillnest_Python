# ==========================================================
# SERVIDOR FLASK
# ==========================================================

from flask import Flask, render_template

from Controllers.mascota import Mascota


# ==========================================================
# CREAR APLICACIÓN
# ==========================================================

app = Flask(__name__)


# ==========================================================
# RUTA PRINCIPAL
# ==========================================================

@app.route("/")
def index():
    """
    Consulta todas las mascotas y las envía
    hacia la plantilla index.html.
    """

    # ------------------------------------------------------
    # OBTENER MASCOTAS DESDE MYSQL
    # ------------------------------------------------------

    mascotas = Mascota.get_all()


    # ------------------------------------------------------
    # MOSTRAR RESULTADOS EN TERMINAL
    # ------------------------------------------------------

    print(mascotas)


    # ------------------------------------------------------
    # ENVIAR DATOS A JINJA2
    # ------------------------------------------------------

    return render_template(

        "index.html",

        todas_mascotas=mascotas

    )


# ==========================================================
# EJECUTAR SERVIDOR
# ==========================================================

if __name__ == "__main__":

    app.run(debug=True)