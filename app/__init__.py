from flask import Flask
from dotenv import load_dotenv
from app.routes import register_routes
import os

def create_app():
    load_dotenv()
    os.makedirs("./temp/collections", exist_ok=True)
    os.makedirs("./temp/environments", exist_ok=True)
    app = Flask(__name__)
    register_routes(app)
    return app

