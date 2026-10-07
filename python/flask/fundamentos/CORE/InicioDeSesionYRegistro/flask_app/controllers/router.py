from flask import (
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)
import re
from datetime import datetime
from flask_app import bcrypt
from flask_app import app
from flask_app.models.usuario import Usuario

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
LETRAS_REGEX = re.compile(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$')

@app.route("/")
def index():
    if 'usuario_id' in session:
        return redirect(url_for('usuario'))
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    nombre = request.form.get("nombre", "").strip()
    apellido = request.form.get("apellido", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "").strip()
    conf_password = request.form.get("conf_password", "").strip()
    fecha_nacimiento = request.form.get("fecha_nacimiento", "").strip()

    errores = 0

    if len(nombre) < 2 or not LETRAS_REGEX.match(nombre):
        flash("El nombre debe tener al menos 2 caracteres y contener solo letras.", "register")
        errores += 1

    if len(apellido) < 2 or not LETRAS_REGEX.match(apellido):
        flash("El apellido debe tener al menos 2 caracteres y contener solo letras.", "register")
        errores += 1

    if not EMAIL_REGEX.match(email):
        flash("Formato de correo electrónico inválido.", "register")
        errores += 1
    else:
        if Usuario.get_user_by_email(email):
            flash("El correo electrónico ya se encuentra registrado.", "register")
            errores += 1

    if len(password) < 8:
        flash("La contraseña debe tener al menos 8 caracteres.", "register")
        errores += 1
    elif not any(char.isupper() for char in password) or not any(char.isdigit() for char in password):
        flash("La contraseña debe incluir al menos una letra mayúscula y un número.", "register")
        errores += 1

    if password != conf_password:
        flash("La confirmación de la contraseña no coincide.", "register")
        errores += 1

    if not fecha_nacimiento:
        flash("La fecha de nacimiento es obligatoria.", "register")
        errores += 1
    else:
        try:
            fecha_nac = datetime.strptime(fecha_nacimiento, "%Y-%m-%d")
            hoy = datetime.today()
            edad = hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))
            if edad < 18:
                flash("Debes ser mayor de edad (18 años) para registrarte.", "register")
                errores += 1
        except ValueError:
            flash("Fecha de nacimiento inválida.", "register")
            errores += 1

    if errores > 0:
        return redirect(url_for('index'))

    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    datos = {
        "nombre": nombre,
        "apellido": apellido,
        "email": email,
        "password_hash": password_hash,
        "fecha_nacimiento": fecha_nacimiento
    }
    
    usuario_id = Usuario.save(datos)
    session['usuario_id'] = usuario_id
    flash("¡Registro exitoso!", "success_msg")
    return redirect(url_for('usuario'))

@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "").strip()
    
    if not email or not password:
        flash("Por favor, llena todos los campos.", "login")
        return redirect(url_for('index'))

    usuario_encontrado = Usuario.get_user_by_email(email)
    
    if usuario_encontrado and bcrypt.check_password_hash(usuario_encontrado['password_hash'], password):
        session['usuario_id'] = usuario_encontrado['idUsuario']
        return redirect(url_for('usuario'))
    
    flash("Email o contraseña incorrectos.", "login")
    return redirect(url_for('index'))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route("/usuario")
def usuario():
    if 'usuario_id' not in session:
        flash("Debes iniciar sesión para acceder a esta página.", "login")
        return redirect(url_for('index'))

    usuario_data = Usuario.get_user_by_id(session['usuario_id'])
    if not usuario_data:
        session.clear()
        return redirect(url_for('index'))
        
    return render_template("usuario.html", usuario=usuario_data)
