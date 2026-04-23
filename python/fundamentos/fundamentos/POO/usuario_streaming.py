class usuarioStreaming:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.sub = "Gratis"
        self.reproductionList = []

    def upToList(self, title):
        """Agrega un contenido a la lista de reproducción del usuario."""
        self.reproductionList.append(title)
        return self
    
    def lookContent(self, title):
        """Simula que el usuario reproduce un contenido."""
        if title in self.reproductionList:
            print(f"Reproduciendo: {title}...")
            self.reproductionList.remove(title)
        else:
            print(f"La cancion '{title}' no esta en la lista")
            print("Agregando...")
            self.reproductionList.append(title)
        return self
    
    def changeSub(self, newSub):
        """Cambia el tipo de suscripción del usuario."""
        permitedTypeSub = ["Gratis", "Estandar", "Premium"]
        if newSub in permitedTypeSub:
            self.sub = newSub
        else:
            print("Tipo de suscripcion no permitida")
        return self
    
    def showInfoUser(self):
        """Muestra la información del usuario y su lista de reproducción."""
        print(f"Usuario: {self.name} | Email: {self.email} | Suscripcion: {self.sub} | Lista: {self.reproductionList}")
        return self

akon = usuarioStreaming("akon12123","akonBustamante@liceovvh.cl")
marcelo = usuarioStreaming("marck98","marceloRios@liceovvh.cl")
daniel = usuarioStreaming("calzoncillofrio","danielJimenez@liceovvh.cl")

print()
akon.changeSub("Premium").upToList("Soy Feo Pero Rico").upToList("Las Seis").showInfoUser().lookContent("Desnudos").showInfoUser().lookContent("La innombrable").showInfoUser()
print()
marcelo.changeSub("Estandar").upToList("Te vas").upToList("El Gran Tirano").showInfoUser().lookContent("El Gran Tirano").showInfoUser().lookContent("Un Hombre Muerto En El Ring").showInfoUser()
print()
daniel.changeSub("premium barato").upToList("Hijos de la Tierra").upToList("Sube a Nacer Conmigo").upToList("Gran Pecador").upToList("Pasto seco").showInfoUser().lookContent("Gran Pecador").showInfoUser().lookContent("Es el Amor").showInfoUser()
print()