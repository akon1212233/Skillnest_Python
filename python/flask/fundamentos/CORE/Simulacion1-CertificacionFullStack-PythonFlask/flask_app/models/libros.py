from flask_app.config.mysqlconnection import MySQLConnection


class Libro:
    @staticmethod
    def crear(data):
        query = """
            INSERT INTO libros (titulo, autor, genero, fecha_publicacion, descripcion, usuario_id)
            VALUES (%(titulo)s, %(autor)s, %(genero)s, %(fecha_publicacion)s, %(descripcion)s, %(usuario_id)s)
        """
        return MySQLConnection.query_db(query, data)

    @staticmethod
    def todos():
        query = """
            SELECT l.*, CONCAT(u.nombre, ' ', u.apellido) AS publicado_por,
            (SELECT COUNT(*) FROM favoritos f WHERE f.libro_id = l.id) AS favoritos
            FROM libros l
            JOIN usuarios u ON u.id = l.usuario_id
            ORDER BY l.created_at DESC
        """
        return MySQLConnection.query_db(query, fetchall=True)

    @staticmethod
    def de_usuario(usuario_id):
        query = """
            SELECT l.*,
            (SELECT COUNT(*) FROM favoritos f WHERE f.libro_id = l.id) AS favoritos
            FROM libros l
            WHERE l.usuario_id = %(usuario_id)s
            ORDER BY l.created_at DESC
        """
        return MySQLConnection.query_db(query, {"usuario_id": usuario_id}, fetchall=True)

    @staticmethod
    def por_id(libro_id):
        query = """
            SELECT l.*, CONCAT(u.nombre, ' ', u.apellido) AS publicado_por
            FROM libros l
            JOIN usuarios u ON u.id = l.usuario_id
            WHERE l.id = %(id)s
            LIMIT 1
        """
        return MySQLConnection.query_db(query, {"id": libro_id}, fetchone=True)

    @staticmethod
    def actualizar(libro_id, usuario_id, data):
        query = """
            UPDATE libros
            SET titulo=%(titulo)s, autor=%(autor)s, genero=%(genero)s,
            fecha_publicacion=%(fecha_publicacion)s, descripcion=%(descripcion)s
            WHERE id=%(id)s AND usuario_id=%(usuario_id)s
        """
        payload = {**data, "id": libro_id, "usuario_id": usuario_id}
        MySQLConnection.query_db(query, payload)

    @staticmethod
    def eliminar(libro_id, usuario_id):
        query = "DELETE FROM libros WHERE id=%(id)s AND usuario_id=%(usuario_id)s"
        MySQLConnection.query_db(query, {"id": libro_id, "usuario_id": usuario_id})

    @staticmethod
    def favoritos_de_libro(libro_id):
        query = """
            SELECT u.id, CONCAT(u.nombre, ' ', u.apellido) AS nombre
            FROM favoritos f
            JOIN usuarios u ON u.id = f.usuario_id
            WHERE f.libro_id = %(libro_id)s
            ORDER BY u.nombre, u.apellido
        """
        return MySQLConnection.query_db(query, {"libro_id": libro_id}, fetchall=True)

    @staticmethod
    def favoritos_de_usuario(usuario_id):
        query = """
            SELECT l.*, CONCAT(u.nombre, ' ', u.apellido) AS publicado_por
            FROM favoritos f
            JOIN libros l ON l.id = f.libro_id
            JOIN usuarios u ON u.id = l.usuario_id
            WHERE f.usuario_id = %(usuario_id)s
            ORDER BY f.created_at DESC
        """
        return MySQLConnection.query_db(query, {"usuario_id": usuario_id}, fetchall=True)

    @staticmethod
    def tiene_favorito(usuario_id, libro_id):
        return MySQLConnection.query_db(
            "SELECT id FROM favoritos WHERE usuario_id=%(usuario_id)s AND libro_id=%(libro_id)s",
            {"usuario_id": usuario_id, "libro_id": libro_id},
            fetchone=True,
        )

    @staticmethod
    def agregar_favorito(usuario_id, libro_id):
        query = "INSERT IGNORE INTO favoritos (usuario_id, libro_id) VALUES (%(usuario_id)s, %(libro_id)s)"
        MySQLConnection.query_db(query, {"usuario_id": usuario_id, "libro_id": libro_id})

    @staticmethod
    def quitar_favorito(usuario_id, libro_id):
        query = "DELETE FROM favoritos WHERE usuario_id=%(usuario_id)s AND libro_id=%(libro_id)s"
        MySQLConnection.query_db(query, {"usuario_id": usuario_id, "libro_id": libro_id})
