from conexiones import cursor,conexion
class tipoUsuario():
    def __init__(self, idTipoUsuario, nombreTipoUsuario):
        self.idTipoUsuario = idTipoUsuario
        self.nombreTipoUsuario = nombreTipoUsuario
    def administrador(self, idTipoUsuario):
        cursor.execute("SELECT * FROM tipoUsuario WHERE idTipoUsuario = %s", (idTipoUsuario,))
        result = cursor.fetchone()
        conexion.commit()
        cursor.close()
        conexion.close()
        if result:
            return True
        else:
            return False
        