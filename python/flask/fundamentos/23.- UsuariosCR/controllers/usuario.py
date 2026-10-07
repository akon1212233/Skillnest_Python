from connection.mysqlconnection import connectToMySQL

class Usuario:
    def __init__(self, data):
        self.id = data["id"]
        self.nombre = data["nombre"]
        self.apellido = data["apellido"]
        self.email = data["email"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def get_all(cls):
        """Recupera todos los usuarios ordenados por ID."""
        query = """
            SELECT id, nombre, apellido, email, created_at, updated_at
            FROM usuarios
            ORDER BY id ASC;
        """
        resultados = connectToMySQL("esquema_usuarios").query_db(query)
        usuarios = []
        if resultados:
            for usuario in resultados:
                usuarios.append(cls(usuario))
        return usuarios

    @classmethod
    def save(cls, data):
        """Inserta de manera segura un nuevo usuario usando sentencias preparadas."""
        query = """
            INSERT INTO usuarios (nombre, apellido, email, created_at, updated_at)
            VALUES (%(nombre)s, %(apellido)s, %(email)s, NOW(), NOW());
        """
        return connectToMySQL("esquema_usuarios").query_db(query, data)

    @classmethod
    def email_existe(cls, email):
        """Desafío adicional: Verifica si un email ya está registrado para evitar colisiones."""
        query = "SELECT id FROM usuarios WHERE email = %(email)s;"
        data = {"email": email}
        resultado = connectToMySQL("esquema_usuarios").query_db(query, data)
        return len(resultado) > 0 if resultado else False
