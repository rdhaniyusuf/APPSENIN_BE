from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user_model import UserModel, UserRoleModel, UserPositionDepartmentModel
from schemas.user_schema import UserCreateSchema, UsersSchema
from core.auth import AuthService, AuthJWT
import sys

sys.dont_write_bytecode = True

async def get_user_service(db: AsyncSession):
    try:
        result = await db.execute(select(UserModel).order_by(UserModel.user_id))
        users = result.scalars().all()
        user_list = []
        for user in users:
            user_data = {
                "user_id": user.user_id,
                "user_name": user.user_name,
                "user_email": user.user_email,
                "user_fullname": user.user_fullname,
                "user_number": user.user_number,
                "created_by": user.created_by,
                "created_at": user.created_at.isoformat(),
                "modified_by": user.modified_by,
                "modified_at": user.modified_at.isoformat(),
                "is_active": user.is_active,
            }
            user_list.append(user_data)
        return user_list
    except Exception as e:
        return {"error": str(e), "success": False}

async def create_user_service(db: AsyncSession, user: UserCreateSchema):
    db_user = UserModel(name=user.user_name, email=user.user_email, user_fullname=user.user_fullname, user_number=user.user_number, created_by=user.created_by, created_at=user.created_at, modified_by=user.modified_by, modified_at=user.modified_at, is_active=user.is_active)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def login_user_service(db: AsyncSession, user_name: str, user_pass: str):
    # Cari user berdasarkan user_name
    result = await db.execute(select(UserModel).filter(UserModel.user_name == user_name))
    user = result.scalar_one_or_none()
    
    if not user:
        return {"error": "User not found", "success": False}
    
    # Cari department user
    department_result = await db.execute(
        select(UserPositionDepartmentModel.department_id)
        .where(UserPositionDepartmentModel.user_id == user.user_id)
        .limit(1)
    )
    department = department_result.scalar_one_or_none()
    
    if not department:
        return {"error": "Department not found", "user_id": user.user_id, "success": False}

    # Cari role user
    role_result = await db.execute(
        select(UserRoleModel.role_id)
        .where(UserRoleModel.user_id == user.user_id)
        .where(UserRoleModel.is_active == True)
    )
    role = role_result.scalar_one_or_none()

    if not role:
        return {"error": "Role not found", "success": False}
        
    if not user.is_active:
        return {"error": "User is not active", "success": False}
    
    if not AuthService.check_password(user_pass, user.user_pass):
        return {"error": "Invalid password", "success": False}
    
    # Data user untuk dikembalikan & dimasukkan ke JWT
    user_data = {
        "user_id": user.user_id,
        "role_id": role,  # role sudah integer
        "department_id": department,  # department sudah integer
        "user_name": user.user_name,
        "user_email": user.user_email,
        "user_fullname": user.user_fullname,
        "user_number": user.user_number,
        "created_by": user.created_by,
        "created_at": user.created_at.isoformat(),
        "modified_by": user.modified_by,
        "modified_at": user.modified_at.isoformat(),
        "is_active": user.is_active, 
    }

    # Generate JWT token
    token = AuthJWT.generate_jwt(user_data)

    return {"success": True, "token": token, "user": user_data}

