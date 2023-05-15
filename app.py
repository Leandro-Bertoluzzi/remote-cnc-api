from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from routes.userRoutes import userBlueprint
from routes.fileRoutes import fileBlueprint
from routes.toolRoutes import toolBlueprint
from routes.materialRoutes import materialBlueprint
from config import Config
from database.base import db

# Configurate app
app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Initialize Flask extensions here
db.init_app(app)

# Routes
app.register_blueprint(userBlueprint, url_prefix='/users')
app.register_blueprint(fileBlueprint, url_prefix='/files')
app.register_blueprint(toolBlueprint, url_prefix='/tools')
app.register_blueprint(materialBlueprint, url_prefix='/materials')

# Migrations controller
migrate = Migrate(app, db, compare_type=False)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
