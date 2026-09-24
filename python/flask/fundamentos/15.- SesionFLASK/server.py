# ==========================================
# IMPORTACIONES
# ==========================================
from flask import Flask, render_template, request, redirect, url_for


# ==========================================
# CREACIÓN DE LA APLICACIÓN
# ==========================================
app = Flask(__name__)


# ==========================================
# REQUISITO 1 - RUTA PRINCIPAL
# ==========================================
@app.route("/")
def index():
    """
    Muestra el formulario de registro de producto.
    """
    return render_template("index.html")


# ==========================================
# REQUISITOS 2, 3 y 4 - PROCESAR FORMULARIO
# ==========================================
@app.route("/registrar", methods=["POST"])
def registrar():
    """
    Acepta únicamente solicitudes POST.
    Obtiene los datos del formulario y los muestra en la terminal.
    """
    
    # Requisito 3: Obtener los datos mediante request.form
    nombre = request.form["nombre"]
    precio = request.form["precio"]
    categoria = request.form["categoria"]

    # Requisito 4: Mostrar la información en la terminal
    print("============================")
    print("Producto recibido")
    print(f"Nombre: {nombre}")
    print(f"Precio: {precio}")
    print(f"Categoría: {categoria}")
    print("============================")

    # Requisito 5: Utilizar redirect()
    return redirect("/resultado")


# ==========================================
# REQUISITO 6 - MOSTRAR RESULTADO
# ==========================================
@app.route("/resultado")
def resultado():
    """
    Esta ruta es de tipo GET y confirma el procesamiento correcto.
    """
    return render_template("resultado.html")


# ==========================================
# DESAFÍO ADICIONAL - RUTA DE AYUDA
# ==========================================
@app.route("/ayuda")
def ayuda():
    """
    Ruta que explica conceptualmente el flujo de las solicitudes.
    """
    return render_template("ayuda.html")


# ==========================================
# EJECUTAR SERVIDOR
# ==========================================
if __name__ == "__main__":
    app.run(debug=True)
