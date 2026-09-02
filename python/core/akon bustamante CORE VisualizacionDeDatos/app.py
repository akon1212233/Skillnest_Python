from flask import Flask,render_template
app = Flask(__name__)

# Base de datos ficticia de plataformas digitales
datos = [
   {"nombre": "Spotify", "usuarios": "515M", "fundado": "2006", "pais": "Suecia"},
   {"nombre": "Netflix", "usuarios": "247M", "fundado": "1997", "pais": "EE.UU."},
   {"nombre": "YouTube", "usuarios": "2.5B", "fundado": "2005", "pais": "EE.UU."},
   {"nombre": "Twitch", "usuarios": "140M", "fundado": "2011", "pais": "EE.UU."},
   {"nombre": "TikTok", "usuarios": "1.7B", "fundado": "2016", "pais": "China"},
   {"nombre": "Instagram", "usuarios": "2.35B", "fundado": "2010", "pais": "EE.UU."},
   {"nombre": "Discord", "usuarios": "250M", "fundado": "2015", "pais": "EE.UU."},
]
paises_unicos = sorted(list(set(d["pais"] for d in datos)))
ordenes = ["Nombre","Usuarios","Anio Fundacion","Pais","Detalles"]
@app.route('/tabla')
def tabla():   
   return render_template(
      "tabla.html", datos=sorted(datos, key=lambda x: x["nombre"]), ordenes=ordenes,
      paises=paises_unicos, imgPath="/static/images/"
   
   )
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)