from flask import render_template, redirect, request, session, flash
from flask_app import app, bcrypt
from flask_app.models.usuario import Usuario

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/registro")
def registro():
    return render_template("registro.html")

@app.route("/registrar", methods=["POST"])
def registrar():
    datos = {
        "nombre": request.form["nombre"].strip(),
        "apellido": request.form["apellido"].strip(),
        "email": request.form["email"].strip().lower(),
        "password": request.form["password"]
    }

    if not Usuario.validar_usuario(datos):
        return redirect("/registro")

    if Usuario.existe_email({"email": datos["email"]}):
        flash("El email ya está registrado.", "email")
        return redirect("/registro")

    password_hash = bcrypt.generate_password_hash(
        datos["password"]
    ).decode("utf-8")

    datos["password"] = password_hash

    usuario_id = Usuario.guardar(datos)

    if not usuario_id:
        flash("No fue posible registrar el usuario.", "general")
        return redirect("/registro")

    session["usuario_id"] = usuario_id

    return redirect("/dashboard")

@app.route("/login", methods=["POST"])
def login():
    datos = {
        "email": request.form["email"].strip().lower(),
        "password": request.form["password"]
    }

    usuario = Usuario.buscar_por_email({
        "email": datos["email"]
    })

    if not usuario:
        flash("Email o contraseña incorrectos.", "login")
        return redirect("/")

    if not bcrypt.check_password_hash(
        usuario.password,
        datos["password"]
    ):
        flash("Email o contraseña incorrectos.", "login")
        return redirect("/")

    session["usuario_id"] = usuario.id

    return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
    if "usuario_id" not in session:
        flash("Debes iniciar sesión.", "login")
        return redirect("/")

    usuario = Usuario.buscar_por_id({
        "id": session["usuario_id"]
    })

    return render_template(
        "dashboard.html",
        usuario=usuario
    )

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
