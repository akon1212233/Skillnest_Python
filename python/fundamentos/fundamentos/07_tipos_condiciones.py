num = 15
if num > 20:
   print("Número mayor a 20")
else:
   print("Número menor a 20")
'''
La variable num es menor a 20, por lo que el bloque de código de else será ejecutado.
Es decir que vamos a imprimir "Número menor a 20"
'''
num = 101
if num > 50:
   print("Número mayor a 50")
elif num > 100:
   print("Número mayor a 100")
else:
   print("Número menor a 10")
'''
A pesar de que num es mayor que 50 y 100, la primera condicional que se cumpla es la única que se ejecutará.
Es por eso que solo imprimirá: "Número mayor a 50"
'''
if num < 60:
   print("Número menor a 50")

#No se cumple con la condicional, por lo que no se ejecuta el bloque de código