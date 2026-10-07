from datetime import date, datetime
from functools import wraps

from flask import flash, redirect, render_template, request, session, url_for

from flask_app import app, bcrypt
from flask_app.models.libros import Libro
from flask_app.models.usuarios import Usuario

GENEROS = ["Novela", "Fábula", "Ciencia Ficción", "Romance", "Desarrollo Personal", "Terror", "Misterio", "Historia", "Otro"]


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            flash("Debes iniciar sesión para continuar.", "warning")
            return redirect(url_for("auth"))
        return view(*args, **kwargs)
    return wrapped


def validar_libro(form):
    titulo = form.get("titulo", "").strip()
    autor = form.get("autor", "").strip()
    genero = form.get("genero", "").strip()
    fecha_publicacion = form.get("fecha_publicacion", "").strip()
    descripcion = form.get("descripcion", "").strip()
    errores = []

    if len(titulo) < 2:
        errores.append("El título debe tener al menos 2 caracteres.")
    if not autor:
        errores.append("El autor es obligatorio.")
    if genero not in GENEROS:
        errores.append("Debes seleccionar un género válido.")
    try:
        fecha = datetime.strptime(fecha_publicacion, "%Y-%m-%d").date()
        if fecha > date.today():
            errores.append("La fecha de publicación no puede ser futura.")
    except ValueError:
        fecha = None
        errores.append("La fecha de publicación no es válida.")
    if len(descripcion) < 10:
        errores.append("La descripción debe tener al menos 10 caracteres.")

    return errores, {
        "titulo": titulo,
        "autor": autor,
        "genero": genero,
        "fecha_publicacion": fecha_publicacion,
        "descripcion": descripcion,
    }, fecha


@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("libros"))
    return redirect(url_for("auth"))


@app.route("/auth")
def auth():
    if "user_id" in session:
        return redirect(url_for("libros"))
    return render_template("auth.html")


@app.post("/registro")
def registro():
    nombre = request.form.get("nombre", "").strip()
    apellido = request.form.get("apellido", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    confirm = request.form.get("confirm_password", "")

    errores = []
    if len(nombre) < 2 or len(apellido) < 2:
        errores.append("Nombre y apellido deben tener al menos 2 caracteres.")
    if "@" not in email or "." not in email.split("@")[-1]:
        errores.append("Ingresa un correo válido.")
    if len(password) < 6:
        errores.append("La contraseña debe tener al menos 6 caracteres.")
    if password != confirm:
        errores.append("Las contraseñas no coinciden.")
    if Usuario.buscar_por_email(email):
        errores.append("El correo ya está registrado.")

    if errores:
        for error in errores:
            flash(error, "danger")
        return redirect(url_for("auth"))

    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    user_id = Usuario.crear({
        "nombre": nombre,
        "apellido": apellido,
        "email": email,
        "password": password_hash,
    })
    session["user_id"] = user_id
    session["user_name"] = nombre
    flash("Cuenta creada correctamente. ¡Bienvenido a BookHub!", "success")
    return redirect(url_for("libros"))


@app.post("/login")
def login():
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    user = Usuario.buscar_por_email(email)

    if not user or not bcrypt.check_password_hash(user["password"], password):
        flash("Correo o contraseña incorrectos.", "danger")
        return redirect(url_for("auth"))

    session.clear()
    session["user_id"] = user["id"]
    session["user_name"] = user["nombre"]
    flash("Sesión iniciada correctamente.", "success")
    return redirect(url_for("libros"))


@app.get("/logout")
def logout():
    session.clear()
    flash("Has cerrado sesión.", "info")
    return redirect(url_for("auth"))


@app.get("/libros")
@login_required
def libros():
    mis_libros = Libro.de_usuario(session["user_id"])
    comunidad = Libro.todos()
    return render_template("list_book.html", mis_libros=mis_libros, comunidad=comunidad)


@app.get("/libros/nuevo")
@login_required
def nuevo_libro():
    return render_template("new_book.html", generos=GENEROS, libro=None)


@app.post("/libros/nuevo")
@login_required
def crear_libro():
    errores, data, fecha = validar_libro(request.form)
    if errores:
        for error in errores:
            flash(error, "danger")
        return render_template("new_book.html", generos=GENEROS, libro=data)

    data["fecha_publicacion"] = fecha
    data["usuario_id"] = session["user_id"]
    Libro.crear(data)
    flash("Libro creado correctamente.", "success")
    return redirect(url_for("libros"))


@app.get("/libros/<int:libro_id>")
@login_required
def detalle_libro(libro_id):
    libro = Libro.por_id(libro_id)
    if not libro:
        flash("El libro no existe.", "danger")
        return redirect(url_for("libros"))
    favoritos = Libro.favoritos_de_libro(libro_id)
    es_favorito = Libro.tiene_favorito(session["user_id"], libro_id) is not None
    return render_template("descripcion.html", libro=libro, favoritos=favoritos, es_favorito=es_favorito)


@app.get("/libros/editar/<int:libro_id>")
@login_required
def editar_libro(libro_id):
    libro = Libro.por_id(libro_id)
    if not libro or libro["usuario_id"] != session["user_id"]:
        flash("Solo puedes editar tus propios libros.", "danger")
        return redirect(url_for("libros"))
    return render_template("edit_book.html", generos=GENEROS, libro=libro)


@app.post("/libros/editar/<int:libro_id>")
@login_required
def actualizar_libro(libro_id):
    libro = Libro.por_id(libro_id)
    if not libro or libro["usuario_id"] != session["user_id"]:
        flash("Solo puedes editar tus propios libros.", "danger")
        return redirect(url_for("libros"))

    errores, data, fecha = validar_libro(request.form)
    if errores:
        for error in errores:
            flash(error, "danger")
        data["id"] = libro_id
        return render_template("edit_book.html", generos=GENEROS, libro=data)

    data["fecha_publicacion"] = fecha
    Libro.actualizar(libro_id, session["user_id"], data)
    flash("Libro actualizado correctamente.", "success")
    return redirect(url_for("detalle_libro", libro_id=libro_id))


@app.post("/libros/eliminar/<int:libro_id>")
@login_required
def eliminar_libro(libro_id):
    libro = Libro.por_id(libro_id)
    if not libro or libro["usuario_id"] != session["user_id"]:
        flash("No puedes eliminar un libro que no te pertenece.", "danger")
        return redirect(url_for("libros"))
    Libro.eliminar(libro_id, session["user_id"])
    flash("Libro eliminado correctamente.", "success")
    return redirect(url_for("libros"))


@app.post("/libros/<int:libro_id>/favorito")
@login_required
def favorito(libro_id):
    if not Libro.por_id(libro_id):
        flash("El libro no existe.", "danger")
        return redirect(url_for("libros"))
    if Libro.tiene_favorito(session["user_id"], libro_id):
        Libro.quitar_favorito(session["user_id"], libro_id)
        flash("Libro eliminado de tus favoritos.", "info")
    else:
        Libro.agregar_favorito(session["user_id"], libro_id)
        flash("Libro agregado a tus favoritos.", "success")
    return redirect(url_for("detalle_libro", libro_id=libro_id))


@app.get("/favoritos")
@login_required
def favoritos():
    libros_favoritos = Libro.favoritos_de_usuario(session["user_id"])
    return render_template("favorites_book.html", libros=libros_favoritos)
