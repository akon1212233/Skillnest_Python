from flask_app.config.mysqlconnection import connectToMySQL


class Inscripcion:
    """
    Representa una relación entre un estudiante y un curso.
    """

    @classmethod
    def existe(cls, data):
        """
        Comprueba si la relación ya existe.
        """

        query = """
            SELECT
                estudiante_id,
                curso_id
            FROM inscripciones
            WHERE estudiante_id = %(estudiante_id)s
              AND curso_id = %(curso_id)s;
        """


        resultado = connectToMySQL(
            "esquema_educacion"
        ).query_db(
            query,
            data
        )


        return bool(resultado)


    @classmethod
    def inscribir_estudiante_en_curso(cls, data):
        """
        Crea una relación entre un estudiante y un curso.
        """

        query = """
            INSERT INTO inscripciones
            (
                estudiante_id,
                curso_id
            )
            VALUES
            (
                %(estudiante_id)s,
                %(curso_id)s
            );
        """


        return connectToMySQL(
            "esquema_educacion"
        ).query_db(
            query,
            data
        )


    @classmethod
    def get_all(cls):
        """
        Obtiene todas las inscripciones mostrando
        los nombres del estudiante y del curso.
        """

        query = """
            SELECT
                estudiantes.id_estudiante,
                estudiantes.nombre AS estudiante,
                estudiantes.email,
                cursos.id_curso,
                cursos.nombre_curso

            FROM inscripciones

            INNER JOIN estudiantes
                ON inscripciones.estudiante_id =
                   estudiantes.id_estudiante

            INNER JOIN cursos
                ON inscripciones.curso_id =
                   cursos.id_curso

            ORDER BY
                estudiantes.id_estudiante,
                cursos.id_curso;
        """


        return connectToMySQL(
            "esquema_educacion"
        ).query_db(query)