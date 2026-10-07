# ==========================================================
# PUNTO DE ENTRADA
# ==========================================================

from flask_app import app


# ==========================================================
# IMPORTAR CONTROLADOR
# ==========================================================
#
# Esta importación carga las rutas definidas en:
#
# flask_app/controllers/tacos.py
#
# y permite que Flask las registre.
# ==========================================================

from flask_app.controllers import tacos


# ==========================================================
# EJECUTAR APLICACIÓN
# ==========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )