import pymysql.cursors


class MySQLConnection:
    """
    Administra la conexión entre Flask y MySQL.
    """

    def __init__(self, db):
        self.connection = pymysql.connect(
            host="localhost",
            user="root",
            password="1234",
            database=db,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )


    def query_db(self, query, data=None):
        """
        Ejecuta una consulta SQL.

        SELECT:
            devuelve una lista de diccionarios.

        INSERT:
            devuelve el ID generado o las filas afectadas.

        UPDATE / DELETE:
            devuelve las filas afectadas.

        Error:
            devuelve False.
        """

        with self.connection.cursor() as cursor:

            try:

                cursor.execute(
                    query,
                    data
                )


                if query.strip().lower().startswith("select"):

                    return cursor.fetchall()


                if query.strip().lower().startswith("insert"):

                    return cursor.lastrowid or cursor.rowcount


                return cursor.rowcount


            except Exception as e:

                print(
                    "Something went wrong:",
                    e
                )

                return False


            finally:

                self.connection.close()


def connectToMySQL(db):
    """
    Recibe el nombre de la base de datos
    y devuelve una conexión.
    """

    return MySQLConnection(db)