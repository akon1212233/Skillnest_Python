# ==========================================================
# MODELO MASCOTA
# ==========================================================

from connection.mysqlconnection import connectToMySQL


# ==========================================================
# CLASE MASCOTA
# ==========================================================

class Mascota:
    """
    Representa un registro de la tabla mascotas.
    """

    def __init__(self, data):
        """
        Recibe un diccionario proveniente de MySQL
        y lo transforma en un objeto Mascota.
        """

        self.id = data["id"]

        self.nombre = data["nombre"]

        self.tipo = data["tipo"]

        self.color = data["color"]

        self.created_at = data["created_at"]

        self.updated_at = data["updated_at"]


    # ======================================================
    # READ
    # OBTENER TODAS LAS MASCOTAS
    # ======================================================

    @classmethod
    def get_all(cls):
        """
        Recupera todas las mascotas de la base de datos.
        """

        query = """
            SELECT
                id,
                nombre,
                tipo,
                color,
                created_at,
                updated_at
            FROM mascotas
            ORDER BY id;
        """


        resultados = connectToMySQL(
            "primera_flask"
        ).query_db(query)


        mascotas = []


        for mascota in resultados:

            mascotas.append(
                cls(mascota)
            )


        return mascotas


    # ======================================================
    # CREATE
    # CREAR NUEVA MASCOTA
    # ======================================================

    @classmethod
    def save(cls, datos):
        """
        Crea una nueva mascota en la base de datos.

        Recibe un diccionario llamado "datos" con:

        nombre
        tipo
        color
        """

        # --------------------------------------------------
        # CONSULTA INSERT
        # --------------------------------------------------
        #
        # Los valores variables no se concatenan
        # directamente dentro del SQL.
        #
        # Utilizamos placeholders.
        # --------------------------------------------------

        query = """
            INSERT INTO mascotas
            (
                nombre,
                tipo,
                color,
                created_at,
                updated_at
            )
            VALUES
            (
                %(nombre)s,
                %(tipo)s,
                %(color)s,
                NOW(),
                NOW()
            );
        """


        # --------------------------------------------------
        # EJECUTAR CONSULTA
        # --------------------------------------------------

        return connectToMySQL(
            "primera_flask"
        ).query_db(
            query,
            datos
        )
