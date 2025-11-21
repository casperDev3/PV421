from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from schemas.user import UserCreate, UserResponse
from helpers import (
    success_response,
    created_response,
    internal_error_response
)
from services.user_service import UserService

router = APIRouter()


@router.post("/users/", response_model=dict)
def create_user(user: UserCreate):
    try:
        response = UserService.create_user(user)
        return created_response(
            data=response,
        )
    except Exception as err:
        return internal_error_response(
            errors=str(err)
        )
