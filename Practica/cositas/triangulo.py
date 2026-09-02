def triangulo():
    largo = int(input("Ingrese el largo del triángulo: "))
    antilargo = (largo)
    mensajelinea = ""
    for i in range(1, largo + 1):

        mensajelinea = " " * (antilargo-i) + "*" * (i*2-1) + (" " * (antilargo-i))
        print(mensajelinea)

triangulo()