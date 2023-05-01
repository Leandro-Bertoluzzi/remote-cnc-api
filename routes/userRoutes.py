from flask import Blueprint, jsonify, request
from database.repositories.userRepository import getAllUsers, createUser, updateUser, removeUser
from utilities.utils import serializeList
from database.models.user import VALID_ROLES
from jsonschema import validate

userBlueprint = Blueprint('userBlueprint', __name__)

USER_SCHEMA = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'email': {'type': 'string'},
        'password': {'type': 'string'},
        'role': {'type': 'string', 'enum': VALID_ROLES},
    },
    'required': ['name', 'email', 'password', 'role'],
}

@userBlueprint.route('/', methods=['GET'])
@userBlueprint.route('/all', methods=['GET'])
def getUsers():
    users = serializeList(getAllUsers())
    return jsonify(users)

@userBlueprint.route('/', methods=['POST'])
def createNewUser():
    try:
        validate(instance=request.json, schema=USER_SCHEMA)
    except Exception as error:
        return {'Error': error.message}, 400

    userName = request.json['name']
    userEmail = request.json['email']
    userPassword = request.json['password']
    userRole = request.json['role']

    try:
        createUser(userName, userEmail, userPassword, userRole)
    except Exception as error:
        return {'Error': str(error)}, 400

    return {'success': 'The user was successfully created'}, 200

@userBlueprint.route('/<int:user_id>', methods=['PUT'])
def updateExistingUser(user_id):
    try:
        validate(instance=request.json, schema=USER_SCHEMA)
    except Exception as error:
        return {'Error': error.message}, 400

    userName = request.json['name']
    userEmail = request.json['email']
    userPassword = request.json['password']
    userRole = request.json['role']

    try:
        updateUser(user_id, userName, userEmail, userPassword, userRole)
    except Exception as error:
        return {'Error': str(error)}, 400

    return {'success': 'The user was successfully updated'}, 200

@userBlueprint.route('/<int:user_id>', methods=['DELETE'])
def removeExistingUser(user_id):
    try:
        removeUser(user_id)
    except Exception as error:
        return {'Error': str(error)}, 400

    return {'success': 'The user was successfully removed'}, 200