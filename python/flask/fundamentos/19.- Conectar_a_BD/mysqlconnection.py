# ==========================================================
# MYSQL CONNECTION
# ==========================================================
#
# Esta clase centraliza la conexión entre Python y MySQL.
#
# La idea es que nuestros modelos no tengan que encargarse
# directamente de crear una conexión cada vez que necesitan
# ejecutar una consulta.
#
# ==========================================================


import pymysql.cursors


# ==========================================================
# CLASE MYSQL CONNECTION
# ==========================================================

class MySQLConnection:
    """
    Administra la conexión con una base de datos MySQL.
    """

    def __init__(self, db):
        """
        Recibe el nombre de la base de datos
        y establece una conexión.
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

        SELECT:
            Retorna una lista de diccionarios.

        INSERT:
            Retorna el ID generado.

        UPDATE / DELETE:
            No retornan registros.

        Error:
            Retorna False.
        """

        with self.connection.cursor() as cursor:

            try:

                # --------------------------------------------------
                # Mostrar la consulta durante el desarrollo.
                # --------------------------------------------------

                print("Running Query:")

                print(query)


                # --------------------------------------------------
                # Ejecutar consulta.
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
                # Cerramos la conexión.
                # --------------------------------------------------

                self.connection.close()


# ==========================================================
# FUNCIÓN AUXILIAR
# ==========================================================

def connectToMySQL(db):
    """
    Recibe el nombre de una base de datos y devuelve
    una instancia de MySQLConnection.
    """

    return MySQLConnection(db)