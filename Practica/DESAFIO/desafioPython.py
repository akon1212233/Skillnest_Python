class Store():
    def __init__(self, name : str):
        self.name = name
        self.list = []
    def addProduct(self, newProduct:str):
        # toma un producto y lo agrega a la tienda
        pass
    def sellProduct(self):
        # elimina el producto de la lista de productos de la tienda dada la identificación (suponga que id es el índice del producto en la lista) e imprima su información.
        pass
    def inflation(self, percentIncrease):
        # aumenta el precio de cada producto por el percent_increase dado (¡use el método que escribió en la clase Product!)
        pass
    def setClearance(self, category, percentDiscount):
        # actualiza todos los productos que coinciden con la categoría dada reduciendo el precio en el percent_discount dado (¡use el método que escribió en la clase Product!)
        pass
class Producto():
    def __init__(self, name:str, price:int, category:str):
        self.name = name
        self.price = price
        self.category = category
    def updatePrice(self, percentChange:float, inCreased:bool):
        # actualiza el precio del producto. Si is_increased es True, el precio debería aumentar en el porcentaje de cambio proporcionado. Si es False, el precio debe disminuir en el cambio porcentual proporcionado.
        pass
    def printInfo(self):
        # imprime el nombre del producto, su categoría y su precio.
        pass