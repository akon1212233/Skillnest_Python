# ==========================================================
# MODELO RESTAURANTE
# ==========================================================

from flask_app.config.mysqlconnection import connectToMySQL

from flask_app.models.taco import Taco


class Restaurante:

    def __init__(self, data):
        """
        Convierte un registro de MySQL
        en un objeto Restaurante.
        """

        self.id = data["id"]

        self.nombre = data["nombre"]

        self.created_at = data["created_at"]

        self.updated_at = data["updated_at"]


        # --------------------------------------------------
        # Lista donde posteriormente almacenaremos
        # los objetos Taco relacionados.
        # --------------------------------------------------

        self.tacos = []


    # ======================================================
    # CREATE
    # ======================================================

    @classmethod
    def save(cls, datos):
        """
        Crea un nuevo restaurante.
        """

        query = """
            INSERT INTO restaurantes
            (
                nombre
            )
            VALUES
            (
                %(nombre)s
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
    # OBTENER TODOS LOS RESTAURANTES
    # ======================================================

    @classmethod
    def get_all(cls):
        """
        Recupera todos los restaurantes.
        """

        query = """
            SELECT
                id,
                nombre,
                created_at,
                updated_at
            FROM restaurantes
            ORDER BY id;
        """


        resultados = connectToMySQL(
            "esquema_tacos"
        ).query_db(
            query
        )


        restaurantes = []


        for restaurante in resultados:

            restaurantes.append(
                cls(restaurante)
            )


        return restaurantes


    # ======================================================
    # READ
    # RESTAURANTE + TACOS
    # ======================================================

    @classmethod
    def get_restaurante_y_tacos(cls, datos):
        """
        Recupera un restaurante junto con
        todos los tacos relacionados.
        """

        query = """
            SELECT

                restaurantes.id
                    AS restaurante_id,

                restaurantes.nombre
                    AS restaurante_nombre,

                restaurantes.created_at
                    AS restaurante_created_at,

                restaurantes.updated_at
                    AS restaurante_updated_at,

                tacos.id
                    AS taco_id,

                tacos.tortilla
                    AS taco_tortilla,

                tacos.guiso
                    AS taco_guiso,

                tacos.salsa
                    AS taco_salsa,

                tacos.restaurante_id
                    AS taco_restaurante_id,

                tacos.created_at
                    AS taco_created_at,

                tacos.updated_at
                    AS taco_updated_at

            FROM restaurantes

            LEFT JOIN tacos
                ON tacos.restaurante_id = restaurantes.id

            WHERE restaurantes.id = %(id)s;
        """


        resultados = connectToMySQL(
            "esquema_tacos"
        ).query_db(
            query,
            datos
        )


        # --------------------------------------------------
        # Si no existe el restaurante.
        # --------------------------------------------------

        if not resultados:

            return None


        # --------------------------------------------------
        # Crear objeto Restaurante.
        # --------------------------------------------------

        restaurante_data = {

            "id": resultados[0][
                "restaurante_id"
            ],

            "nombre": resultados[0][
                "restaurante_nombre"
            ],

            "created_at": resultados[0][
                "restaurante_created_at"
            ],

            "updated_at": resultados[0][
                "restaurante_updated_at"
            ]

        }


        restaurante = cls(
            restaurante_data
        )


        # --------------------------------------------------
        # Recorrer los resultados del JOIN.
        # --------------------------------------------------

        for fila_en_db in resultados:

            # --------------------------------------------------
            # Como utilizamos LEFT JOIN, el restaurante puede
            # no tener tacos.
            #
            # En ese caso taco_id será None.
            # --------------------------------------------------

            if fila_en_db["taco_id"] is not None:

                datos_taco = {

                    "id": fila_en_db[
                        "taco_id"
                    ],

                    "tortilla": fila_en_db[
                        "taco_tortilla"
                    ],

                    "guiso": fila_en_db[
                        "taco_guiso"
                    ],

                    "salsa": fila_en_db[
                        "taco_salsa"
                    ],

                    "restaurante_id": fila_en_db[
                        "taco_restaurante_id"
                    ],

                    "created_at": fila_en_db[
                        "taco_created_at"
                    ],

                    "updated_at": fila_en_db[
                        "taco_updated_at"
                    ]

                }


                # --------------------------------------------------
                # Convertimos el diccionario en un objeto Taco
                # y lo agregamos al restaurante.
                # --------------------------------------------------

                restaurante.tacos.append(
                    Taco(datos_taco)
                )


        return restaurante