#1)Marcelo
#2)
#3)
#4)yoycer
#5)
#6)Akon
#7)
#8)AKON
#9
#10)



# Ando viendo cuales son mas faciles y de ahí las clasifico (ez), (Medium) y (Hard)


#Marck
"""
1) Crear una función que reciba una lista de números enteros y genere una nueva lista solo con los
números pares mayores a 10. Luego debe mostrar la nueva lista y la cantidad de elementos encontrados.
"""
def numeros_pares_mayores_a_10():
    numeros = input("Ingrese los números enteros separados por espacios: ")
    lista = [int(num) for num in numeros.split()]
    pares_mayores_a_10 = []
    for i in range(len(lista)):
        if lista[i] > 10 and lista[i] % 2 == 0:
            pares_mayores_a_10.append(lista[i])
    print("Nueva lista:", pares_mayores_a_10)
    print("Cantidad de elementos:", len(pares_mayores_a_10))

def main():
    numeros_pares_mayores_a_10()

#Marck
"""
2) Crear una función que reciba una lista de nombres y una letra.
 Debe mostrar todos los nombres que comiencen con esa letra y contar cuántos cumplen la condición.
"""


#Marck
"""
3) Crear una función que reciba una lista de notas (decimales) y genere dos listas:una con aprobados (≥ 4.0)
y otra con reprobados (< 4.0). Debe mostrar ambas listas y la cantidad de estudiantes en cada grupo.
"""




#Yoycer
"""
4) Crear una función que reciba una lista de números y determine cuál es el número que más se repite.
 Debe mostrar el número y la cantidad de veces que aparece.
"""


#Yoycer
"""
5) Crear una función que reciba una lista de palabras y genere una nueva lista solo con aquellas que tengan más de 4 letras y contengan la letra “a”.
 Debe mostrar la lista resultante.
"""
def palabras_tenga_a(palabra):
    return "a" in palabra

def ejercicio5():
    palabras = input("Ingresas algunas palabras: ").split()
    palabras4 = []
    for palabra in palabras:
        if len(palabra) > 4 and palabras_tenga_a(palabra):
            palabras4.append(palabra)
    if palabras4:
        print("Palabras que contienen la letra 'a' y tienen más de 4 letras:", palabras4)
    else:
        print("Ninguna palabra contiene la letra 'a' o tiene más de 4 letras")

#Akon
"""
--6) Crear una función que reciba una lista de edades y clasifique a las personas en tres grupos: menores de edad, adultos y adultos mayores (60+).
 Debe mostrar la cantidad de personas en cada grupo.
"""
def probadorDeEdad(lista):
    menor = []
    mayor = []
    mayorDeEdad = []
    for personaEdad in  lista:
        if personaEdad < 18:
            menor.append(personaEdad)
        elif personaEdad >= 18 and personaEdad <= 60:
            mayor.append(personaEdad)
        else:
            mayorDeEdad.append(personaEdad)
    menor = sorted(menor)
    mayor = sorted(mayor)
    mayorDeEdad = sorted(mayorDeEdad)
    print(f"Menores : {len(menor)} {menor}), Mayores de edad : {len(mayor)} {mayor}, Adultos Mayores : {len(mayorDeEdad)} {mayorDeEdad}")
#Testeo lugar
#probadorDeEdad([1,7,1,4,89,43,22,72,100,56,41,12,54])
def ejercicio6():
    dato = input("Ingrese la lista de edades: (ej: [1,4,2,5]) ")
    lista = eval(dato)
    probadorDeEdad(lista)
#Akon
"""
--7) Crear una función que reciba una lista de números y determine si todos los números son positivos.
 Si encuentra al menos un número negativo, debe indicarlo y detener el recorrido.
"""


"""
8) Crear una función que reciba una lista de productos (diccionarios con nombre y precio).
 Debe mostrar los productos cuyo precio esté entre 1000 y 5000, y calcular el promedio de esos precios.
"""

"""
--9) Crear una función que reciba una lista de palabras y un número entero.
 Debe mostrar solo las palabras cuya longitud sea mayor al número ingresado.
"""


"""
10) Crear una función que reciba una lista de números y genere una nueva lista sin elementos repetidos.
 Luego debe mostrar la lista original y la lista resultante.
"""






#Terminal Para trabajar los ejercicios:

def Terminal():
    while True:
        print("\n--- Menu ---")
        print("1. Ingresar números enteros")
        print("2. Verificador de edad")
        print("3. Ver cantidad de elementos en la lista")
        print("4. Salir")
        opcion = int(input("Elige una opcion "))
        if opcion == 4:
            break
        elif opcion == 1:
            print("    Autor: Marcelo")
            main()
        elif opcion == 2:
            print("    Autor: Akon")
            ejercicio6()
        elif opcion == 3:
            print("    Autor: Yoycer")
            ejercicio5()
        else:
            print("Dato no coincidente")
Terminal()