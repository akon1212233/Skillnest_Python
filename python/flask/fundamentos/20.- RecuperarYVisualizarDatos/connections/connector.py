# ==========================================================
# MYSQL CONNECTION
# ==========================================================

import pymysql.cursors


# ==========================================================
# CLASE DE CONEXIÓN
# ==========================================================

class MySQLConnection:
    """
    Administra una conexión con una base de datos MySQL.
    """

    def __init__(self, db):
        """
        Recibe el nombre de la base de datos y establece
        la conexión con el servidor MySQL.
        """

        self.connection = pymysql.connect(

            host="localhost",

            user="root",

            password="12123",

            database='primera_flask',

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

        Para SELECT:
            devuelve una lista de diccionarios.

        Para INSERT:
            devuelve el ID generado.

        Para UPDATE / DELETE:
            devuelve None.

        Si ocurre un error:
            devuelve False.
        """

        with self.connection.cursor() as cursor:

            try:

                # --------------------------------------------------
                # Ejecutar consulta
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
                # Cerrar conexión
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