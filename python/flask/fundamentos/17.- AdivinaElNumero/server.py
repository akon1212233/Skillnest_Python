# ==========================================================
# ADIVINA EL NÚMERO
# Juego desarrollado con Flask
# ==========================================================


# ----------------------------------------------------------
# IMPORTACIONES
# ----------------------------------------------------------

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session
)

import random


# ----------------------------------------------------------
# CREAR APLICACIÓN
# ----------------------------------------------------------

app = Flask(__name__)


# ----------------------------------------------------------
# SECRET KEY
# ----------------------------------------------------------
#
# Flask necesita una clave secreta para utilizar session.
#
# Esta clave permite firmar y proteger la información
# relacionada con la sesión del usuario.
#
# En una aplicación real debe mantenerse fuera del código
# fuente, por ejemplo utilizando variables de entorno.
#
# Para esta práctica utilizaremos una clave sencilla.
# ----------------------------------------------------------

app.secret_key = "clave-secreta-adivina-numero"


# ----------------------------------------------------------
# RUTA PRINCIPAL
# ----------------------------------------------------------

@app.route("/")
def index():
    """
    Muestra la página principal del juego.

    Si todavía no existe un número secreto dentro
    de la sesión, lo generamos aleatoriamente.

    También inicializamos la cantidad de intentos
    y un mensaje para el usuario.
    """

    # ------------------------------------------------------
    # INICIALIZAR NÚMERO SECRETO
    # ------------------------------------------------------

    if "numero_secreto" not in session:

        session["numero_secreto"] = random.randint(1, 10)


    # ------------------------------------------------------
    # INICIALIZAR INTENTOS
    # ------------------------------------------------------

    if "intentos" not in session:

        session["intentos"] = 0


    # ------------------------------------------------------
    # INICIALIZAR MENSAJE
    # ------------------------------------------------------

    if "mensaje" not in session:

        session["mensaje"] = (
            "Adivina un número entre 1 y 10."
        )


    # ------------------------------------------------------
    # INICIALIZAR ESTADO DEL JUEGO
    # ------------------------------------------------------

    if "resultado" not in session:

        session["resultado"] = ""


    # ------------------------------------------------------
    # ENVIAR INFORMACIÓN A LA PLANTILLA
    # ------------------------------------------------------

    mensaje = session["mensaje"]

    resultado = session["resultado"]

    intentos = session["intentos"]


    # ------------------------------------------------------
    # MOSTRAR PÁGINA
    # ------------------------------------------------------

    return render_template(
        "index.html",
        mensaje=mensaje,
        resultado=resultado,
        intentos=intentos
    )


# ----------------------------------------------------------
# PROCESAR INTENTO
# ----------------------------------------------------------

@app.route("/adivinar", methods=["POST"])
def adivinar():
    """
    Procesa el número ingresado por el usuario
    y lo compara con el número secreto.
    """

    # ------------------------------------------------------
    # RECIBIR DATO DEL FORMULARIO
    # ------------------------------------------------------

    numero = int(request.form["numero"])


    # ------------------------------------------------------
    # OBTENER NÚMERO SECRETO
    # ------------------------------------------------------

    numero_secreto = session["numero_secreto"]


    # ------------------------------------------------------
    # AUMENTAR INTENTOS
    # ------------------------------------------------------

    session["intentos"] += 1


    # ------------------------------------------------------
    # COMPARAR NÚMEROS
    # ------------------------------------------------------

    if numero < numero_secreto:

        session["mensaje"] = (
            f"El número secreto es mayor que {numero}."
        )

        session["resultado"] = "mayor"


    elif numero > numero_secreto:

        session["mensaje"] = (
            f"El número secreto es menor que {numero}."
        )

        session["resultado"] = "menor"


    else:

        session["mensaje"] = (
            f"¡Correcto! El número secreto era {numero_secreto}."
        )

        session["resultado"] = "correcto"


    # ------------------------------------------------------
    # VOLVER A LA PÁGINA PRINCIPAL
    # ------------------------------------------------------
    #
    # Aplicamos POST → Redirect → GET.
    #
    # El formulario se procesa aquí y luego el navegador
    # vuelve a realizar una solicitud GET hacia "/".
    # ------------------------------------------------------

    return redirect(url_for("index"))


# ----------------------------------------------------------
# REINICIAR JUEGO
# ----------------------------------------------------------

@app.route("/reiniciar")
def reiniciar():
    """
    Elimina la información actual de la sesión
    y redirige al inicio.

    Al volver a "/", se generará un nuevo número secreto.
    """

    # ------------------------------------------------------
    # ELIMINAR SESIÓN
    # ------------------------------------------------------

    session.clear()


    # ------------------------------------------------------
    # VOLVER AL INICIO
    # ------------------------------------------------------

    return redirect(url_for("index"))


# ----------------------------------------------------------
# EJECUTAR SERVIDOR
# ----------------------------------------------------------

if __name__ == "__main__":

    app.run(debug=True)