# python -m pipenv install flask

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def inicio():
    return ""

@app.route("/saludar/<nombre>")
def saludar(nombre):
    return f"¡Hola, {nombre}!"


if __name__ == "__main__":
    app.run(debug=True)