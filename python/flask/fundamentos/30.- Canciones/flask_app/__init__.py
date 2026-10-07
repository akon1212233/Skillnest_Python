from flask import Flask

app = Flask(__name__)

# Necesaria para utilizar mensajes flash.
# En un proyecto real la clave debe mantenerse fuera del código.
app.secret_key = "clave-secreta-desarrollo"