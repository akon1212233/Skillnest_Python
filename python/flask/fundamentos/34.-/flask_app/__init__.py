from flask import Flask
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")

bcrypt = Bcrypt(app)

from flask_app.controllers import usuarios
