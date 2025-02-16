import sys
sys.dont_write_bytecode = True
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()