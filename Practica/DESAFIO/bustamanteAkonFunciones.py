"""
Requisitos obligatorios
Su trabajo debe cumplir con lo siguiente:
Uso de funciones con parámetros
Uso de menú con ciclo while
Uso de input() para solicitar datos
Uso de listas (arreglos)
Uso de diccionarios
Uso de ciclos for
Uso de estructuras condicionales (if, elif, else)
Código ordenado, comentado y correctamente indentado
Opción de salida del programa (0. Salir)
"""
"""
Ejercicios a desarrollar
Su programa deberá considerar las siguientes funciones:
"""

#Crear una función que reciba una lista de números enteros y muestre cuál es el número mayor y cuál es el menor.
def higherOrLower(lista):
    print(f"Mayor: {max(lista)}, Menor: {min(lista)}")
#Crear una función que reciba una cadena de texto y cuente cuántas vocales contiene.
def vocalCount(texto):
    conteo = 0
    for letra in texto.lower():
        if letra in "aeiouáéíóú":
            conteo += 1
    print(f"Vocales: {conteo}")
#Crear una función que reciba una lista de nombres y muestre únicamente aquellos que tengan más de 5 letras.
def more5Letters(list):
    pass
#Crear una función que reciba una lista de notas (números decimales), calcule el promedio e indique si el estudiante aprueba (promedio mayor o igual a 4.0).
def passOrNot(lista):
    promedio = sum(lista) / len(lista)
    resultado = "Aprobado" if promedio >= 4.0 else "Reprobado"
    print(f"Promedio: {promedio:.1f} - {resultado}")
#Crear una función que reciba una lista de precios de productos y aplique un descuento del 10%, mostrando el valor original y el nuevo valor.
def descount(lista):
    for p in lista:
        print(f"Original: {p} -> Con 10% desc: {p * 0.9:.2f}")
#Crear una función que reciba un número entero y determine si es par o impar.
def evenOrOdd(n):
    if n % 2 == 0:
        print(f"{n} es Par")
    else:
        print(f"{n} es Impar")
#Crear una función que reciba una lista de edades y muestre cuántas personas son mayores de edad (18 años o más).
def highter18Years(lista):
    pass
#Crear una función que reciba una lista de palabras y permita buscar cuántas veces aparece una palabra específica ingresada por el usuario.
def wordSpecific(lista, buscar):
    print(f"La palabra '{buscar}' aparece {lista.count(buscar)} veces")
#Crear una función que reciba una lista de números y genere una nueva lista que contenga únicamente los números positivos.
def positiveNumbers():
    pass
#Crear una función que reciba una lista de productos (utilizando diccionarios con nombre y stock) y muestre cuáles tienen un stock menor a 5 unidades.
def stillStock(productos):
    for p in productos:
        if p["stock"] < 5:
            print(f"Bajo stock: {p['nombre']} ({p['stock']} un.)")

def recibeInput():
    while True:

        print("""
    1) 
    2)
    3)
    4)
    5)
    6)
    7)
    8)
    9)
    10)
""")
        respuesta = int(input("Cual funcion quieres activa "))
        if respuesta == 0:
            break
        elif respuesta == 1:
            higherOrLower(input("Ingresa un lista de numeros para mostrar el mayor y el menor").split())
        elif respuesta == 2:
            vocalCount()
        elif respuesta == 3:
            more5Letters()
        elif respuesta == 4:
            passOrNot()
        elif respuesta == 5:
            descount()
        elif respuesta == 6:
            evenOrOdd()
        elif respuesta == 7:
            highter18Years()
        elif respuesta == 8:
            wordSpecific()
        elif respuesta == 9:
            positiveNumbers()
        elif respuesta == 10:
            stillStock()
        else:
            print("\nNumero no Accesible, ingrese nuevamente su numero")
recibeInput()