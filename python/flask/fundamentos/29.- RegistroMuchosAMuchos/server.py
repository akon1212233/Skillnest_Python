from flask_app import app

# Importamos el controlador para registrar las rutas.
from flask_app.controllers import inscripciones


if __name__ == "__main__":
    app.run(debug=True)