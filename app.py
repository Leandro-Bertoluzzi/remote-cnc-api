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
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.wsgi import WSGIMiddleware
from routes.cncRoutes import cncRoutes
from routes.fileRoutes import fileRoutes
from routes.materialRoutes import materialRoutes
from routes.toolRoutes import toolRoutes
from routes.taskRoutes import taskRoutes
from routes.userRoutes import userRoutes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/v2")
def read_main():
	return {"message": "Hello World from FastAPI"}

app.mount("/v1", WSGIMiddleware(flask_app))

# Routes
app.include_router(cncRoutes)
app.include_router(fileRoutes)
app.include_router(materialRoutes)
app.include_router(toolRoutes)
app.include_router(taskRoutes)
app.include_router(userRoutes)
