from flask import FLask,render_template
app = Flask(__name__)

@app.route('/bienvenido')
def bienvenido():

   #Enviamos 2 nuevos argumentos
   return render_template('index.html', cancion="dale a tu cuerpo alegría macarena", repite=5)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)