# ==========================================
# IMPORTACIONES
# ==========================================
from flask import Flask, render_template, request, redirect

# ==========================================
# CREACIÓN DE LA APLICACIÓN
# ==========================================
app = Flask(__name__)

# ==========================================
# RUTA PRINCIPAL
# ==========================================
@app.route("/")
def index():
    """
    Muestra el formulario de creación de usuario.
    """
    return render_template("index.html")

# ==========================================
# PROCESAR FORMULARIO
# ==========================================
@app.route("/crear_usuario", methods=["POST"])
def crear_usuario():
    """
    Recibe la información enviada mediante POST.

    Esta función se encarga de procesar los datos
    antes de realizar la redirección.
    """

    # ------------------------------------------
    # Obtener los datos enviados por el formulario
    # ------------------------------------------
    nombre = request.form["nombre"]
    email = request.form["email"]

    # ------------------------------------------
    # Mostrar los datos en la terminal
    # ------------------------------------------
    print("===================================")
    print("Información recibida")
    print(f"Nombre: {nombre}")
    print(f"Email : {email}")
    print("===================================")

    # ------------------------------------------
    # Redireccionar al usuario
    # ------------------------------------------
    return redirect("/mostrar_usuario")

# ==========================================
# MOSTRAR RESULTADO
# ==========================================
@app.route("/mostrar_usuario")
def mostrar_usuario():
    """
    Esta ruta recibe una solicitud GET después
    de la redirección.
    """
    print("Usuario redirigido")
    # ------------------------------------------
    # request.form estará vacío
    # ------------------------------------------
    print(request.form)

    # ------------------------------------------
    # Mostrar la plantilla
    # ------------------------------------------
    return render_template("mostrar.html")

# ==========================================
# EJECUTAR SERVIDOR
# ==========================================
if __name__ == "__main__":
    app.run(debug=True)