from authMiddleware import GetAdminDep, GetUserDep
import bcrypt
from config import TOKEN_SECRET
from core.database.models import RoleType
from core.database.repositories.userRepository import UserRepository
from fastapi import APIRouter, HTTPException
import jwt
from pydantic import BaseModel, EmailStr, Field
from utilities.utils import serializeList

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
