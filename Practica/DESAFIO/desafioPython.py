class Store():
    def __init__(self, name : str):
        self.name = name
        self.list = []
    def addProduct(self, newProduct:object):
            # toma un producto y lo agrega a la tienda
        self.list.append(newProduct)
        return self
    def sellProduct(self, id:int):
            # elimina el producto de la lista de productos de la tienda dada la identificación (suponga que id es el índice del producto en la lista) e imprima su información.
        productoVendido = self.list.pop(id)
        print("Producto vendido:")
        productoVendido.printInfo()
        return self
    def inflation(self, percentIncrease:float):
            # aumenta el precio de cada producto por el percent_increase dado (¡use el método que escribió en la clase Product!)
        for producto in self.list:
            producto.updatePrice(percentIncrease, True)
        return self
    def setClearance(self, category:str, percentDiscount:float):
            # actualiza todos los productos que coinciden con la categoría dada reduciendo el precio en el percent_discount dado (¡use el método que escribió en la clase Product!)
        for producto in self.list:
            if producto.category == category:
                producto.updatePrice(percentDiscount, False)
        return self
class Producto():
    def __init__(self, name:str, price:int, category:str):
        self.name = name
        self.price = price
        self.category = category
    def updatePrice(self, percentChange:float, isCreased:bool):
            # actualiza el precio del producto. Si is_increased es True, el precio debería aumentar en el porcentaje de cambio proporcionado. Si es False, el precio debe disminuir en el cambio porcentual proporcionado.
        if isCreased == True:
            self.price = self.price + (self.price * (percentChange / 100))
        else:
            self.price = self.price - (self.price * (percentChange / 100))
        return self
    def printInfo(self):
            # imprime el nombre del producto, su categoría y su precio.
        print(f"""
            Nombre: {self.name}
            Precio: $ {self.price}
            Categoria: {self.category}
            """)
        return self
pepino = Producto("Pepino", 1380, "Verdura")
mamitasPuebla = Store("Tienda mamitas puebla")
mamitasPuebla.addProduct(pepino).inflation(10.0).sellProduct(0)