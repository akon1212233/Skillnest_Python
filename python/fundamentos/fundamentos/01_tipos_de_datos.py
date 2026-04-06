#      TIPOS DE DATOS

# Booleanos (Verdadero o falso)
mayor_edad = True
tiene_bigote = False
# Integer (Numerales enteros)
mayoria_edad = 18
altura = 1.72
# String (Cadena de texto)
frase = "Anita lava la tina"
#      DATOS COMPUESTOS

# Lista (Lista de objetos)
lista_vacia = []
gatos = ["Garfield", "Silvestre", "Hello Kitty"]

# Imprimir (Imprime los datos)
print(gatos[2]) # Imprime: Silvestre

# Cambio de dato en el INDEX [1] de la lista 'gatos' por "Tom" 
gatos[1] = "Tom"
# Agrega a la lista 'gatos' el dato "Felix"
gatos.append("Felix")
print(gatos) #Imprime: ['Garfield', 'Tom', 'Hello Kitty', 'Felix']
gatos.pop() # saca el dato final y lo devuelve.

print(gatos) #Imprime: ['Garfield', 'Tom', 'Hello Kitty']
gatos.pop(1) # Elimina el dato en el INDEX 1 y lo devuelve.
print(gatos) #Imprime: ['Garfield', 'Hello Kitty']

#      TUPLAS
perro = ("Scooby Doo", "Gran Danés", "Scooby Galletas", 7)
print(perro[0]) #Imprime: Scooby Doo
# perro[2] = "comida de perro" #ERROR: Las tuplas no pueden ser modificadas (TypeError: 'tuple' object does not support item assignment)

#      DICCIONARIOS
diccionario_vacio = {}
persona = {'nombre': 'Carmen', 'edad': 31, 'altura': 1.71, 'usa_lentes': False}
persona['nombre'] = 'Valeria'  # Actualiza si el valor de la llave existente
persona['hobbies'] = ['jugar videojuegos', 'programación'] 

# Agrega esa clave-valor si no existía previamente
print(persona)

# Imprime: {'nombre': 'Carmen', 'edad': 31, 'altura': 1.71, 'usa_lentes': False, 'hobbies': ['jugar videojuegos', 'programación']}
altura = persona.pop('altura')  # Elimina la clave indicada y devuelve el valor
print(altura)    # Imprime: 1.71
print(persona) 

# salida: {'nombre': 'Carmen', 'edad': 31, 'usa_lentes': False, 'hobbies': ['jugar videojuegos', 'programación']} 

#      FUNCIONES COMUNES

# Devuelve el tipo de dato :

#      Numericos (INT, FLOAT, COMPLEX)
#      Secuenciales (STR,LIST,TUPLE,RANGE)
#      Booleanos (BOOL)
#      Binarios (BYTES,BYTEARRAY,MEMORYVIEW)
#      Conjuntos (SET, FROZENSET)
#      y NONETYPE

print(type(3.1416)) #Imprime: <class 'float'>
print(type(persona)) #Imprime <class 'dict'>

print(len(persona)) #Imprime: 4 (la cantidad de pares de clave-valor)
print(len("Me encanta programar")) #Imprime: 20