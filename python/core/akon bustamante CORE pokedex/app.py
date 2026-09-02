import os
from flask import Flask, render_template

app = Flask(__name__)

# Base de datos ficticia de Pokémon
pokedex = [
   {"id": 1,  "nombre": "Bulbasaur",  "tipo": {"Planta","Veneno"},   "imagen": "bulbasaur.png",  "poder": 45,  "altura": "0.7m", "peso": "6.9kg"},
   {"id": 4,  "nombre": "Charmander", "tipo": {"Fuego"},           "imagen": "charmander.png", "poder": 39,  "altura": "0.6m", "peso": "8.5kg"},
   {"id": 7,  "nombre": "Squirtle",   "tipo": {"Agua"},            "imagen":  "squirtle.png",  "poder": 44,  "altura": "0.5m", "peso": "9.0kg"},
   {"id": 25, "nombre": "Pikachu",    "tipo": {"Electrico"},       "imagen": "pikachu.png",    "poder": 35,  "altura": "0.4m", "peso": "6.0kg"},
   {"id": 39, "nombre": "Jigglypuff", "tipo": {"Normal","Hada"},     "imagen": "jigglypuff.png", "poder": 115, "altura": "0.5m", "peso": "5.5kg"},
   {"id": 52, "nombre": "Meowth",     "tipo": {"Normal"},          "imagen": "meowth.png",     "poder": 40,  "altura": "0.4m", "peso": "4.2kg"},
   {"id": 54, "nombre": "Psyduck",    "tipo": {"Agua"},            "imagen": "psyduck.png",    "poder": 50,  "altura": "0.8m", "peso": "19.6kg"},
   {"id": 94, "nombre": "Gengar",     "tipo": {"Fantasma","Veneno"}, "imagen": "gengar.png",     "poder": 60,  "altura": "1.5m", "peso": "40.5kg"},
   {"id": 95, "nombre": "Onix",       "tipo": {"Roca","Tierra"},     "imagen": "onix.png",       "poder": 35,  "altura": "8.8m", "peso": "210.0kg"},
   {"id": 143,"nombre": "Snorlax",    "tipo": {"Normal"},          "imagen": "snorlax.png",    "poder": 160, "altura": "2.1m", "peso": "460.0kg"}
]

def calcularPoder(lista_pokemon):
    resultado = []
    
    for pokemon in lista_pokemon:
        p_copy = pokemon.copy()
        porcentaje = (float(p_copy["poder"]) / 200) * 100.0
        p_copy["flex_relleno"] = max(0.0, min(100.0, porcentaje))
        p_copy["flex_vacio"] = 100.0 - p_copy["flex_relleno"]
        resultado.append(p_copy)
    return resultado

def buscador(datoABuscar, claveDato, arregloBase):
    for datos in arregloBase:
        valor_base = str(datos[claveDato])
        
        if isinstance(datoABuscar, str):
            if valor_base.lower() == datoABuscar.lower():
                return datos
        else:
            if valor_base == str(datoABuscar):
                return datos

# Ruta para mostrar todos los Pokémon
@app.route("/pokemon")
def raiz():
    pokedex_listo = calcularPoder(pokedex)
    return render_template("pokedex.html",pokedex=pokedex_listo)
@app.route("/pokemon/<string:nombre_pokemon>")
def nombre(nombre_pokemon):
    if not nombre_pokemon.isdigit():
        res = buscador(nombre_pokemon, "nombre", pokedex)
        if res:
            pokedex_listo = calcularPoder([res])
            return render_template("pokedex.html", pokedex=pokedex_listo)
        return pokemon_no_encontrado(f"{nombre_pokemon}")
    return numero(int(nombre_pokemon))
# Ruta para mostrar un Pokémon por número en la Pokédex
def numero(numero):
    res = buscador(numero, "id", pokedex)
    if res:
        pokedex_listo = calcularPoder([res])
        return render_template("pokedex.html", pokedex=pokedex_listo)
    return pokemon_no_encontrado(f"{numero}")
# Ruta para mostrar una cantidad específica de Pokémon
@app.route("/pokemon/cantidad/<string:cantidad>")
def cantidades(cantidad):
    if cantidad.isdigit():
        newPokedex = pokedex[:int(cantidad)]
        pokedex_listo = calcularPoder(newPokedex)
        return render_template("pokedex.html", pokedex=pokedex_listo)
    return nombre(cantidad)


# Error cuando no se encuentra un Pokémon
def pokemon_no_encontrado(mensaje: str):
   """Función simple para renderizar la página 404 con un mensaje."""
   return render_template("404.html", mensaje=mensaje)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)