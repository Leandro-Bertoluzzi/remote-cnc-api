import jwt
from functools import wraps
from flask import request, abort
from config import TOKEN_SECRET
from core.database.repositories.userRepository import UserRepository

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]
        elif request.args.get('token'):
            token = request.args.get('token')

        if not token:
            return {
                'message': 'Authentication Token is missing!',
                'data': None,
                'error': 'Unauthorized'
            }, 401
        try:
            repository = UserRepository()
            data = jwt.decode(token, TOKEN_SECRET, algorithms=['HS256'])
            user = repository.get_user_by_id(data['user_id'])
            if user is None:
                return {
                'message': 'Invalid Authentication token!',
                'data': None,
                'error': 'Unauthorized'
            }, 401
        except jwt.ExpiredSignatureError as e:
            return {
                'message': 'Expired token, please login to generate a new one',
                'data': None,
                'error': str(e)
            }, 401
        except Exception as e:
            return {
                'message': 'Something went wrong',
                'data': None,
                'error': str(e)
            }, 500

        return f(user, *args, **kwargs)

    return decorated

def only_admin(f):
    @wraps(f)
    def decorated(user, *args, **kwargs):
        if not user:
            return {
                'message': 'Authentication error',
                'data': None,
                'error': 'Unauthorized'
            }, 401

        if user.role != 'admin':
            return {
            'message': 'This endpoint needs admin permission',
            'data': None,
            'error': 'Unauthorized'
        }, 400

        return f(admin=user, *args, **kwargs)

    return decorated

###################################################################################

from core.database.models import User
from fastapi import Depends, HTTPException, Request
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
