from flask import Flask
from flask_cors import CORS
from routes.userRoutes import userBlueprint
from routes.fileRoutes import fileBlueprint
from routes.taskRoutes import taskBlueprint
from routes.toolRoutes import toolBlueprint
from routes.materialRoutes import materialBlueprint
from routes.cncRoutes import cncBlueprint

# Configurate Flask app
flask_app = Flask(__name__)
CORS(flask_app)

# Routes
flask_app.register_blueprint(userBlueprint, url_prefix='/users')
flask_app.register_blueprint(fileBlueprint, url_prefix='/files')
flask_app.register_blueprint(taskBlueprint, url_prefix='/tasks')
flask_app.register_blueprint(toolBlueprint, url_prefix='/tools')
flask_app.register_blueprint(materialBlueprint, url_prefix='/materials')
flask_app.register_blueprint(cncBlueprint, url_prefix='/cnc')

@flask_app.route("/")
def hello_world():
    return {"message": "Hello World from Flask"}

from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from markupsafe import escape

app = FastAPI()

@app.get("/v2")
def read_main():
	return {"message": "Hello World from FastAPI"}

app.mount("/v1", WSGIMiddleware(flask_app))
