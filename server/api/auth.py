"""Authentication routes: register, login, refresh, change password, current user."""
from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from controllers import auth_controller
from database.connection import get_db
from middleware.auth import get_current_user
from schemas.auth_schema import ChangePasswordRequest, LoginRequest, RefreshRequest, RegisterRequest, TokenResponse
from utils.response import success_response

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=None)
async def register(payload: RegisterRequest, db: AsyncIOMotorDatabase = Depends(get_db)):
    tokens = await auth_controller.register_user(db, payload)
    return success_response(tokens, "Registration successful", 201)


@router.post("/login", response_model=None)
async def login(payload: LoginRequest, db: AsyncIOMotorDatabase = Depends(get_db)):
    tokens = await auth_controller.login_user(db, payload)
    return success_response(tokens, "Login successful")


@router.post("/refresh", response_model=None)
async def refresh(payload: RefreshRequest):
    tokens = await auth_controller.refresh_access_token(payload.refresh_token)
    return success_response(tokens, "Token refreshed")


@router.post("/change-password", response_model=None)
async def change_password(
    payload: ChangePasswordRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    await auth_controller.change_password(db, current_user, payload)
    return success_response(None, "Password changed successfully")


@router.get("/me", response_model=None)
async def me(current_user: dict = Depends(get_current_user)):
    current_user.pop("password", None)
    return success_response(current_user, "Current user fetched")
