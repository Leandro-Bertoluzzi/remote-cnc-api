from flask import Blueprint, jsonify, request
from jsonschema import validate
import jwt

from authMiddleware import token_required, only_admin
from config import TOKEN_SECRET
from database.models.user import VALID_ROLES
from database.repositories.userRepository import getAllUsers, createUser, updateUser, removeUser, loginUser
from utilities.utils import serializeList
from utilities.validators import validateEmailAndPassword

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

LOGIN_SCHEMA = {
    'type': 'object',
    'properties': {
        'email': {'type': 'string'},
        'password': {'type': 'string'},
    },
    'required': ['email', 'password'],
}

@userBlueprint.route('/', methods=['GET'])
@userBlueprint.route('/all', methods=['GET'])
@token_required
@only_admin
def getUsers(admin):
    users = serializeList(getAllUsers())
    return jsonify(users)

@userBlueprint.route('/', methods=['POST'])
@token_required
@only_admin
def createNewUser(admin):
    try:
        validate(instance=request.json, schema=USER_SCHEMA)
    except Exception as error:
        return {
            'message': error.message,
            'data': None,
            'error': 'Invalid data'
        }, 400

    name = request.json['name']
    email = request.json['email']
    password = request.json['password']
    role = request.json['role']

    validationErrors = validateEmailAndPassword(email, password)
    if validationErrors:
        return {
            'message': 'Invalid data',
            'data': None,
            'error': validationErrors
        }, 400

    try:
        createUser(name, email, password, role)
    except Exception as error:
        return {'error': str(error)}, 400

    return {'success': 'The user was successfully created'}, 200

@userBlueprint.route('/<int:user_id>', methods=['PUT'])
@token_required
@only_admin
def updateExistingUser(admin, user_id):
    try:
        validate(instance=request.json, schema=USER_SCHEMA)
    except Exception as error:
        return {'error': error.message}, 400

    name = request.json['name']
    email = request.json['email']
    password = request.json['password']
    role = request.json['role']

    try:
        updateUser(user_id, name, email, password, role)
    except Exception as error:
        return {'error': str(error)}, 400

    return {'success': 'The user was successfully updated'}, 200

@userBlueprint.route('/<int:user_id>', methods=['DELETE'])
@token_required
@only_admin
def removeExistingUser(admin, user_id):
    try:
        removeUser(user_id)
    except Exception as error:
        return {'error': str(error)}, 400

    return {'success': 'The user was successfully removed'}, 200

@userBlueprint.route('/login', methods=['POST'])
def login():
    try:
        validate(instance=request.json, schema=LOGIN_SCHEMA)
    except Exception as error:
        return {'error': error.message}, 400

    email = request.json.get('email')
    password = request.json.get('password')

    # Get user from DB
    try:
        user, message = loginUser(email, password)
    except Exception as error:
        return {
            'message': str(error),
            'data': None,
            'error': 'Something went wrong'
        }, 500

    if not user:
        return {
            'message': message,
            'data': None,
            'error': 'Unauthorized'
        }, 404

    try:
        userData = user.serialize()
        # token should expire after 24 hrs
        userData['token'] = jwt.encode(
            {'user_id': user.id},
            TOKEN_SECRET,
            algorithm='HS256'
        )
        return {
            'message': 'Successfully fetched auth token',
            'data': userData
        }, 200
    except Exception as e:
        return {
            'error': 'Something went wrong',
            'message': str(e)
        }, 500
