import bcrypt
from flask import Blueprint, jsonify, request
from jsonschema import validate
import jwt
from authMiddleware import token_required, only_admin
from config import TOKEN_SECRET
from core.database.models import VALID_ROLES, RoleType
from core.database.repositories.userRepository import UserRepository
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
    repository = UserRepository()
    users = serializeList(repository.get_all_users())
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
        repository = UserRepository()
        repository.create_user(name, email, password, role)
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
        repository = UserRepository()
        repository.update_user(user_id, name, email, password, role)
    except Exception as error:
        return {'error': str(error)}, 400

    return {'success': 'The user was successfully updated'}, 200

@userBlueprint.route('/<int:user_id>', methods=['DELETE'])
@token_required
@only_admin
def removeExistingUser(admin, user_id):
    try:
        repository = UserRepository()
        repository.remove_user(user_id)
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
        repository = UserRepository()
        user = repository.get_user_by_email(email)
        checks = bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))
    except Exception as error:
        return {
            'message': str(error),
            'data': None,
            'error': 'Something went wrong'
        }, 500

    if not user:
        return {
            'message': 'Invalid email',
            'data': None,
            'error': 'Unauthorized'
        }, 404

    if not checks:
        return {
            'message': 'Invalid combination of email and password',
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
            'error': 'Error with credentials',
            'message': str(e)
        }, 500

@userBlueprint.route('/auth', methods=['GET'])
@token_required
def authenticate(user):
    return {
        'message': 'Successfully authenticated',
        'data': user.serialize()
    }, 200

###################################################################################

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, Field
from authMiddleware import GetAdminDep, GetUserDep

userRoutes = APIRouter()

class UserCreateModel(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(
        regex=r'\b^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$\b',
        description='Password must be 8-20 characters long with upper and lower case \
            letters, numbers and special characters (@$!%*#?&)'
        )
    role: RoleType

class UserUpdateModel(BaseModel):
    name: str
    email: EmailStr
    role: RoleType

class UserLoginModel(BaseModel):
    email: EmailStr
    password: str

# Routes

@userRoutes.get('/users/')
@userRoutes.get('/users/all')
def get_users(admin: GetAdminDep):
    repository = UserRepository()
    users = serializeList(repository.get_all_users())
    return users

@userRoutes.post('/users/')
def create_user(request: UserCreateModel, admin: GetAdminDep):
    name = request.name
    email = request.email
    password = request.password
    role = request.role

    try:
        repository = UserRepository()
        repository.create_user(name, email, password, role)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

    return {'success': 'The user was successfully created'}

@userRoutes.put('/users/{user_id}')
def update_user(
    user_id: int,
    request: UserUpdateModel,
    admin: GetAdminDep
):
    name = request.name
    email = request.email
    role = request.role

    try:
        repository = UserRepository()
        repository.update_user(user_id, name, email, role)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

    return {'success': 'The user was successfully updated'}

@userRoutes.delete('/users/{user_id}')
def remove_user(user_id: int, admin: GetAdminDep):
    try:
        repository = UserRepository()
        repository.remove_user(user_id)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

    return {'success': 'The user was successfully removed'}

@userRoutes.post('/users/login')
def login(request: UserLoginModel):
    email = request.email
    password = request.password

    # Get user from DB
    try:
        repository = UserRepository()
        user = repository.get_user_by_email(email)
        checks = bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))
    except Exception as error:
        raise HTTPException(400, detail=str(error))

    if not user:
        raise HTTPException(404, detail='Unauthorized: Invalid email')

    if not checks:
        raise HTTPException(404, detail='Unauthorized: Invalid combination of email and password')

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
        }
    except Exception as error:
        raise HTTPException(400, detail=str(error))

@userRoutes.get('/users/auth')
def authenticate(user: GetUserDep):
    return {
        'message': 'Successfully authenticated',
        'data': user.serialize()
    }
