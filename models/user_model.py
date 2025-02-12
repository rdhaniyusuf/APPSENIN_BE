from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, LargeBinary,VARCHAR, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from typing import List
from sqlalchemy.sql import func
from core.database import Base
import datetime
import sys

sys.dont_write_bytecode = True

class UserModel(Base):
    __tablename__ = "at_sys_msuser"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String, nullable=False, unique=True)
    user_fullname = Column(String, nullable=False)
    user_pass = Column(String, nullable=False)
    user_email = Column(String, nullable=False, unique=True)
    user_number = Column(String, nullable=False, unique=True)
    user_image = Column(LargeBinary, nullable=True)
    created_by = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    modified_by = Column(Integer, nullable=False)
    modified_at = Column(TIMESTAMP, server_default=func.now())
    is_active = Column(Boolean, default=True)
    


class RoleModel(Base):
    __tablename__ = "at_sys_msrole"
    role_id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String, nullable=False)
    role_desc = Column(String, nullable=False)
    created_by = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    modified_by = Column(Integer, nullable=False)
    modified_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True)

class UserRoleModel(Base):
    __tablename__ = "at_sys_msuserrole"
    user_role_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("at_sys_msuser.user_id"), nullable=False)
    role_id = Column(Integer, ForeignKey("at_sys_msrole.role_id"), nullable=False)
    created_by = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    modified_by = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
    
class PositionModel(Base):
    __tablename__ = "at_sys_msposition"
    position_id = Column(Integer, primary_key=True, autoincrement=True)
    position_name = Column(String, nullable=False)
    position_desc = Column(String, nullable=False)
    created_by = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.datetime.now(datetime.timezone.utc))
    modified_by = Column(Integer, nullable=False)
    modified_at = Column(TIMESTAMP, default=datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc))
    is_active = Column(Boolean, default=True)
    
    
class DepartmentModel(Base):
    __tablename__ = "at_sys_msdepartment"
    department_id = Column(Integer, primary_key=True, autoincrement=True)
    department_name = Column(String, nullable=False)
    department_desc = Column(String, nullable=False)
    created_by = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.datetime.now(datetime.timezone.utc))
    modified_by = Column(Integer, nullable=False)
    modified_at = Column(TIMESTAMP, default=datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc))
    is_active = Column(Boolean, default=True)

class UserPositionDepartmentModel(Base):
    __tablename__ = "at_sys_msuserdepartment"
    userdepartment_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer,ForeignKey("at_sys_msuser.user_id"), nullable=False)
    position_id = Column(Integer,ForeignKey("at_sys_msposition.position_id"), nullable=False)
    department_id = Column(Integer,ForeignKey("at_sys_msdepartement.departement_id"), nullable=False)
    created_by = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.datetime.now(datetime.timezone.utc))
    modified_by = Column(Integer, nullable=False)
    modified_at = Column(TIMESTAMP, default=datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc))
    is_active = Column(Boolean, default=True)