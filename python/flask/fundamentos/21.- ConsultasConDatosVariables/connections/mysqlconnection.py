# ==========================================================
# MYSQL CONNECTION
# ==========================================================

import pymysql.cursors


# ==========================================================
# CLASE MYSQL CONNECTION
# ==========================================================

class MySQLConnection:
    """
    Administra una conexión con una base de datos MySQL.
    """

    def __init__(self, db):
        """
        Establece una conexión con la base de datos
        recibida como parámetro.
        """

        self.connection = pymysql.connect(

            host="localhost",

            user="root",

            password="1234",

            database="primera_flask",

            charset="utf8mb4",

            cursorclass=pymysql.cursors.DictCursor,

            autocommit=True

        )


    # ======================================================
    # EJECUTAR CONSULTA
    # ======================================================

    def query_db(self, query, data=None):
        """
        Ejecuta una consulta SQL.

        query:
            Cadena con la consulta SQL.

        data:
            Diccionario con los valores que serán enviados
            a los parámetros de la consulta.
        """

        with self.connection.cursor() as cursor:

            try:

                # --------------------------------------------------
                # Ejecutar consulta con parámetros.
                # --------------------------------------------------

                cursor.execute(query, data)


                # --------------------------------------------------
                # SELECT
                # --------------------------------------------------

                if query.strip().lower().startswith("select"):

                    resultados = cursor.fetchall()

                    return resultados


                # --------------------------------------------------
                # INSERT
                # --------------------------------------------------

                elif query.strip().lower().startswith("insert"):

                    return cursor.lastrowid


                # --------------------------------------------------
                # UPDATE / DELETE
                # --------------------------------------------------

                else:

                    return None


            except Exception as e:

                print("Something went wrong:")

                print(e)

                return False


            finally:

                # --------------------------------------------------
                # Cerrar conexión.
                # --------------------------------------------------

                self.connection.close()


# ==========================================================
# FUNCIÓN DE CONEXIÓN
# ==========================================================

def connectToMySQL(db):
    """
    Crea y devuelve una instancia de MySQLConnection.
    """

    return MySQLConnection(db)