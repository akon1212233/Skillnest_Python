class User(object):
    def __init__(self, name, email, balance):
        self.rol = "User"
        self.name = name
        self.email = email
        self.limitDebt = 50000
        self.balance = balance
    def comprar(self, monto):
        self.balance -= monto
    

akon = User("Akon", "akonbustamante11@gmail.com", 1000)
akon.comprar(300)
print(akon.name, akon.balance)