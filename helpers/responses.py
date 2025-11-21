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


# alias
def success_response(*args, **kwargs):
    return ResponseHelper.success(*args, **kwargs)