from flask_app import app

# Importamos el controlador para registrar todas las rutas.
from flask_app.controllers import canciones


if __name__ == "__main__":
    app.run(debug=True)