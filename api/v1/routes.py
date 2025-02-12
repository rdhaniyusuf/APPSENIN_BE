from fastapi import APIRouter
from api.v1.controllers import account_controller
import sys

sys.dont_write_bytecode = True

router = APIRouter()

router.include_router(account_controller.router, prefix="/users", tags=["Users"])
