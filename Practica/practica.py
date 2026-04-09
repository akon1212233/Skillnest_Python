def Looker(type, message):
    if type == "int":
        return int(input(message))
    elif type == "float":
        return float(input(message))
    elif type == "str":
        return input(message)
    else:
        return TypeError

#Numeros pares
def Npares():
    lista_final = ""
    numLook = Looker("int","Cuantos numeros pares deseas ver? ")
    if numLook == "" or numLook <= 0:
        print("Porfavor ingrese un valor mayor a 0 o numerico.")
        return
    print(f"Los primeros {numLook} numeros pares son: ")
    for i in range(1, numLook + 1):
        par = i * 2
        lista_final += f"{par} "
    print(lista_final + "\n")

def verificador():
    year = 2026
    yearLook = Looker("int", "Cual es tu año de nacimiento? ")
    finalyears = year - yearLook
    if finalyears >= 120:
        print("Edad imposible :v")
    elif finalyears >= 18:
        print("Eres mayor de edad! :D")
    else:
        print("Eres menor de edad :C")


def calDesc():
    final = 0.0
    productLook = Looker("float", "Cual es el precio de tu producto? (Dolares) ")
    if productLook >= 100:
        final = productLook * 0.15
    print(f"Subtotal: ${productLook}") #Subtotal
    print(f"Descuento aplicado: ${final}") #Descuento
    print(f"Total: ${productLook - final}") #Total 

def clasificador():
    numLook = Looker("int", "Cual es tu numero? ")
    if numLook > 0 and numLook % 2 == 0:
        print(f"{numLook} es Positivo-Par")
    elif numLook > 0 and numLook % 2 == 1:
        print(f"{numLook} es Positivo-Impar")
    elif numLook < 0 and numLook % 2 == 0:
        print(f"{numLook} es Negativo-Par")
    elif numLook < 0 and numLook % 2 == 1:
        print(f"{numLook} es Negativo-Impar")
    else: 
        print(f"{numLook} es Cero!")

def tabla():
    numlook = Looker("int", "Dime un numero entero: ")
    for i in range(1,12 + 1,1):
        if (numlook * i) % 3 == 0:
             print(f"{numlook} * {i} = {numlook * i}")


def sumatoria():
    total = 0
    while True:
        num = Looker("int", "Dame un numero (si quieres salir, pon un numero negativo) ")
        if num > 0:
            total += num
            print(f"\nTotal de sumatoria es: {total}\n")
        else:
            break
sumatoria()


'''
range(0, 1, 0)
total = 0
num = int(input("Indique cantidad de números que quiera sumar:))
for i in range(num)
    numeros = int(input("Ingrese números: ))
    total += numeros
print(total)
'''
def contador():
    frase = Looker("str", "Dame una frase o palabra ").lower()
    vocales = "aeiouáéíóú" 
    veces = 0
    for caracter in frase:
        if caracter in vocales:
            veces += 1
    
    print(f"La frase '{frase}' tiene {veces} vocales.")


def validador():
    contraseña = "admin1234"
    for i in range(3):
        questLook = Looker("str", "Adivina la contraseña ")
        if questLook == contraseña:
            print("Adivinaste la contraseña! :D\n \n")
            return
        else:
            print("Contraseña incorrecta! :c\n")
    print("No adivinaste la contraseña :CCCC")

def registro():
    arreglo = []
    for i in range(5):
        arreglo.append(Looker("str", f"Nombre {i+1}: "))
    print("Inverso", arreglo[::-1])

def promedio():
    cantidad = Looker("int", "Cuantas notas? ")
    notas = []
    for i in range(cantidad):
        notas += [Looker("float", f"Nota {i+1} ")]
    print(f"Promedio: {sum(notas)/len(notas):.2f}")
    print(f"Maxima: {max(notas)} | Minima {min(notas)}")
promedio()
def filtro():
    numeros = []
    entrada = Looker("str", "Ingresa numeros separados por espacio: ")
    for n in entrada.split():
        numeros += [int(n)]
    mayores = []
    for n in numeros:
        if n > 50:
            mayores += [int(n)]
    print(f"Original: {numeros}\nMayores a 50: {mayores}")
filtro()
def buscador():
    ciudades = ["Santiago","Bogota","Lima","Buenos aires","California", "Ciudad de Mexico","Paris","Tokio","Otawa","Valparaiso"]
    busqueda = Looker("str", "Ciudad a buscar: ")
    if busqueda in ciudades:
        print(f"Entradaen indice: {ciudades.index(busqueda)}")
    else:
        print("No se encontro.")

def simulador():
    nombresProductos = []
    precios = []
    for i in range(3):
        n = Looker("str", f"Producto {i+1} ")
        p = Looker("float", f"Precio de {n} ")
        nombresProductos.append(n)
        precios.append(p)
        for i in range(len(nombresProductos)):
            print(f"Producto: {nombresProductos[i]} - Precio: ${precios[i]}")


def generador():
    lista = []
    while True:
        item = Looker("str", "Articulo ( o 'terminar') ")
        if item.lower() == "terminar": 
            break
        lista.append(item)
    print(f"Ordenada: {sorted(lista)}")

def analisis():
    dias = ["Lunes","Martes","Miercoles","Jueves","Viernes","Sabado","Domingo"]
    temps = []
    for i in range(len(dias)):
        valor = Looker("float", f"Temperaturas del {dias[i]}:")
        temps.append(valor)
    promedio = sum(temps) / len(temps)
    calurosos = 0
    for t in temps:
        if t > 25:
            calurosos += 1
    diaFrio = dias[temps.index(min(temps))]
    print(f"Promedio: {promedio:.1f}")
    print(f"Dias > 25°: {calurosos}")
    print(f"Mas frio: {diaFrio} ({min(temps)}°))")
analisis()