lista_vacia = []
lista_compras = ['tomate', 'pan', 'queso', 'jamón']

lista_especial = [1, 2, ['a', 'b', 'c'], True]

verso1 = ['dale', 'a', 'tu', 'cuerpo']
verso2 = ['alegria', 'macarena']
estrofa = verso1 + verso2
print(estrofa)
cancion = 3 * estrofa
print(cancion)

cajonera = ["pantalones", "camisetas", "calcetines"]
print(cajonera[0]) #Accedemos al cajón con índice 0. Imprime: "pantalones"
print(cajonera[1]) #Accedemos al cajón con índice 1. Imprime: "camisetas"
print(cajonera[2]) #Accedemos al cajón con índice 2. Imprime: "calcetines"
cajonera[1] = "sueters" #Cambiamos el valor del cajón con índice 1
print(cajonera) #Imprime: ['pantalones', 'sueters', 'calcetines']

cajonera.append("vestidos") #Agregamos "vestidos" al final de la lista
print(cajonera) #Imprime: ['pantalones', 'sueters', 'calcetines', 'vestidos']

lista_grande = [2, 4, 6, 8, 10, 12, 14, 16]
print(lista_grande[3:]) #Imprime:[8, 10, 12, 14, 16]
print(lista_grande[:6]) #Imprime:[2, 4, 6, 8, 10, 12]
print(lista_grande[3:6]) #Imprime:[8, 10, 12]

vocales = ['a', 'e', 'i', 'o', 'u']
print(len(vocales)) #Imprime: 5

frozen = ["Elsa", "Anna", "Olaf"]
frozen.pop() #Sintaxis: nombre_lista.funcion()
print(frozen) #Imprime: ['Elsa', 'Anna']