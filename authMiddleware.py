from config import TOKEN_SECRET
from core.database.models import User
from core.database.repositories.userRepository import UserRepository
from fastapi import Depends, HTTPException, Request
import jwt
from typing import Annotated

def auth_user(request: Request) -> User:
    token = None

    if 'Authorization' in request.headers:
        token = request.headers['Authorization'].split(' ')[1]
    elif request.query_params.get('token'):
        token = request.query_params.get('token')

    if not token:
        raise HTTPException(
            401,
            detail='Unauthorized: Authentication Token is missing!'
        )
    try:
        repository = UserRepository()
        data = jwt.decode(token, TOKEN_SECRET, algorithms=['HS256'])
        user = repository.get_user_by_id(data['user_id'])
        if user is None:
            raise HTTPException(
                401,
                detail='Unauthorized: Invalid Authentication token!'
            )
    except jwt.ExpiredSignatureError as e:
        raise HTTPException(
            401,
            detail='Expired token, please login to generate a new one'
        )
    except Exception as error:
        raise HTTPException(
            400,
            detail=str(error)
        )

    return user

def auth_admin(request: Request) -> User:
    user = auth_user(request)

    if not user:
        raise HTTPException(
            401,
            detail='Unauthorized: Authentication error'
        )

    if user.role != 'admin':
        raise HTTPException(
            401,
            detail='Unauthorized: This endpoint requires admin permission'
        )

    return user

# Type definitions

GetUserDep = Annotated[User, Depends(auth_user)]
GetAdminDep = Annotated[User, Depends(auth_admin)]
