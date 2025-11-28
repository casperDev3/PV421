import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr, Field
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional

from typing_extensions import deprecated

# Config
SECRET_KEY = "some-secret-kay-change-on-prod"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Init
app = FastAPI(title="FastAPi", version="0.0.1")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
fake_users_db = {}
security = HTTPBearer()


# Models
class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    username: str
    password: str


class PasswordChange(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=6)


class UserResponse(BaseModel):
    username: str
    email: str
    message: str


class HealthResponse(BaseModel):
    status: int
    success: bool
    message: str


# default endpoints
@app.get("/api/health")
def health():
    return HealthResponse(
        success=True,
        status=200,
        message="ok!"
    )

@app.get("/")
def root():
    return "Server is working!"

def main():
    uvicorn.run(app, host="0.0.0.0", port=3000)

if __name__ == '__main__':
    main()

