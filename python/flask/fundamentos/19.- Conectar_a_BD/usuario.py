from mysqlconnection import connectToMySQL
class Usuario:
    def __init__(self, data):
        self.id = data["id"]
        self.nombre = data["nombre"]
        self.email = data["email"]
        self.edad = data["edad"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM usuarios;"
        resultados = connectToMySQL(
            "primera_flask"
        ).query_db(query)
        usuarios = []
        for usuario in resultados:
            usuarios.append(
                cls(usuario)
            )
        return usuarios