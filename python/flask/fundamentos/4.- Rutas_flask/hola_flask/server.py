# python -m pipenv install flask

from flask import Flask

app = Flask(__name__)

@app.route("/")
def inicio():
    return "Bienvenido al curso de Flask!"

@app.route("/saludar/<nombre>")
def saludar(nombre):
    return f"¡Hola, {nombre}!"


if __name__ == "__main__":
    app.run(debug=True)