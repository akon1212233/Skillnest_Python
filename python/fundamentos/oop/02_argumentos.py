class Estudiante:
    def __init__(self,rut,nombre,apellido,especialidad,fechaNacimiento):
        self.rut = rut
        self.nombre = nombre
        self.apellido = apellido
        self.especialidad = especialidad
        self.fechaNacimiento = fechaNacimiento
        print(f"\nHola!\nMi nombre es {self.nombre} {self.apellido}, estoy en la especialidad {self.especialidad} y naci el {self.fechaNacimiento}\n")

akon = Estudiante("22.782.651-7","Akon","Bustamante","Programacion", "30/07/2008")
javiera = Estudiante("25.019.325-1", "Javiera", "Zapata" ,"Programacion", "10/05/2009")
benjamin = Estudiante("22.926.226-2","Benjamin","Delgado","Programacion", "07/01/2009")

akon
javiera
benjamin