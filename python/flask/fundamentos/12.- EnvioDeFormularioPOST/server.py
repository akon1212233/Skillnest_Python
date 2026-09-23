"""
===========================================
Formulario de Prueba
===========================================

En esta aplicación aprenderemos cómo
recibir información enviada desde un
formulario HTML utilizando solicitudes POST.
"""

# ==========================================
# Importaciones
# ==========================================

from flask import (Flask,render_template,request,redirect)

# ==========================================
# Crear aplicación Flask
# ==========================================

app = Flask(__name__)

# ==========================================
# Ruta principal
# ==========================================

@app.route("/")
def index():
    return render_template("index.html")


# ==========================================
# Procesar formulario
# ==========================================

@app.route("/crear_usuario", methods=["POST"])
def crear_usuario():
    """
    Procesa la información enviada desde el formulario.
    """

    # ==========================================
    # Obtener la información enviada
    # ==========================================

    nombre = request.form["nombre"]
    email = request.form["email"]
    edad = request.form["edad"]
    ciudad = request.form["ciudad"]
    telefono = request.form["telefono"]

    # ==========================================
    # Mostrar información en la terminal
    # ==========================================

    print("====================================")
    print("Nuevo usuario recibido")
    print(f"Nombre  : {nombre}")
    print(f"Correo  : {email}")
    print(f"Edad    : {edad}")
    print(f"Ciudad  : {ciudad}")
    print(f"Telefono: {telefono.replace(" ","")}") #.replace para eliminar espacios
    print("====================================")

    # ==========================================
    # Enviar la información a una nueva plantilla
    # ==========================================

    return render_template(
        "usuario.html",
        nombre=nombre,
        email=email,
        telefono=telefono
    )


# ==========================================
# Ejecutar servidor
# ==========================================

if __name__ == "__main__":
    app.run(debug=True)