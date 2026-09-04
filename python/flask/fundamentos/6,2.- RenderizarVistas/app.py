from flask import Flask,render_template

app = Flask(__name__)

@app.route("/")
def inicio():
    return render_template("index.html",
    nombre="Dany Hernandez",
    curso="Desarrollo Web con Flask",
    ciudad="Santiago",
    anio=2026,
    profesor=True,
    tecnologias=["Python","Flask","HTML","CSS"])



@app.route("/jugador")
def jugador():
    return render_template("jugador.html",
    jugador="CyberWarrior",
    puntaje="1084",
    lider=True)

# Ejecutar el servidor
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
