inventario = ["laptop","raton","monitor","cable hdmi"]
inventario.append("impresora")
inventario.append("teclado")
for i in range(len(inventario)):
    print(inventario[i])
print(len(inventario))
inventario[5] = "teclado mecanico"
promocion = []
for i in range(0, 3):
    promocion.append(inventario[i])
promocion.sort()
print(promocion)
print(inventario.pop(), inventario)