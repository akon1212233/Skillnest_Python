from flask import render_template, request, redirect, url_for

from academia import app
from academia.models.taller import Taller
from academia.models.alumno import Alumno


# ---------------- FORMULARIO NUEVO ALUMNO ----------------
@app.route("/alumnos/nuevo")
def nuevo_alumno():
    """Carga los talleres para el <select> del formulario."""
    return render_template("nuevo_alumno.html", talleres=Taller.obtener_todos())


# ---------------- CREAR ALUMNO ----------------
@app.route("/alumnos/crear", methods=["POST"])
def crear_alumno():
    """Recibe el formulario y crea un alumno."""
    nombre = request.form.get("nombre", "").strip()
    apellido = request.form.get("apellido", "").strip()
    edad = request.form.get("edad", "").strip()
    taller_id = request.form.get("taller_id", "").strip()

    if not (nombre and apellido and edad and taller_id):
        return redirect(url_for("nuevo_alumno"))

    try:
        edad = int(edad)
        taller_id = int(taller_id)
    except ValueError:
        return redirect(url_for("nuevo_alumno"))

    Alumno.guardar({
        "nombre": nombre,
        "apellido": apellido,
        "edad": edad,
        "taller_id": taller_id,
    })

    return redirect(url_for("talleres"))
