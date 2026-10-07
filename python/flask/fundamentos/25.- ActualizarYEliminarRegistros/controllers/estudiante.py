# ==========================================================
# MODELO ESTUDIANTE
# ==========================================================

from connection.mysqlconnection import connectToMySQL


# ==========================================================
# CLASE ESTUDIANTE
# ==========================================================

class Estudiante:
    """
    Representa un registro de la tabla estudiantes.
    """

    def __init__(self, data):
        """
        Recibe un diccionario proveniente de MySQL
        y lo convierte en un objeto Estudiante.
        """

        self.id_estudiante = data["id_estudiante"]

        self.nombre = data["nombre"]

        self.email = data["email"]

        self.created_at = data["created_at"]


    # ======================================================
    # READ
    # OBTENER TODOS
    # ======================================================

    @classmethod
    def get_all(cls):
        """
        Recupera todos los estudiantes.
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
            "esquema_estudiantes"
        ).query_db(query)


        estudiantes = []


        for estudiante in resultados:

            estudiantes.append(
                cls(estudiante)
            )


        return estudiantes


    # ======================================================
    # READ
    # OBTENER UNO POR ID
    # ======================================================

    @classmethod
    def get_by_id(cls, id_estudiante):
        """
        Busca un estudiante específico mediante su ID.

        Si existe:
            devuelve un objeto Estudiante.

        Si no existe:
            devuelve None.
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
            "esquema_estudiantes"
        ).query_db(
            query,
            data
        )


        if resultados:

            return cls(
                resultados[0]
            )


        return None


    # ======================================================
    # UPDATE
    # ACTUALIZAR ESTUDIANTE
    # ======================================================

    @classmethod
    def actualizar(cls, data):
        """
        Actualiza el nombre y email de un estudiante.

        data debe contener:

        id_estudiante
        nombre
        email
        """

        query = """
            UPDATE estudiantes
            SET
                nombre = %(nombre)s,
                email = %(email)s
            WHERE id_estudiante = %(id_estudiante)s;
        """


        return connectToMySQL(
            "esquema_estudiantes"
        ).query_db(
            query,
            data
        )


    # ======================================================
    # DELETE
    # ELIMINAR ESTUDIANTE
    # ======================================================

    @classmethod
    def eliminar(cls, data):
        """
        Elimina un estudiante mediante su ID.
        """

        query = """
            DELETE FROM estudiantes
            WHERE id_estudiante = %(id_estudiante)s;
        """


        return connectToMySQL(
            "esquema_estudiantes"
        ).query_db(
            query,
            data
        )