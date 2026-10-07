import random
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)

# Clave obligatoria para cifrar las cookies de sesión en el navegador
app.secret_key = "clave_secreta_juego_destino"

# ==========================================
# DATOS DEL ORÁCULO
# ==========================================

# Significados de colores. Si el color ingresado no está en la lista,
# se usa el mensaje y el tono por defecto (DEFAULT_COLOR).
COLOR_MEANINGS = {
    "rojo":     {"hex": "#dc2626", "meaning": "pasión y energía"},
    "azul":     {"hex": "#2563eb", "meaning": "calma y sabiduría"},
    "verde":    {"hex": "#16a34a", "meaning": "crecimiento y esperanza"},
    "amarillo": {"hex": "#f59e0b", "meaning": "alegría y optimismo"},
    "morado":   {"hex": "#7c3aed", "meaning": "misterio y espiritualidad"},
    "purpura":  {"hex": "#7c3aed", "meaning": "misterio y espiritualidad"},
    "naranja":  {"hex": "#f97316", "meaning": "creatividad y entusiasmo"},
    "rosado":   {"hex": "#ec4899", "meaning": "ternura y compasión"},
    "rosa":     {"hex": "#ec4899", "meaning": "ternura y compasión"},
    "negro":    {"hex": "#111827", "meaning": "elegancia y protección"},
    "blanco":   {"hex": "#e5e7eb", "meaning": "pureza y nuevos comienzos"},
    "gris":     {"hex": "#6b7280", "meaning": "equilibrio y neutralidad"},
    "celeste":  {"hex": "#38bdf8", "meaning": "tranquilidad y claridad"},
    "cafe":     {"hex": "#78350f", "meaning": "estabilidad y raíces firmes"},
    "marron":   {"hex": "#78350f", "meaning": "estabilidad y raíces firmes"},
    "dorado":   {"hex": "#d4af37", "meaning": "abundancia y éxito"},
    "plateado": {"hex": "#c0c0c0", "meaning": "intuición y sensibilidad"},
    "turquesa": {"hex": "#14b8a6", "meaning": "sanación y comunicación"},
}
DEFAULT_COLOR = {"hex": "#9ca3af", "meaning": "misterio y descubrimiento"}

# Significados de animales. Si el animal ingresado no está en la lista,
# se usa el mensaje por defecto (DEFAULT_ANIMAL).
ANIMAL_MEANINGS = {
    "perro":    "lealtad y compañía",
    "gato":     "independencia y misterio",
    "aguila":   "visión y libertad",
    "leon":     "coraje y liderazgo",
    "delfin":   "inteligencia y alegría",
    "lobo":     "instinto y lealtad de manada",
    "tigre":    "fuerza y pasión",
    "elefante": "sabiduría y memoria",
    "mariposa": "transformación y renovación",
    "buho":     "sabiduría oculta",
    "caballo":  "libertad y fuerza",
    "conejo":   "suerte y fertilidad",
}
DEFAULT_ANIMAL = "independencia y misterio"

# Predicciones aleatorias que puede recibir el usuario.
PREDICCIONES = [
    "Encontrarás el verdadero amor en los próximos meses. Tu corazón se llenará de alegría.",
    "Una gran oportunidad profesional está por llegar. Mantente atento a las señales.",
    "Un viaje inesperado cambiará tu forma de ver el mundo.",
    "El dinero fluirá hacia ti si mantienes la paciencia y la disciplina.",
    "Una amistad del pasado volverá a tu vida con buenas noticias.",
    "Tu creatividad estará en su punto más alto; es momento de crear algo nuevo.",
]

# Mensajes según rango de edad.
def mensaje_por_edad(edad):
    if edad < 12:
        return f"A tus {edad} años, la vida te tiene preparadas aventuras llenas de curiosidad y descubrimiento."
    if edad < 18:
        return f"A tus {edad} años, estás formando el camino que definirá tu futuro."
    if edad < 26:
        return f"A tus {edad} años, estás en un momento favorable para aprovechar nuevas oportunidades."
    if edad < 41:
        return f"A tus {edad} años, tu experiencia y energía se combinan para abrir nuevas puertas."
    if edad < 61:
        return f"A tus {edad} años, la sabiduría acumulada te guía hacia decisiones acertadas."
    return f"A tus {edad} años, tu experiencia es un faro que ilumina el camino de quienes te rodean."


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
    session["animal"] = request.form.get("animal")

    # Seleccionar una predicción aleatoria y un número de la suerte
    session["prediccion_destino"] = random.choice(PREDICCIONES)
    session["numero_suerte"] = random.randint(1, 99)

    # Redirección limpia para cumplir con el patrón PRG
    return redirect(url_for("futuro"))

# ==========================================
# 3. MOSTRAR PREDICCIÓN (GET)
# ==========================================
@app.route("/futuro")
def futuro():
    """Recupera los datos guardados en sesión y los muestra dinámicamente."""
    # Si alguien intenta entrar directo sin rellenar el formulario, lo regresamos al inicio
    if "nombre" not in session:
        return redirect(url_for("index"))

    color_ingresado = (session.get("color") or "").strip().lower()
    animal_ingresado = (session.get("animal") or "").strip().lower()
    edad = int(session.get("edad") or 0)

    color_info = COLOR_MEANINGS.get(color_ingresado, DEFAULT_COLOR)
    animal_meaning = ANIMAL_MEANINGS.get(animal_ingresado, DEFAULT_ANIMAL)

    return render_template(
        "futuro.html",
        nombre=session.get("nombre"),
        prediccion=session.get("prediccion_destino"),
        color=session.get("color"),
        color_hex=color_info["hex"],
        color_meaning=color_info["meaning"],
        animal=session.get("animal"),
        animal_meaning=animal_meaning,
        numero_suerte=session.get("numero_suerte"),
        edad=edad,
        mensaje_edad=mensaje_por_edad(edad),
    )

if __name__ == "__main__":
    app.run(debug=True)