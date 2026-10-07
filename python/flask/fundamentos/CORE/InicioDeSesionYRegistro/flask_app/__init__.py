from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

# Necesaria para utilizar mensajes flash.
app.secret_key = "clave-secreta-desarrollo"