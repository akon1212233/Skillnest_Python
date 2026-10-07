from flask import Flask

app = Flask(__name__)

# Necesaria para que Flask pueda utilizar flash().
app.secret_key = "clave-secreta-desarrollo"
