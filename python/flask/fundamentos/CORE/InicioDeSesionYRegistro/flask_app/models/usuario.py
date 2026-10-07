from flask_app.config.mysqlconnection import MySQLConnection

class Usuario:
    def __init__(self, data):
        self.idUsuario = data["idUsuario"]
        self.nombre = data["nombre"]
        self.apellido = data["apellido"]
        self.email = data["email"]
        self.password_hash = data["password_hash"]
        self.fecha_nacimiento = data["fecha_nacimiento"]
        self.created_at = data["created_at"]

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO usuarios (nombre, apellido, email, password_hash, fecha_nacimiento) 
            VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password_hash)s, %(fecha_nacimiento)s);
        """
        return MySQLConnection("sessions_register").query_db(query, data)

    @classmethod
    def get_user_by_email(cls, email):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        data = {"email": email}
        resultado = MySQLConnection("sessions_register").query_db(query, data)
        if resultado and len(resultado) > 0:
            return resultado[0]
        return None

    @classmethod
    def get_user_by_id(cls, usuario_id):
        query = "SELECT * FROM usuarios WHERE idUsuario = %(id)s;"
        data = {"id": usuario_id}
        resultado = MySQLConnection("sessions_register").query_db(query, data)
        if resultado and len(resultado) > 0:
            return resultado[0]
        return None
