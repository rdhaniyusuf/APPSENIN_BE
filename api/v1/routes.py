from fastapi import APIRouter
from . import account_controller, dashboard_controller
import sys
sys.dont_write_bytecode = True

router = APIRouter()

router.include_router(account_controller.router, prefix="/users", tags=["Users"])

router.include_router(dashboard_controller.router, prefix="/dashboard", tags=["Dashboard"])
