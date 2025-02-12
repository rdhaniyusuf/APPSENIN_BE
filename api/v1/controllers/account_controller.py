import sys
sys.dont_write_bytecode = True
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from core.database import get_db
from schemas.user_schema import UserCreateSchema, UserSchema,UserLoginSchema,UsersSchema
from services.user_service import create_user_service, get_user_service, login_user_service
from core.auth import AuthJWT

router = APIRouter()
@router.get("/", response_model=List[UsersSchema])
async def list_users(db: AsyncSession = Depends(get_db)):
    users = await get_user_service(db)
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users

# Endpoint untuk menambahkan user baru
@router.post("/register", response_model=UserSchema)
async def register_user_controller(user: UserCreateSchema, db: AsyncSession = Depends(get_db)):
    return await create_user_service(db, user)

# Endpoint untuk login user
# @router.post("/login")
# async def login_user_controller(user: UserLoginSchema, db: AsyncSession = Depends(get_db)):
#     user_data = await login_user_service(db, user.user_name, user.user_pass)

#     if "error" in user_data:
#         raise HTTPException(status_code=401, detail=user_data["error"])
#     return {"message": "Login successful", "user": user_data, "valid": True}

@router.post("/login")
async def login_user_controller(user: UserLoginSchema, db: AsyncSession = Depends(get_db)):
    response = await login_user_service(db, user.user_name, user.user_pass)

    if not response.get("success"):
        raise HTTPException(status_code=401, detail=response["error"])

    return {
        "message": "Login successful",
        "token": response["token"],
        "user": response["user"]
    }

# Endpoint untuk mendapatkan profile
@router.get("/profile")
async def get_profile(user: dict = Depends(AuthJWT.get_current_user)):
    return {"message": "Success", "user": user}

# endpoitn untuk mendapatkan role
@router.get("/role")
async def get_role():
    return {"message": "Role User", "role": "Admin"}
