import random
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)

# Clave obligatoria para cifrar las cookies de sesión en el navegador
app.secret_key = "clave_secreta_juego_destino"

# ==========================================
# 1. RUTA PRINCIPAL (GET)
# ==========================================
@app.route("/")
def index():
    """Muestra el formulario inicial para ingresar datos."""
    return render_template("index.html")

# ==========================================
# 2. PROCESAR DATOS (POST)
# ==========================================
@app.route("/enviar", methods=["POST"])
def enviar():
    """
    Recibe los datos mediante POST, los almacena en la sesión
    y genera la predicción aleatoria antes de redirigir.
    """
    # Almacenar datos del formulario en la sesión
    session["nombre"] = request.form.get("nombre")
    session["edad"] = request.form.get("edad")
    session["color"] = request.form.get("color")
    
    # Lista de posibles predicciones (Buena suerte vs Mala suerte)
    predicciones = [
        f"¡Grandes noticias, {session['nombre']}! El universo te depara un viaje inesperado lleno de éxito, abundancia y felicidad.",
        f"Cuidado, {session['nombre']}. Las estrellas sugieren que esta semana pisarás un chicle, se te caerá el pan por el lado de la mantequilla o perderás tus llaves.",
        f"A tus {session['edad']} años, estás a punto de descubrir un talento oculto que cambiará tu vida por completo.",
        f"El destino dice que tu color de la suerte es el {session['color']}, pero hoy es mejor que no tomes decisiones importantes basándote en él."
    ]
    
    # Seleccionar una predicción aleatoria y guardarla en la sesión
    session["prediccion_destino"] = random.choice(predicciones)
    
    # Redirección limpia para cumplir con el patrón PRG
    return redirect(url_for("futuro"))

# ==========================================
# 3. MOSTRAR PREDICCIÓN (GET)
# ==========================================
@app.route("/futuro")
def futuro():
    """Recupera la predicción guardada en sesión y la muestra dinámicamente."""
    # Si alguien intenta entrar directo sin rellenar el formulario, lo regresamos al inicio
    if "nombre" not in session:
        return redirect(url_for("index"))
        
    return render_template(
        "futuro.html",
        nombre=session.get("nombre"),
        prediccion=session.get("prediccion_destino")
    )

if __name__ == "__main__":
    app.run(debug=True)
