from connections.connector import connectToMySQL
class Mascota:
    """
    Representa un registro de la tabla mascotas.
    """

    def __init__(self, data):
        """
        Recibe un diccionario proveniente de MySQL
        y lo transforma en atributos del objeto.
        """
        self.id = data["id"]
        self.nombre = data["nombre"]
        self.tipo = data["tipo"]
        self.color = data["color"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def get_all(cls):
        """
        Consulta todas las mascotas almacenadas
        en la base de datos.

        Retorna una lista de objetos Mascota.
        """

        query = """
            SELECT *
            FROM mascotas;
        """
        resultados = connectToMySQL(
            "primera_flask"
        ).query_db(query)
        mascotas = []
        for mascota in resultados:
            mascotas.append(cls(mascota))
        return mascotas