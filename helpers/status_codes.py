from enum import Enum

class StatusCode(Enum):
    # Успішні відповіді
    HTTP_200_OK = 200
    HTTP_201_CREATED = 201
    HTTP_204_NO_CONTENT = 204

    # Клієнтські помилки
    HTTP_400_BAD_REQUEST = 400
    HTTP_401_UNAUTHORIZED = 401
    HTTP_403_FORBIDDEN = 403
    HTTP_404_NOT_FOUND = 404
    HTTP_409_CONFLICT = 409
    HTTP_422_UNPROCESSABLE_ENTITY = 422

    # Серверні помилки
    HTTP_500_INTERNAL_SERVER_ERROR = 500
    HTTP_503_SERVICE_UNAVAILABLE = 503

class StatusMessage(Enum):
    # Успішні повідомлення
    SUCCESS = "Success"
    CREATED = "Created successfully"
    UPDATED = "Updated successfully"
    DELETED = "Deleted successfully"

    # Повідомлення про помилки
    NOT_FOUND = "Resource not found"
    UNAUTHORIZED = "Unauthorized access"
    FORBIDDEN = "Access forbidden"
    VALIDATION_ERROR = "Validation error"
    CONFLICT = "Resource conflict"
    INTERNAL_ERROR = "Internal server error"
    SERVICE_UNAVAILABLE = "Service temporarily unavailable"

    # Аутентифікація
    LOGIN_SUCCESS = "Login successful"
    LOGIN_FAILED = "Invalid credentials"
    REGISTER_SUCCESS = "Registration successful"
    INVALID_TOKEN = "Invalid or expired token"

    # Користувачі
    USER_CREATED = "User created successfully"
    USER_UPDATED = "User updated successfully"
    USER_DELETED = "User deleted successfully"
    USER_NOT_FOUND = "User not found"
    USER_EXISTS = "User already exists"
