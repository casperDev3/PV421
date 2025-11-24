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
        """
        Успішна відповідь
        """
        response = {
            "status": status_code.value,
            "success": True,
            "message": message,
            "data": data or {},
            "meta": meta or {}
        }
        return response

    @staticmethod
    def error(
        message: str = StatusMessage.INTERNAL_ERROR.value,
        status_code: StatusCode = StatusCode.HTTP_500_INTERNAL_SERVER_ERROR,
        errors: Optional[List] = None,
        data: Optional[Dict] = None
    ) -> Dict:
        """
        Помилкова відповідь
        """
        response = {
            "status": status_code.value,
            "success": False,
            "message": message,
            "data": data or {},
            "errors": errors or []
        }
        return response

    @staticmethod
    def created(
        data: Any = None,
        message: str = StatusMessage.CREATED.value
    ) -> Dict:
        """
        Відповідь для створення ресурсу
        """
        return ResponseHelper.success(
            data=data,
            message=message,
            status_code=StatusCode.HTTP_201_CREATED
        )

    @staticmethod
    def no_content(
        message: str = StatusMessage.DELETED.value
    ) -> Dict:
        """
        Відповідь для успішного видалення
        """
        return ResponseHelper.success(
            data={"message": message},
            message=message,
            status_code=StatusCode.HTTP_204_NO_CONTENT
        )

    @staticmethod
    def not_found(
        message: str = StatusMessage.NOT_FOUND.value,
        resource: str = "Resource"
    ) -> Dict:
        """
        Відповідь для відсутнього ресурсу
        """
        return ResponseHelper.error(
            message=message,
            status_code=StatusCode.HTTP_404_NOT_FOUND,
            data={"resource": resource}
        )

    @staticmethod
    def unauthorized(
        message: str = StatusMessage.UNAUTHORIZED.value
    ) -> Dict:
        """
        Відповідь для неавторизованого доступу
        """
        return ResponseHelper.error(
            message=message,
            status_code=StatusCode.HTTP_401_UNAUTHORIZED
        )

    @staticmethod
    def validation_error(
        errors: List,
        message: str = StatusMessage.VALIDATION_ERROR.value
    ) -> Dict:
        """
        Відповідь для помилок валідації
        """
        return ResponseHelper.error(
            message=message,
            status_code=StatusCode.HTTP_422_UNPROCESSABLE_ENTITY,
            errors=errors
        )

    @staticmethod
    def conflict(
        message: str = StatusMessage.CONFLICT.value,
        details: Optional[Dict] = None
    ) -> Dict:
        """
        Відповідь для конфлікту ресурсів
        """
        return ResponseHelper.error(
            message=message,
            status_code=StatusCode.HTTP_409_CONFLICT,
            data=details or {}
        )

    @staticmethod
    def internal_error(
        message: str = StatusMessage.INTERNAL_ERROR.value,
        error_details: Optional[str] = None
    ) -> Dict:
        """
        Відповідь для внутрішньої помилки сервера
        """
        data = {}
        if error_details:
            data["error_details"] = error_details

        return ResponseHelper.error(
            message=message,
            status_code=StatusCode.HTTP_500_INTERNAL_SERVER_ERROR,
            data=data
        )

# Швидкі alias для зручності
def success_response(*args, **kwargs):
    return ResponseHelper.success(*args, **kwargs)

def error_response(*args, **kwargs):
    return ResponseHelper.error(*args, **kwargs)

def created_response(*args, **kwargs):
    return ResponseHelper.created(*args, **kwargs)

def not_found_response(*args, **kwargs):
    return ResponseHelper.not_found(*args, **kwargs)

def unauthorized_response(*args, **kwargs):
    return ResponseHelper.unauthorized(*args, **kwargs)

def validation_error_response(*args, **kwargs):
    return ResponseHelper.validation_error(*args, **kwargs)

def conflict_response(*args, **kwargs):
    return ResponseHelper.conflict(*args, **kwargs)

def internal_error_response(*args, **kwargs):
    return ResponseHelper.internal_error(*args, **kwargs)
