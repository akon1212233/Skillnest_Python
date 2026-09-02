from conexiones import cursor, conexion
from tipoUsuarios import tipoUsuario

class Usuario():
    def __init__(self, idTipoUsuario="Usuario", nickname=None, password=None, email=None):
        self.idTipoUsuario = idTipoUsuario
        self.nickname = nickname
        self.password = password
        self.email = email

    def buscarUsuario(self, email, password):
        self.email = email
        self.password = password
        cursor.execute(
            "SELECT idUsuario, nombreUsuario, idTipoUsuario FROM usuario WHERE emailUsuario = %s AND contrasenaUsuario = %s AND deleted = 0", 
            (self.email, self.password)
        )
        return cursor.fetchone()

    def verificarEmail(self, email, password):
        result = self.buscarUsuario(email, password)
        if result:
            return True
        else:
            return False

    def administrador(self, idUsuario):
        self.tipo_usuario = tipoUsuario(self.idTipoUsuario, None)

    def registrarUsuario(self, idTipoUsuario, nickname, password, email):
        cursor.execute("SELECT IFNULL(MAX(idUsuario), 0) + 1 FROM usuario")
        nuevo_id = cursor.fetchone()[0]
        
        cursor.execute(
            "INSERT INTO usuario (idUsuario, idTipoUsuario, nombreUsuario, contrasenaUsuario, emailUsuario) VALUES (%s, %s, %s, %s, %s)", 
            (nuevo_id, idTipoUsuario, nickname, password, email)
        )
        conexion.commit()

    def modificarUsuario(self, idUsuario, nickname, password, email, idTipoUsuario):
        cursor.execute(
            "UPDATE usuario SET nombreUsuario = %s, contrasenaUsuario = %s, emailUsuario = %s, idTipoUsuario = %s WHERE idUsuario = %s", 
            (nickname, password, email, idTipoUsuario, idUsuario)
        )
        conexion.commit()

    def eliminarUsuario(self, idUsuario):
        cursor.execute("UPDATE usuario SET deleted = 1 WHERE idUsuario = %s", (idUsuario,))
        conexion.commit()

    def listarUsuarios(self):
        cursor.execute("SELECT idUsuario, nombreUsuario, idTipoUsuario FROM usuario WHERE deleted = 0")
        return cursor.fetchall()

    def listarUsuariosEliminados(self):
        cursor.execute("SELECT idUsuario, nombreUsuario, idTipoUsuario FROM usuario WHERE deleted = 1")
        return cursor.fetchall()

    def validarUsuario(self, idUsuario):
        if self.buscarUsuario(self.email, self.password):
            return True
        else:
            return False
