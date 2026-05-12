class estudiante:
    colegio = "VVH"
    estudiantes = []
    def __init__(self, name, nota):
        self.name = name
        self.nota = nota
        estudiante.estudiantes.append(self)
    def mostrarInfo(self):
        print(f"Nombre : {self.name}")
        print(f"Nota: {self.nota}")
    @classmethod
    def cambiarColegio(cls, nuevoNombre):
        cls.colegio = nuevoNombre
    @staticmethod
    def aprobar(nota):
        if nota > 4.0:
            return True
        else:
            return False
    def cantidadEstudiantes(cls):
        return len(cls.estudiantes)

