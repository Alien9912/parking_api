"""
В этом файле будет ваше Flask-приложение
"""
from flask import Flask
from routes import api
from config import UPLOAD_FOLDER, TEMP_FOLDER
import os

app = Flask(__name__)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TEMP_FOLDER, exist_ok=True)

app.register_blueprint(api)

if __name__ == '__main__':
    app.run(debug=True)