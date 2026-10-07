import pymysql
from flask import current_app


class MySQLConnection:
    """Conexión pequeña y reutilizable a MySQL mediante PyMySQL."""

    @staticmethod
    def get_db():
        return pymysql.connect(
            host=current_app.config["MYSQL_HOST"],
            port=current_app.config["MYSQL_PORT"],
            user=current_app.config["MYSQL_USER"],
            password=current_app.config["MYSQL_PASSWORD"],
            database=current_app.config["MYSQL_DB"],
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False,
        )

    @classmethod
    def query_db(cls, query, data=None, fetchone=False, fetchall=False):
        connection = cls.get_db()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, data or ())
                if fetchone:
                    return cursor.fetchone()
                if fetchall:
                    return cursor.fetchall()
                connection.commit()
                return cursor.lastrowid
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()
