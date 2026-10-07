from flask_app.config.mysqlconnection import connectToMySQL


class Estudiante:
    """
    Representa un registro de la tabla estudiantes.
    """

    def __init__(self, data):
        self.id_estudiante = data["id_estudiante"]
        self.nombre = data["nombre"]
        self.email = data["email"]
        self.created_at = data["created_at"]


    @classmethod
    def get_all(cls):
        """
        Obtiene todos los estudiantes.
        """

        query = """
            SELECT
                id_estudiante,
                nombre,
                email,
                created_at
            FROM estudiantes
            ORDER BY id_estudiante;
        """


        resultados = connectToMySQL(
            "esquema_educacion"
        ).query_db(query)


        estudiantes = []


        for estudiante in resultados:

            estudiantes.append(
                cls(estudiante)
            )


        return estudiantes


    @classmethod
    def get_by_id(cls, id_estudiante):
        """
        Busca un estudiante específico por su ID.
        """

        query = """
            SELECT
                id_estudiante,
                nombre,
                email,
                created_at
            FROM estudiantes
            WHERE id_estudiante = %(id_estudiante)s;
        """


        data = {
            "id_estudiante": id_estudiante
        }


        resultados = connectToMySQL(
            "esquema_educacion"
        ).query_db(
            query,
            data
        )


        if resultados:

            return cls(
                resultados[0]
            )


        return None