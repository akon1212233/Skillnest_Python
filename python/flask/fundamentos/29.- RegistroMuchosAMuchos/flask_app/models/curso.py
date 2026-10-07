from flask_app.config.mysqlconnection import connectToMySQL


class Curso:
    """
    Representa un registro de la tabla cursos.
    """

    def __init__(self, data):
        self.id_curso = data["id_curso"]
        self.nombre_curso = data["nombre_curso"]
        self.descripcion = data["descripcion"]
        self.created_at = data["created_at"]


    @classmethod
    def get_all(cls):
        """
        Obtiene todos los cursos.
        """

        query = """
            SELECT
                id_curso,
                nombre_curso,
                descripcion,
                created_at
            FROM cursos
            ORDER BY id_curso;
        """


        resultados = connectToMySQL(
            "esquema_educacion"
        ).query_db(query)


        cursos = []


        for curso in resultados:

            cursos.append(
                cls(curso)
            )


        return cursos


    @classmethod
    def get_by_id(cls, id_curso):
        """
        Busca un curso específico por su ID.
        """

        query = """
            SELECT
                id_curso,
                nombre_curso,
                descripcion,
                created_at
            FROM cursos
            WHERE id_curso = %(id_curso)s;
        """


        data = {
            "id_curso": id_curso
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