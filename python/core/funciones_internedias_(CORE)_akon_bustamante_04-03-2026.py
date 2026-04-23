""" Actualización de datos: a partir de los siguientes datos, realiza las modificaciones solicitadas:"""

# Ranking de puntajes de un torneo de eSports
puntajes = [ [1000, 1500, 2000], [300, 700, 1400] ]


# Lista de creadores de contenido en una plataforma de streaming
streamers = [
    {"nombre": "GameNinjaPro", "seguidores": 250000},
    {"nombre": "PixelWarrior", "seguidores": 180000}
]


# Eventos en distintas ciudades del mundo
eventos = {
    "Estados Unidos": ["Los Ángeles", "Nueva York", "Las Vegas"],
    "España": ["Madrid", "Barcelona", "Valencia"]
}


# Coordenadas de la sede de un torneo internacional
ubicacion = [
    {"latitud": 34.052235, "longitud": -118.243683}
]

# En puntajes, cambia el valor 300 por 600 (ajuste en los puntajes de la primera ronda). Resultado esperado:
#           puntajes = [[1000, 1500, 2000], [600, 700, 1400]]​​
puntajes[1][0] = 600

# En streamers, cambia el nombre de ”GameNinjaPro” a ”EliteGamerX”.

for streamer in streamers:
    if streamer["nombre"] == "GameNinjaPro":
        streamer["nombre"] = "EliteGamerX"

# En eventos, cambia la ciudad “Las Vegas” por “San Francisco”.

eventos["Estados Unidos"][eventos["Estados Unidos"].index("Las Vegas")] = "San Francisco"

#En ubicacion, cambia el valo de ”latitud” a 40.712776 (cambiando la sede del torneo a Nueva York).
ubicacion[0]["latitud"] = 40.712776

"""
Crea la función iterar_diccionario(lista) que reciba una lista de diccionarios (como streamers) y recorra cada uno, imprimiendo sus claves y valores.
Formatea la salida para que cada diccionario se imprima en una sola línea, con el formato.
nombre - EliteGamerX, seguidores - 250000
"""
def iterar_diccionario(lista):
    for valor in lista:
        print(f"nombre - {valor["nombre"]}, seguidores - {valor["seguidores"]}")
iterar_diccionario(streamers)
"""

Obtener valores de un diccionario creando la función obtener_valores(clave, lista) que reciba, por una parte, una cadena con el nombre de una clave, por otra, una lista de diccionarios. La función debe imprimir el valor asociado a esa clave en cada uno de los diccionarios.
Ejemplo de uso:
obtener_valores("nombre", streamers)
obtener_valores("seguidores", streamers)​
Salida esperada:

EliteGamerX
PixelWarrior

250000
180000
"""
def obtener_valores(clave, lista):
    for diccionario in lista:
        print(diccionario[clave])
    print() #Espacio para mejor visualizacion en terminal


obtener_valores("nombre", streamers)
obtener_valores("seguidores", streamers)
""" Mostrar información de un diccionario con listas: """

""" 
Crea la función mostrar_informacion(diccionario), que reciba un diccionario en el que los valores sean listas. 
La función debe, por una parte, imprimir el tamaño de la lista y la clave en mayúsculas, por otra, imprimir cada elemento de la lista en líneas separadas.
Ejemplo de uso:
"""
categorias = {
    "juegos_populares": [
        "Fortnite", 
        "Minecraft", 
        "Valorant", 
        "GTA V",
    ],
    "ciudades_eventos": [
        "Nueva York",
        "Madrid",
        "Tokio",
    ]
}
def mostrar_informacion(diccionario):
    for clave, lista in diccionario.items():
        print(f"{len(lista)} {clave.upper()}")
        for element in lista:
            print(element)
        print()
mostrar_informacion(categorias)

# Salida esperada:
"""
4 JUEGOS_POPULARES
Fortnite
Minecraft
Valorant
GTA V

3 CIUDADES_EVENTOS
Nueva York
Madrid
Tokio​
"""