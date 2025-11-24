from fastapi import APIRouter, HTTPException, status
from fastapi.security import  OAuth2PasswordBearer, OAuth2PasswordRequestForm
from  datetime import  timedelta
from schemas.user import UserCreate, Token, UserLogin
from helpers import (
    success_response,
    created_response,
    conflict_response,
    unauthorized_response,
    not_found_response,
    StatusMessage
)

# TODO: Check libs
# from services.auth_service import AuthService

router = APIRouter()
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

# fake_users_db = {
#     "user@example.com": {
#         "email": "user@example.com",
#         "hashed_password": AuthService.get_password_hash("password123"),
#         "name": "Test User",
#         "age": 25
#     }
# }

@router.post("/register/", response_model=dict)
def register():
    print("register")
    return success_response()

@router.post("/login/", response_model=dict)
def login():
    print("login")
    return success_response()

@router.post("/password/change/")
def change_pwd():
    print("change password")
    return success_response()

@router.post("/password/reset/")
def reset_password():
    print("reset password")
    return success_response()

@router.post("/password/new/")
def set_new_pwd():
    print("new password!")
    return success_response()