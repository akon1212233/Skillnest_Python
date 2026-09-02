import webbrowser
import time

def buscar_en_pestaña_actual(termino_busqueda):
    
    url_busqueda = f"https://www.pokemon.com/el/pokedex/{termino_busqueda}"

    print(f"Abriendo pestaña para buscar: {termino_busqueda}")

    webbrowser.open_new_tab(url_busqueda)

pokedex = [
   {"id": 1,  "nombre": "Bulbasaur",  "tipo": "Planta/Veneno",   "imagen": "bulbasaur.png",  "poder": 45,  "altura": "0.7m", "peso": "6.9kg"},
   {"id": 4,  "nombre": "Charmander", "tipo": "Fuego",           "imagen": "charmander.png", "poder": 39,  "altura": "0.6m", "peso": "8.5kg"},
   {"id": 7,  "nombre": "Squirtle",   "tipo": "Agua",            "imagen": "squirtle.png",   "poder": 44,  "altura": "0.5m", "peso": "9.0kg"},
   {"id": 25, "nombre": "Pikachu",    "tipo": "Eléctrico",       "imagen": "pikachu.png",    "poder": 35,  "altura": "0.4m", "peso": "6.0kg"},
   {"id": 39, "nombre": "Jigglypuff", "tipo": "Normal/Hada",     "imagen": "jigglypuff.png", "poder": 115, "altura": "0.5m", "peso": "5.5kg"},
   {"id": 52, "nombre": "Meowth",     "tipo": "Normal",          "imagen": "meowth.png",     "poder": 40,  "altura": "0.4m", "peso": "4.2kg"},
   {"id": 54, "nombre": "psyduck",    "tipo": "Agua",            "imagen": "psyduck.png",    "poder": 50,  "altura": "0.8m", "peso": "19.6kg"},
   {"id": 94, "nombre": "gengar",     "tipo": "Fantasma/Veneno", "imagen": "gengar.png",     "poder": 60,  "altura": "1.5m", "peso": "40.5kg"},
   {"id": 95, "nombre": "onix",       "tipo": "Roca/Tierra",     "imagen": "onix.png",       "poder": 35,  "altura": "8.8m", "peso": "210.0kg"},
   {"id": 143,"nombre": "snorlax",    "tipo": "Normal",          "imagen": "snorlax.png",    "poder": 160, "altura": "2.1m", "peso": "460.0kg"}
]

for pokemon in pokedex:
    termino = pokemon["nombre"].lower()
    buscar_en_pestaña_actual(termino)
    time.sleep(1)

