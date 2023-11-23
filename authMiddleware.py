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
