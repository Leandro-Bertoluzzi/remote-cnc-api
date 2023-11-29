from config import TOKEN_SECRET
import jwt
from typing import Dict


# JSON Web Token

def generate_token(user_id: int) -> str:
    return jwt.encode(
        {'user_id': user_id},
        TOKEN_SECRET,
        algorithm='HS256'
    )


def verify_token(token: str) -> Dict[str, int]:
    return jwt.decode(token, TOKEN_SECRET, algorithms=['HS256'])
