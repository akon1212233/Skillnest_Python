from flask import render_template, request, redirect, url_for

from academia import app
from academia.models.taller import Taller


# ---------------- PÁGINA PRINCIPAL ----------------
@app.route("/")
def inicio():
    """Redirige la raíz hacia la página de talleres."""
    return redirect(url_for("talleres"))


# ---------------- LISTAR TALLERES ----------------
@app.route("/talleres")
def talleres():
    """Obtiene y muestra todos los talleres."""
    todos = Taller.obtener_todos()
    return render_template("talleres.html", talleres=todos)


# ---------------- CREAR TALLER ----------------
@app.route("/talleres/crear", methods=["POST"])
def crear_taller():
    """Recibe el título del taller y crea el registro."""
    titulo = request.form.get("titulo", "").strip()

    if titulo:
        Taller.guardar({"titulo": titulo})

    return redirect(url_for("talleres"))


# ---------------- MOSTRAR TALLER ----------------
@app.route("/talleres/<int:id>")
def mostrar_taller(id):
    """Obtiene un taller y sus alumnos."""
    taller = Taller.obtener_con_alumnos(id)

    if taller is None:
        return redirect(url_for("talleres"))

    return render_template("mostrar_taller.html", taller=taller)
