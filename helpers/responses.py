from typing import Any, Dict, Optional, List
from helpers.status_codes import StatusCode, StatusMessage


class ResponseHelper:
    @staticmethod
    def success(
            data: Optional[Any] = None,
            message: str = StatusMessage.SUCCESS.value,
            status_code: StatusCode = StatusCode.HTTP_200_OK,
            meta: Optional[Dict] = None
    ) -> Dict:
        return {
            "status": status_code.value,
            "success": True,
            "message": message,
            "data": data or {},
            "meta": meta or {}
        }

    @staticmethod
    def error(
            message: str = StatusMessage.INTERNAL_ERROR.value,
            status_code: StatusCode = StatusCode.HTTP_500_INTERNAL_SERVER_ERROR,
            errors: Optional[List] = None,
            data: Optional[Dict] = None
    ):
        response = {
            "status": status_code.value,
            "success": False,
            "message": message,
            "data": data or {},
            "errors": errors or {}
        }
        return response

    @staticmethod
    def created(
            data: Any = None,
            message: str = StatusMessage.CREATED.value,
    ) -> Dict:
        return ResponseHelper.success(
            data=data,
            message=message,
            status_code=StatusCode.HTTP_201_CREATED
        )


# alias
def success_response(*args, **kwargs):
    return ResponseHelper.success(*args, **kwargs)

def created_response(*args, **kwargs):
    return  ResponseHelper.created(*args, **kwargs)

def internal_error_response(*args, **kwargs):
    return  ResponseHelper.error(*args, **kwargs)