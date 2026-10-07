# ==========================================================
# PUNTO DE ENTRADA DE LA APLICACIÓN
# ==========================================================


from __init__ import app


# ==========================================================
# IMPORTAR CONTROLADORES
# ==========================================================
#
# Aunque no utilizamos directamente la variable "tacos",
# esta importación ejecuta el módulo y registra sus rutas
# utilizando la instancia "app".
# ==========================================================

from controllers.taco import tacos


# ==========================================================
# EJECUTAR SERVIDOR
# ==========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )