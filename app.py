from flask import Flask
from flask_cors import CORS
from routes.userRoutes import userBlueprint
from routes.fileRoutes import fileBlueprint
from routes.taskRoutes import taskBlueprint
from routes.toolRoutes import toolBlueprint
from routes.materialRoutes import materialBlueprint
from routes.cncRoutes import cncBlueprint

# Configurate app
app = Flask(__name__)
CORS(app)

# Routes
app.register_blueprint(userBlueprint, url_prefix='/users')
app.register_blueprint(fileBlueprint, url_prefix='/files')
app.register_blueprint(taskBlueprint, url_prefix='/tasks')
app.register_blueprint(toolBlueprint, url_prefix='/tools')
app.register_blueprint(materialBlueprint, url_prefix='/materials')
app.register_blueprint(cncBlueprint, url_prefix='/cnc')

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
