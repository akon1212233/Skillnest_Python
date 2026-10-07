from academia import app

# Importamos los controladores para registrar las rutas.
from academia.controllers import talleres
from academia.controllers import alumnos


if __name__ == "__main__":
    app.run(debug=True)
