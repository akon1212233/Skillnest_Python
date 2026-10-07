# ==========================================================
# MODELO USUARIO
# ==========================================================

from connection.mysqlconnection import connectToMySQL


# ==========================================================
# CLASE USUARIO
# ==========================================================

class Usuario:
    """
    Representa un registro de la tabla usuarios.
    """

    def __init__(self, data):
        """
        Recibe un diccionario proveniente de MySQL
        y lo transforma en un objeto Usuario.
        """

        self.id = data["id"]

        self.nombre = data["nombre"]

        self.apellido = data["apellido"]

        self.email = data["email"]

        self.created_at = data["created_at"]

        self.updated_at = data["updated_at"]


    # ======================================================
    # READ
    # OBTENER TODOS LOS USUARIOS
    # ======================================================

    @classmethod
    def get_all(cls):
        """
        Recupera todos los usuarios.
        """

        query = """
            SELECT
                id,
                nombre,
                apellido,
                email,
                created_at,
                updated_at
            FROM usuarios
            ORDER BY id;
        """


        resultados = connectToMySQL(
            "esquema_usuarios"
        ).query_db(query)


        usuarios = []


        for usuario in resultados:

            usuarios.append(
                cls(usuario)
            )


        return usuarios


    # ======================================================
    # READ
    # OBTENER USUARIO POR ID
    # ======================================================

    @classmethod
    def get_by_id(cls, id):
        """
        Busca un usuario específico mediante su ID.

        Si existe:
            devuelve un objeto Usuario.

        Si no existe:
            devuelve None.
        """

        query = """
            SELECT
                id,
                nombre,
                apellido,
                email,
                created_at,
                updated_at
            FROM usuarios
            WHERE id = %(id)s;
        """


        data = {
            "id": id
        }


        resultados = connectToMySQL(
            "esquema_usuarios"
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
    # CREATE
    # CREAR USUARIO
    # ======================================================

    @classmethod
    def save(cls, data):
        """
        Crea un nuevo usuario.
        """

        query = """
            INSERT INTO usuarios
            (
                nombre,
                apellido,
                email,
                created_at,
                updated_at
            )
            VALUES
            (
                %(nombre)s,
                %(apellido)s,
                %(email)s,
                NOW(),
                NOW()
            );
        """


        return connectToMySQL(
            "esquema_usuarios"
        ).query_db(
            query,
            data
        )


    # ======================================================
    # UPDATE
    # ACTUALIZAR USUARIO
    # ======================================================

    @classmethod
    def update(cls, data):
        """
        Actualiza los datos de un usuario existente.

        data debe contener:

        id
        nombre
        apellido
        email
        """

        query = """
            UPDATE usuarios
            SET
                nombre = %(nombre)s,
                apellido = %(apellido)s,
                email = %(email)s,
                updated_at = NOW()
            WHERE id = %(id)s;
        """


        return connectToMySQL(
            "esquema_usuarios"
        ).query_db(
            query,
            data
        )


    # ======================================================
    # DELETE
    # ELIMINAR USUARIO
    # ======================================================

    @classmethod
    def delete(cls, id):
        """
        Elimina un usuario utilizando su ID.
        """

        query = """
            DELETE FROM usuarios
            WHERE id = %(id)s;
        """


        data = {
            "id": id
        }


        return connectToMySQL(
            "esquema_usuarios"
        ).query_db(
            query,
            data
        )