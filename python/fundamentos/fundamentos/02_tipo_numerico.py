print(type(1.1)) #Imprime: <class 'float'>
print(type(615)) #Imprime: <class 'int'>
print(type(2j)) #Imprime: <class 'complex'>

entero_a_decimal = float(123)
decimal_a_entero = int(22.5)
entero_a_complejo = complex(35)
print(entero_a_decimal) #Imprime: 123.0
print(decimal_a_entero) #Imprime: 22
print(entero_a_complejo) #Imprime: (35+0j)

import random
num_aleatorio = random.randint(5, 10) #Genera un número aleatorio entre 5 y 10
print(num_aleatorio) #Imprime el número aleatorio generado
