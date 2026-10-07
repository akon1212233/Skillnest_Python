from flask_app.config.mysqlconnection import MySQLConnection


class Usuario:
    @staticmethod
    def crear(data):
        query = """
            INSERT INTO usuarios (nombre, apellido, email, password)
            VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password)s)
        """
        return MySQLConnection.query_db(query, data)

    @staticmethod
    def buscar_por_email(email):
        return MySQLConnection.query_db(
            "SELECT * FROM usuarios WHERE email = %(email)s LIMIT 1",
            {"email": email},
            fetchone=True,
        )

    @staticmethod
    def buscar_por_id(user_id):
        return MySQLConnection.query_db(
            "SELECT id, nombre, apellido, email, created_at FROM usuarios WHERE id = %(id)s",
            {"id": user_id},
            fetchone=True,
        )
