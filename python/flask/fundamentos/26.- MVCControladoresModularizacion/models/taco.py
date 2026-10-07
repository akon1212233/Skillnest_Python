# ==========================================================
# MODELO TACO
# ==========================================================

from connection.mysqlconnection import connectToMySQL


# ==========================================================
# CLASE TACO
# ==========================================================

class Taco:

    def __init__(
        self,
        data
    ):
        """
        Convierte un registro de MySQL
        en un objeto Taco.
        """

        self.id = data["id"]

        self.tortilla = data["tortilla"]

        self.guiso = data["guiso"]

        self.salsa = data["salsa"]

        self.created_at = data["created_at"]

        self.updated_at = data["updated_at"]


    # ======================================================
    # CREATE
    # ======================================================

    @classmethod
    def save(
        cls,
        datos
    ):
        """
        Crea un nuevo taco.
        """

        query = """
            INSERT INTO tacos
            (
                tortilla,
                guiso,
                salsa
            )
            VALUES
            (
                %(tortilla)s,
                %(guiso)s,
                %(salsa)s
            );
        """


        return connectToMySQL(
            "esquema_tacos"
        ).query_db(
            query,
            datos
        )


    # ======================================================
    # READ
    # OBTENER TODOS
    # ======================================================

    @classmethod
    def get_all(cls):
        """
        Recupera todos los tacos.
        """

        query = """
            SELECT
                id,
                tortilla,
                guiso,
                salsa,
                created_at,
                updated_at
            FROM tacos
            ORDER BY id;
        """


        tacos_en_bd = connectToMySQL(
            "esquema_tacos"
        ).query_db(
            query
        )


        tacos = []


        for taco in tacos_en_bd:

            tacos.append(
                cls(taco)
            )


        return tacos


    # ======================================================
    # READ
    # OBTENER UNO
    # ======================================================

    @classmethod
    def get_one(
        cls,
        datos
    ):
        """
        Recupera un taco mediante su ID.
        """

        query = """
            SELECT
                id,
                tortilla,
                guiso,
                salsa,
                created_at,
                updated_at
            FROM tacos
            WHERE id = %(id)s;
        """


        taco_en_db = connectToMySQL(
            "esquema_tacos"
        ).query_db(
            query,
            datos
        )


        if not taco_en_db:

            return None


        return cls(
            taco_en_db[0]
        )


    # ======================================================
    # UPDATE
    # ======================================================

    @classmethod
    def update(
        cls,
        datos
    ):
        """
        Actualiza un taco existente.
        """

        query = """
            UPDATE tacos
            SET
                tortilla = %(tortilla)s,
                guiso = %(guiso)s,
                salsa = %(salsa)s
            WHERE id = %(id)s;
        """


        return connectToMySQL(
            "esquema_tacos"
        ).query_db(
            query,
            datos
        )


    # ======================================================
    # DELETE
    # ======================================================

    @classmethod
    def delete(
        cls,
        datos
    ):
        """
        Elimina un taco mediante su ID.
        """

        query = """
            DELETE FROM tacos
            WHERE id = %(id)s;
        """


        return connectToMySQL(
            "esquema_tacos"
        ).query_db(
            query,
            datos
        )