from pyexpat.errors import messages

from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from schemas.user import UserCreate, UserResponse
from helpers import (
    success_response,
    created_response,
    internal_error_response,
    not_found_response, StatusMessage
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


@router.get("/users/", response_model=dict)
def get_all_users(
        adult_only: bool = False,
        name_filter: Optional[str] = None,
):
    try:
        filtered_users = UserService.get_all_users(adult_only, name_filter)
        all_users = UserService.get_all_users()
        return success_response(
            data={
                "users": filtered_users
            },
            meta={
                "count_all_users": len(all_users),
                "count_filtered_users": len(filtered_users)
            }
        )
    except Exception as err:
        return internal_error_response(
            error_details=str(err)
        )


@router.get("/users/{user_id}/", response_model=dict)
def get_user(user_id: int):
    try:
        user = UserService.get_user_by_id(user_id)
        if not user:
            return not_found_response(
                message=StatusMessage.USER_NOT_FOUND.value,
                resource="User"
            )
        return success_response(
            data=user
        )
    except Exception as err:
        return internal_error_response(
            error_details=str(err)
        )
