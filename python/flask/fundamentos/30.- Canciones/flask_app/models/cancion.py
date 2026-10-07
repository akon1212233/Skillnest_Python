from flask_app.config.mysqlconnection import connectToMySQL


class Cancion:
    """
    Representa un registro de la tabla canciones.
    """

    def __init__(self, data):
        self.id = data["id"]
        self.titulo = data["titulo"]
        self.artista = data["artista"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.usuarios = []

    @classmethod
    def get_all(cls):
        """
        Obtiene todas las canciones.
        """

        query = """
            SELECT
                id,
                titulo,
                artista,
                created_at,
                updated_at
            FROM canciones
            ORDER BY id;
        """

        resultados = connectToMySQL(
            "esquema_canciones"
        ).query_db(query)

        canciones = []

        for cancion in resultados:
            canciones.append(cls(cancion))

        return canciones

    @classmethod
    def get_by_id(cls, id):
        """
        Obtiene una canción por su ID.
        """

        query = """
            SELECT
                id,
                titulo,
                artista,
                created_at,
                updated_at
            FROM canciones
            WHERE id = %(id)s;
        """

        data = {
            "id": id
        }

        resultados = connectToMySQL(
            "esquema_canciones"
        ).query_db(query, data)

        if resultados:
            return cls(resultados[0])

        return None

    @classmethod
    def save(cls, data):
        """
        Crea una nueva canción.
        """

        query = """
            INSERT INTO canciones
            (
                titulo,
                artista
            )
            VALUES
            (
                %(titulo)s,
                %(artista)s
            );
        """

        return connectToMySQL(
            "esquema_canciones"
        ).query_db(query, data)

    @classmethod
    def get_by_id_with_users(cls, data):
        """
        Obtiene una canción y todos los usuarios
        que la tienen como favorita.
        """

        query = """
            SELECT
                canciones.id AS cancion_id,
                canciones.titulo AS cancion_titulo,
                canciones.artista AS cancion_artista,
                canciones.created_at AS cancion_created_at,
                canciones.updated_at AS cancion_updated_at,

                usuarios.id AS usuario_id,
                usuarios.nombre AS usuario_nombre,
                usuarios.email AS usuario_email,
                usuarios.contrasena AS usuario_contrasena,
                usuarios.created_at AS usuario_created_at,
                usuarios.updated_at AS usuario_updated_at

            FROM canciones

            LEFT JOIN favoritos
                ON favoritos.cancion_id = canciones.id

            LEFT JOIN usuarios
                ON favoritos.usuario_id = usuarios.id

            WHERE canciones.id = %(id)s;
        """

        resultados = connectToMySQL(
            "esquema_canciones"
        ).query_db(query, data)

        if not resultados:
            return None

        cancion_data = {
            "id": resultados[0]["cancion_id"],
            "titulo": resultados[0]["cancion_titulo"],
            "artista": resultados[0]["cancion_artista"],
            "created_at": resultados[0]["cancion_created_at"],
            "updated_at": resultados[0]["cancion_updated_at"]
        }

        cancion = cls(cancion_data)

        for fila in resultados:

            if fila["usuario_id"] is not None:

                cancion.usuarios.append({
                    "id": fila["usuario_id"],
                    "nombre": fila["usuario_nombre"],
                    "email": fila["usuario_email"],
                    "contrasena": fila["usuario_contrasena"],
                    "created_at": fila["usuario_created_at"],
                    "updated_at": fila["usuario_updated_at"]
                })

        return cancion

    @classmethod
    def get_users_not_favorited(cls, data):
        """
        Obtiene solamente los usuarios que todavía
        no han marcado la canción como favorita.
        """

        query = """
            SELECT
                usuarios.id,
                usuarios.nombre,
                usuarios.email,
                usuarios.contrasena,
                usuarios.created_at,
                usuarios.updated_at

            FROM usuarios

            LEFT JOIN favoritos
                ON favoritos.usuario_id = usuarios.id
                AND favoritos.cancion_id = %(cancion_id)s

            WHERE favoritos.usuario_id IS NULL

            ORDER BY usuarios.nombre;
        """

        return connectToMySQL(
            "esquema_canciones"
        ).query_db(query, data)