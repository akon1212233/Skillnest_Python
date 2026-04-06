import random #importacion de libreria de procesos aleatorios.

nombre = "Frida Kahlo" #Creacion de variable tipo string y se asigna un valor.
print(type(nombre)) #Type = Metodo de python para mostrar el tipo de una variable.
print(len(nombre)) #Len = Devuelve el largo de una variable.

edad = 25 #Creacion de varible tipo numerico (INT)

if edad < 18: #Se establece condicion if.
    print("Eres menor de edad") #Se establece subcondicion elif (else if)
elif edad == 18: #condicion else if
    print("Tienes 18 años") #imprime string
else: #condicion si no se cumple ninguna anterior
    print("Eres mayor de edad.") #imprime string

frutas = ["Manzana", "Pera", "Fresa"] #Creacion de la variable con un array (ARREGLO) incluido
print(frutas[0]) #Imprime la posicion 0 de el arreglo
frutas[0] = "Banana" #A la posicion 0 del arreglo se le remplaza con otro valor
frutas.append("Uva") #Se agrega un valor al final del arreglo
frutas.remove("Pera") #Se elimina un valor del arreglo

dimensiones = (200,50) #Variable tipo imputable(TUPLA)
print(dimensiones[0]) #Imprime el primer valor de la variable

persona = { #Variable tipo objetos(DICCIONARIO)
    "nombre": "Carlos",
    "edad": "30"
}

print(persona["nombre"]) #Imprime el valor del item de la varible 'persona'.
persona["edad"] = 31 #Remplaza datos de un item de la variable persona
persona["ciudad"] #Agrega un item y su valor a la variable
del persona["ciudad"] #Borra el item "ciudad" de la variable 'persona'

for i in range(5): #For range: se crea bucle en rango desde 0 a 5 (saltandose el ultimo numero!)
    if i == 2: #Condicional (IF) si i es igual a 2
        continue #(CONTINUE) ignora el proceso y continua
    elif i == 4: #Condicial (ELIF) si i es igual a 4
        break #Si se activa, el bucle se rompe.
    print(i) #Imprime el valor de 'i'

contador = 0 #Variable tipo numero
while contador < 3: #Bucle (WHILE) preguntando si 'contador' es menor a 3 (Inicio: FALSE)
    print(f"while contador es: {contador}") #Imprime "while contador es: " mas el valor de 'contador' en el momento.
    contador += 1 #Agrega 1 numero a la variable 'contador'

def saludar_usuario(nombre): #Se define la funcion (DEF) `saludar_usuario` con el parametro 'nombre'
    return f"Hola, {nombre}!" #Regresa (RETURN) la cadena de texto "Hola, " mas el valor de 'nombre'

print(saludar_usuario("Francisca")) #imprime lo que regrese la funcion `saludar_usuario()` con el parametro "Francisca"

