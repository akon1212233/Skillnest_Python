from flask import Flask, render_template
from Controllers.mascota import Mascota

app = Flask(__name__)

@app.route("/")
def index():
    """
    Consulta todas las mascotas y las envía
    hacia la plantilla index.html.
    """
    mascotas = Mascota.get_all()
    print(mascotas)
    return render_template(
        "index.html",
        todas_mascotas=mascotas
    )

if __name__ == "__main__":
    app.run(debug=True)