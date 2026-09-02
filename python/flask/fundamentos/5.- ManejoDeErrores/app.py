from flask import Flask

app = Flask(__name__)

@app.route("/")
def inicio():
    return "Bienvenido a Flask"

@app.route("/saludo/<nombre>")
def saludo(nombre):
    return f"Hola {nombre}"


@app.errorhandler(404)
@app.route('/<string:direccion>')
def pagina_no_encontrada(direccion):
    return f"""
    <h1>Pagina no encontrada</h1>
    <p>la pagina { direccion } no existe</p>
    <a href="/">Regresar a la pagina principal</a>
    
    """, 404

# Ejecuta el servidor
if __name__ == "__main__":
   app.run(debug=True)

