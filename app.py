from flask import Flask
from routes.userRoutes import userBlueprint

app = Flask(__name__)
app.register_blueprint(userBlueprint, url_prefix='/user')

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"