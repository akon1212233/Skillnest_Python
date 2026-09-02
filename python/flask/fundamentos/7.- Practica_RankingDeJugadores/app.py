from flask import Flask, render_template

app = Flask(__name__)

# Datos de jugadores con puntajes
jugadores = [
   {"nombre": "AlexGamer", "puntaje": 5000},
   {"nombre": "PixelMaster", "puntaje": 7500},
   {"nombre": "ShadowNinja", "puntaje": 8200},
   {"nombre": "CyberWarrior", "puntaje": 9100},
   {"nombre": "UltraNoob", "puntaje": 3000}
]


# Ruta para mostrar el ranking de jugadores
@app.route("/ranking")
def raiz():
   return render_template("index.html",jugadores=list(jugadores))
# Ruta para mostrar un número limitado de jugadores
@app.route("/ranking/<int:limite>")
def rankingLimite(limite):
   newList = jugadores[:limite]
   
   return render_template("index.html",jugadores= newList)
   pass
# Ruta para personalizar el color del ranking
@app.route("/ranking/<int:limite>/<string:color>")
def rankingLimiteColor(limite,color):
   newList = jugadores[:limite]
   
   return render_template("index.html",jugadores= newList,color= color)
   pass
# Ejecutar el servidor
if __name__ == "__main__":
   app.run(debug=True)


"""
/ranking	    Muestra el ranking de jugadores completo.	        http://127.0.0.1:5000/ranking	     Muestra la lista de todos los jugadores.
/ranking/3	    Muestra solo los 3 primeros jugadores.	            http://127.0.0.1:5000/ranking/3	     Solo aparecen los 3 primeros del ranking.
/ranking/3/blue	Muestra los 3 primeros jugadores con el fondo azul.	http://127.0.0.1:5000/ranking/3/blue Lista de los 3 primeros jugadores con el fondo en azul.
"""