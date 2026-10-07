from academia.config.conexion import connectToMySQL

BD = "academia_talleres"


class Alumno:
    """Representa un registro de la tabla alumnos."""

    def __init__(self, datos):
        self.id = datos["id"]
        self.nombre = datos["nombre"]
        self.apellido = datos["apellido"]
        self.edad = datos["edad"]
        self.created_at = datos["created_at"]
        self.updated_at = datos["updated_at"]
        self.taller_id = datos["taller_id"]

    @classmethod
    def guardar(cls, datos):
        """Crea un alumno asociado a un taller."""
        consulta = """
            INSERT INTO alumnos
                (nombre, apellido, edad, taller_id)
            VALUES
                (%(nombre)s, %(apellido)s, %(edad)s, %(taller_id)s);
        """
        return connectToMySQL(BD).query_db(consulta, datos)
