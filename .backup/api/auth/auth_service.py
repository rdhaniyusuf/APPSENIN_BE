import bcrypt
import jwt
import datetime
import os
from typing import Any

class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def check_password(hash: str, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hash.encode('utf-8'))
    
    @staticmethod
    def generate_jwt(user: Any) -> str:
        payload = {
            'user_id': user.id,
            'user_name': user.username,
            'exp': datetime.datetime.now() + datetime.timedelta(hours=1)  # Token expires in 1 hour
        }
        secret_key = os.getenv('JWT_SECRET_KEY', 'default_secret_key')
        token = jwt.encode(payload, secret_key, algorithm='HS256')
        return token