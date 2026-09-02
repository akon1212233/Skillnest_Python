from flask import Flask, render_template

app = Flask(__name__)

@app.route('/listas')

def renderizar_listas():

   #Próximamente estas listas serán extraidas de la base de datos

   listado_estudiantes = [

       {'nombre': 'Florencia', 'edad': 25},

       {'nombre': 'Valentina', 'edad': 30},

       {'nombre': 'José', 'edad': 27},

       {'nombre': 'Patricio', 'edad': 21}

   ]

   return render_template('listas.html', numeros=[7, 15, 22], estudiantes=listado_estudiantes)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)