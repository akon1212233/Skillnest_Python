import pymysql.cursors

class MySQLConnection:
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
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(query, data)
                if query.strip().lower().startswith("select"):
                    resultados = cursor.fetchall()
                    return resultados
                elif query.strip().lower().startswith("insert"):
                    return cursor.lastrowid
                else:
                    return None
            except Exception as e:
                print("Ocurrió un error en la base de datos:")
                print(e)
                return False
            finally:
                self.connection.close()

def connectToMySQL(db):
    return MySQLConnection(db)
