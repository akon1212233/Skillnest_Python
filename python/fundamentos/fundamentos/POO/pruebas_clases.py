class animal(): 
    def __init__(self, name : str, yearOld : int, typeMove, specie, maxYearOlds):
        self.name = name
        self.yearOld = yearOld
        self.typeMove = typeMove
        self.specie = specie
        self.maxYears = maxYearOlds
        self.lostYears = maxYearOlds - yearOld
        self.milagro = False
        self.check_milagro()
    def check_milagro(self):
        if self.lostYears < 0:
            self.milagro = True
            self.lostYears = abs(self.lostYears)
        
    def __str__(self):
        return f"El animal {self.name} tiene {self.yearOld} años humanos, su tipo de movimiento es {self.typeMove} y su especie es {self.specie}. {f"\nTu animal esta por encima de la vida media! los años por encima de la media es {self.lostYears} años!\n" if self.milagro == True else ''}\n"

perro = animal("Perro", 17, "Terrestre", "Canino", 15)
gato = animal("Gato", 3, "Terrestre", "Felino", 10)
tortuga = animal("Tortuga", 163, "Terrestre", "quelonios", 150)

print(perro, gato, tortuga)
