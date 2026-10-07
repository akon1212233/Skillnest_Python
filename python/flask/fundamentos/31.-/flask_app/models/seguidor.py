from flask_app.config.mysqlconnection import connectToMySQL


class Seguidor:
    """
    Representa una relación entre dos usuarios.
    """

    @classmethod
    def get_all(cls):
        """
        Obtiene todas las relaciones utilizando SELF JOIN.

        u = usuario seguido
        s = seguidor
        """

        query = """
            SELECT
                u.id AS usuario_id,
                CONCAT(
                    u.nombre,
                    " ",
                    u.apellido
                ) AS usuario_nombre,

                s.id AS seguidor_id,
                CONCAT(
                    s.nombre,
                    " ",
                    s.apellido
                ) AS seguidor_nombre

            FROM seguidores f

            INNER JOIN usuarios u
                ON f.usuario_id = u.id

            INNER JOIN usuarios s
                ON f.seguidor_id = s.id

            ORDER BY
                u.nombre,
                u.apellido,
                s.nombre,
                s.apellido;
        """

        return connectToMySQL(
            "esquema_seguidores"
        ).query_db(query)


    @classmethod
    def existe(cls, data):
        """
        Comprueba si ya existe una relación.
        """

        query = """
            SELECT
                id
            FROM seguidores
            WHERE usuario_id = %(usuario_id)s
              AND seguidor_id = %(seguidor_id)s;
        """

        resultado = connectToMySQL(
            "esquema_seguidores"
        ).query_db(
            query,
            data
        )

        return bool(resultado)


    @classmethod
    def seguir(cls, data):
        """
        Crea una relación de seguimiento.
        """

        query = """
            INSERT INTO seguidores
            (
                usuario_id,
                seguidor_id
            )
            VALUES
            (
                %(usuario_id)s,
                %(seguidor_id)s
            );
        """

        return connectToMySQL(
            "esquema_seguidores"
        ).query_db(
            query,
            data
        )