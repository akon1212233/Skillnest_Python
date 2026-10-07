from flask import Flask

app = Flask(__name__)

# Necesaria para utilizar mensajes flash.
app.secret_key = "clave-secreta-desarrollo"