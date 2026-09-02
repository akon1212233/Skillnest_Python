from flask import Flask

app = Flask(__name__)

@app.route("/")
def hola_mundo():
    return "asdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasd!"

@app.route("/nosotros")
def nosotros():
    return "<h1>conócenos un poco más!</h1>"

@app.route("/tuche")
def tuche():
    return "no quiero hacer tareas"

@app.route("/tarea")
def tarea():
    return "no me gusta hacer tareas"

if __name__ == "__main__":
    app.run(debug=True)