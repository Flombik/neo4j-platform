from fastapi import APIRouter

from .routers import login, users

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/user", tags=["users"])
