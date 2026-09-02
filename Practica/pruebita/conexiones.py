import mysql.connector

class Conexion:
    @staticmethod
    def conexion():    
        conexion = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "1234",
            database = "usuarios_db",
        )
        return conexion

conexion = Conexion.conexion()
cursor = conexion.cursor()