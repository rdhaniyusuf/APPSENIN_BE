from pydantic import BaseModel, EmailStr
from typing import Optional
import sys
sys.dont_write_bytecode = True

class UserSchema(BaseModel):
    user_id: Optional[int]
    user_name: str
    user_pass: str
    user_fullname: str
    user_email: EmailStr
    user_number:str
    created_by:int
    created_at:str
    modified_by:int
    modified_at:str
    is_active:bool
    
class UsersSchema(BaseModel):
    user_id: Optional[int]
    user_name: str
    user_fullname: str
    user_email: EmailStr
    user_number:str
    created_by:int
    created_at:str
    modified_by:int
    modified_at:str
    is_active:bool

class UserCreateSchema(BaseModel):
    user_id: Optional[int]
    user_name: str
    user_pass: str
    user_fullname: str
    user_email: EmailStr
    user_number:str
    created_by:int
    created_at:str
    modified_by:int
    modified_at:str
    is_active:bool
    

class UserLoginSchema(BaseModel):
    user_name: str
    user_pass: str 
    
class UserResponse(BaseModel):
    user_id: int
    items: UserSchema

    class Config:
        from_attributes = True