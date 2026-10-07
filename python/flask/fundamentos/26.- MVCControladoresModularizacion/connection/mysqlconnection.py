# ==========================================================
# MYSQL CONNECTION
# ==========================================================

import pymysql.cursors


# ==========================================================
# CLASE MYSQL CONNECTION
# ==========================================================

class MySQLConnection:
    """
    Administra una conexión con MySQL.
    """

    def __init__(self, db):
        """
        Recibe el nombre de la base de datos
        y establece la conexión.
        """

        connection = pymysql.connect(

            host="localhost",

            user="root",

            password="1234",

            database=db,

            charset="utf8mb4",

            cursorclass=pymysql.cursors.DictCursor,

            autocommit=True

        )


        self.connection = connection


    # ======================================================
    # EJECUTAR CONSULTA
    # ======================================================

    def query_db(
        self,
        query,
        data=None
    ):
        """
        Ejecuta una consulta SQL.
        """

        with self.connection.cursor() as cursor:

            try:

                # --------------------------------------------------
                # Mostrar consulta durante el desarrollo.
                # --------------------------------------------------

                query_debug = cursor.mogrify(
                    query,
                    data
                )

                print(
                    "Running Query:",
                    query_debug
                )


                # --------------------------------------------------
                # Ejecutar consulta.
                # --------------------------------------------------

                cursor.execute(
                    query,
                    data
                )


                # --------------------------------------------------
                # INSERT
                # --------------------------------------------------

                if query.lower().find("insert") >= 0:

                    self.connection.commit()

                    return cursor.lastrowid


                # --------------------------------------------------
                # SELECT
                # --------------------------------------------------

                elif query.lower().find("select") >= 0:

                    result = cursor.fetchall()

                    return result


                # --------------------------------------------------
                # UPDATE / DELETE
                # --------------------------------------------------

                else:

                    self.connection.commit()


            except Exception as e:

                print(
                    "Something went wrong:",
                    e
                )

                return False


            finally:

                # --------------------------------------------------
                # Cerrar conexión.
                # --------------------------------------------------

                self.connection.close()


# ==========================================================
# FUNCIÓN AUXILIAR
# ==========================================================

def connectToMySQL(db):
    """
    Recibe el nombre de una base de datos
    y devuelve una instancia de MySQLConnection.
    """

    return MySQLConnection(db)