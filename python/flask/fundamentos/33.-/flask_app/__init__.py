from flask import Flask

app = Flask(__name__)

# Necesaria para utilizar flash() y session.
app.secret_key = "clave-secreta-desarrollo"
