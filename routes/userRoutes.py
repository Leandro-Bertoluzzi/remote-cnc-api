from flask import Blueprint, abort, jsonify

userBlueprint = Blueprint('userBlueprint', __name__)

# Assume this function returns a list of users from the database
def getUsersFromDb():
    return [{'name': 'Alice'}, {'name': 'Bob'}, {'name': 'Charlie'}]

@userBlueprint.route('/', methods=['GET'])
@userBlueprint.route('/all', methods=['GET'])
def getUsers():
    users = getUsersFromDb()
    return jsonify(users)