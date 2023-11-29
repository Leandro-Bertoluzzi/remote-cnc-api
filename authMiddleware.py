from core.database.models import User
from core.database.repositories.userRepository import UserRepository
from fastapi import Depends, HTTPException, Request
from jwt import ExpiredSignatureError, InvalidSignatureError
from services.security import verify_token
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
        data = verify_token(token)
        user = repository.get_user_by_id(data['user_id'])
        if user is None:
            raise HTTPException(
                401,
                detail='Unauthorized: Invalid Authentication token!'
            )
    except ExpiredSignatureError:
        raise HTTPException(
            401,
            detail='Expired token, please login to generate a new one'
        )
    except InvalidSignatureError:
        raise HTTPException(
            401,
            detail='Invalid token, please login to generate a new one'
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
