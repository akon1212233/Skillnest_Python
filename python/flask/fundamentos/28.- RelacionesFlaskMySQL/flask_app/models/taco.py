# ==========================================================
# MODELO TACO
# ==========================================================

from flask_app.config.mysqlconnection import connectToMySQL


class Taco:

    def __init__(self, data):
        """
        Convierte un registro de MySQL
        en un objeto Taco.
        """

        self.id = data["id"]
        self.tortilla = data["tortilla"]
        self.guiso = data["guiso"]
        self.salsa = data["salsa"]
        self.restaurante_id = data["restaurante_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]


    # ======================================================
    # CREATE
    # ======================================================

    @classmethod
    def save(cls, datos):
        """
        Crea un nuevo taco.

        Ahora necesitamos también el ID
        del restaurante al que pertenece.
        """

        query = """
            INSERT INTO tacos
            (
                tortilla,
                guiso,
                salsa,
                restaurante_id
            )
            VALUES
            (
                %(tortilla)s,
                %(guiso)s,
                %(salsa)s,
                %(restaurante_id)s
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
                restaurante_id,
                created_at,
                updated_at
            FROM tacos
            ORDER BY id;
        """


        resultados = connectToMySQL(
            "esquema_tacos"
        ).query_db(
            query
        )


        tacos = []


        for taco in resultados:

            tacos.append(
                cls(taco)
            )


        return tacos