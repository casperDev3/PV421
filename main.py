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
    email: EmailStr
    message: str


class Meta(BaseModel):
    total: int


class RegisterResponse(BaseModel):
    status: int
    success: bool
    data: UserResponse
    meta: Meta


class HealthResponse(BaseModel):
    status: int
    success: bool
    message: str


# utils for JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({
        "exp": expire
    })
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Не валідний токен!")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Не валідний токен!")


# utils for PWD
def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


# Depends
def get_current_user(creds: HTTPAuthorizationCredentials = Depends(security)):
    token = creds.credentials
    username = verify_token(token)
    user = fake_users_db.get(username)
    if not user:
        raise HTTPException(status_code=404, detail="Користувача не знайдено!")
    return user


# auth endpoints
@app.post("/api/register/", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserRegister):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="Користувач з таким ніком вже існує!")

    hashed_password = get_password_hash(user.password)
    fake_users_db[user.username] = {
        "username": user.username,
        "email": user.email,
        "hashed_password": hashed_password,
        "created_at": datetime.utcnow()
    }
    return RegisterResponse(
        success=True,
        status=201,
        data=UserResponse(
            username=user.username,
            email=user.email,
            message="Користувач успішно створений!"
        ),
        meta=Meta(
            total=2
        )
    )


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
