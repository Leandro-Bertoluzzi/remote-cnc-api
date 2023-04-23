from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from routes.userRoutes import userBlueprint

app = Flask(__name__)
app.register_blueprint(userBlueprint, url_prefix='/user')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/cnc_db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"