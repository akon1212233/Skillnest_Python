from flask import Flask, render_template

app = Flask(__name__)

@app.route("/listas")
def renderizar_listas():

    # Lista de números
    numeros = [7, 15, 22]

    # Lista de diccionarios
    listado_estudiantes = [
        {
            "nombre":"Florencia",
            "edad":25
        },
        {
            "nombre":"Valentina",
            "edad":30
        },
        {
            "nombre":"José",
            "edad":27
        },
        {
            "nombre":"Patricio",
            "edad":21
        }
    ]

    return render_template(
        "listas.html",
        numeros=numeros,
        estudiantes=listado_estudiantes
    )


@app.route("/videojuegos")
def renderGames():
    juegos = [
        {
            "nombre":"Minecraft Bedrock",
            "plataforma":"Android",
            "anio":2011
        },
        {
            "nombre":"Slime Rancher",
            "plataforma":"PC",
            "anio": 2017
        },
        {
            "nombre":"Watch_Dogs",
            "plataforma":"PC",
            "anio":2014
        },
        {
            "nombre":"Half Life",
            "plataforma":"PC",
            "anio":1998
        },
        {
            "nombre":"InFamous",
            "plataforma":"PlayStation",
            "anio":2009
        }
    ]
    return render_template(
        "games.html",
        juegos=juegos
    )
# Ejecutar el servidor
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
