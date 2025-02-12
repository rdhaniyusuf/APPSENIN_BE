import bcrypt
import jwt
from jose import jwt, JWTError
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
import datetime
import os
from typing import Any, Union

SECRET_KEY = ("4PPS3N1N#2025", "default_secret_key")
ACCESS_TOKEN_EXPIRE_HOURS = 1
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class AuthService:
    @staticmethod
    async def hash_password(password: str) -> str:
        return await bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=15, prefix=b"2b")).decode('utf-8')

    @staticmethod
    def check_password(pass_in: str, pass_out: str) -> bool:
        bcrypt.gensalt(rounds=15, prefix=b"2b")
        return bcrypt.checkpw(pass_in.encode('utf-8'), pass_out.encode('utf-8'))

    @staticmethod
    async def generate_jwt(user: Any) -> str:
        payload = {
            'user_id': str(user.user_id),
            'user_name': str(user.user_name),
            'exp': datetime.datetime.now() + datetime.timedelta(hours=1)
        }
        # secret_key = os.getenv('JWT_SECRET_KEY', 'default_secret_key')
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return await token
    
class AuthJWT:
    @staticmethod
    def generate_jwt(user: Any) -> str:
        """Membuat JWT token untuk pengguna"""
        payload = {
            "user_id": user["user_id"],
            "user_name": user["user_name"],
            "user_role": user["role_id"],
            "user_department": user["department_id"],
            "user_email": user["user_email"],
            "user_fullname": user["user_fullname"],
            "user_number": user["user_number"],
            "created_by": user["created_by"],
            "exp": datetime.datetime.now() + datetime.timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS),
        }
        token = jwt.encode(payload, SECRET_KEY[1], algorithm=ALGORITHM)
        return token

    @staticmethod
    def verify_jwt(token: str) -> Union[dict, None]:
        """Memverifikasi dan mendekode JWT token"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

    @staticmethod
    async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
        """Mengambil user dari token JWT"""
        return AuthJWT.verify_jwt(token)