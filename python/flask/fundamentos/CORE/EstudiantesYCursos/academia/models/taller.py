from academia.config.conexion import connectToMySQL
from academia.models.alumno import Alumno

BD = "academia_talleres"


class Taller:
    """Representa un registro de la tabla talleres."""

    def __init__(self, datos):
        self.id = datos["id"]
        self.titulo = datos["titulo"]
        self.created_at = datos["created_at"]
        self.updated_at = datos["updated_at"]
        self.alumnos = []

    @classmethod
    def obtener_todos(cls):
        """Obtiene todos los talleres ordenados por título."""
        consulta = """
            SELECT id, titulo, created_at, updated_at
            FROM talleres
            ORDER BY titulo;
        """
        resultados = connectToMySQL(BD).query_db(consulta) or []
        return [cls(fila) for fila in resultados]

    @classmethod
    def guardar(cls, datos):
        """Crea un nuevo taller."""
        consulta = """
            INSERT INTO talleres (titulo)
            VALUES (%(titulo)s);
        """
        return connectToMySQL(BD).query_db(consulta, datos)

    @classmethod
    def obtener_con_alumnos(cls, taller_id):
        """
        Obtiene un taller junto con sus alumnos.
        LEFT JOIN conserva el taller aunque no tenga alumnos todavía.
        """
        consulta = """
            SELECT
                t.id         AS taller_id,
                t.titulo     AS taller_titulo,
                t.created_at AS taller_created_at,
                t.updated_at AS taller_updated_at,

                a.id         AS alumno_id,
                a.nombre     AS alumno_nombre,
                a.apellido   AS alumno_apellido,
                a.edad       AS alumno_edad,
                a.created_at AS alumno_created_at,
                a.updated_at AS alumno_updated_at

            FROM talleres t
            LEFT JOIN alumnos a
                ON t.id = a.taller_id
            WHERE t.id = %(id)s;
        """
        resultados = connectToMySQL(BD).query_db(consulta, {"id": taller_id})

        if not resultados:
            return None

        taller = cls({
            "id": resultados[0]["taller_id"],
            "titulo": resultados[0]["taller_titulo"],
            "created_at": resultados[0]["taller_created_at"],
            "updated_at": resultados[0]["taller_updated_at"],
        })

        for fila in resultados:
            if fila["alumno_id"] is not None:
                taller.alumnos.append(Alumno({
                    "id": fila["alumno_id"],
                    "nombre": fila["alumno_nombre"],
                    "apellido": fila["alumno_apellido"],
                    "edad": fila["alumno_edad"],
                    "created_at": fila["alumno_created_at"],
                    "updated_at": fila["alumno_updated_at"],
                    "taller_id": taller.id,
                }))

        return taller
