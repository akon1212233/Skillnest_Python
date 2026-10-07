from flask_app import app

from flask import render_template, request, redirect, url_for

from flask_app.models.usuario import Usuario


@app.route("/usuarios")
def usuarios():
    lista_usuarios = Usuario.get_all()

    return render_template(
        "index.html",
        usuarios=lista_usuarios
    )


@app.route("/usuarios/nuevo")
def nuevo():
    return render_template("nuevo.html")


@app.route("/usuarios/crear", methods=["POST"])
def crear():
    data = {
        "nombre": request.form["nombre"].strip(),
        "apellido": request.form["apellido"].strip(),
        "email": request.form["email"].strip()
    }

    if not data["nombre"] or not data["apellido"] or not data["email"]:
        return render_template(
            "nuevo.html",
            error="Todos los campos son obligatorios.",
            datos=data
        )

    resultado = Usuario.save(data)

    if resultado is False:
        return render_template(
            "nuevo.html",
            error="No fue posible crear el usuario.",
            datos=data
        )

    return redirect(url_for("usuarios"))


@app.route("/usuarios/<int:id>")
def detalle(id):
    usuario = Usuario.get_by_id(id)

    if usuario is None:
        return "Usuario no encontrado", 404

    return render_template(
        "detalle.html",
        usuario=usuario
    )


@app.route("/usuarios/editar/<int:id>")
def editar(id):
    usuario = Usuario.get_by_id(id)

    if usuario is None:
        return "Usuario no encontrado", 404

    return render_template(
        "editar.html",
        usuario=usuario
    )


@app.route("/usuarios/<int:id>/actualizar", methods=["POST"])
def actualizar(id):
    data = {
        "id": id,
        "nombre": request.form["nombre"].strip(),
        "apellido": request.form["apellido"].strip(),
        "email": request.form["email"].strip()
    }

    if not data["nombre"] or not data["apellido"] or not data["email"]:
        usuario = Usuario.get_by_id(id)

        return render_template(
            "editar.html",
            usuario=usuario,
            error="Todos los campos son obligatorios."
        )

    resultado = Usuario.update(data)

    if resultado is False:
        usuario = Usuario.get_by_id(id)

        return render_template(
            "editar.html",
            usuario=usuario,
            error="No fue posible actualizar el usuario."
        )

    return redirect(url_for("usuarios"))


@app.route("/usuarios/borrar/<int:id>")
def borrar(id):
    data = {
        "id": id
    }

    resultado = Usuario.delete(data)

    if resultado is False:
        return "No fue posible eliminar el usuario.", 500

    return redirect(url_for("usuarios"))
