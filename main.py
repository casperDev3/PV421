from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr, Field
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional

# Конфігурація
SECRET_KEY = "your-secret-key-change-in-production"  # Змініть у продакшені!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI(title="FastAPI JWT Auth", version="1.0.0")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
fake_users_db = {}
security = HTTPBearer()


# Моделі Pydantic
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


# Утиліти для JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Невалідний токен")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Невалідний токен")


# Утиліти для паролів
def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


# Dependency для отримання поточного користувача
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    username = verify_token(token)
    user = fake_users_db.get(username)
    if not user:
        raise HTTPException(status_code=401, detail="Користувача не знайдено")
    return user


# Ендпоїнти
@app.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserRegister):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="Користувач з таким іменем вже існує")

    hashed_password = get_password_hash(user.password)
    fake_users_db[user.username] = {
        "username": user.username,
        "email": user.email,
        "hashed_password": hashed_password,
        "created_at": datetime.utcnow()
    }

    return {
        "username": user.username,
        "email": user.email,
        "message": "Користувач успішно створений"
    }


@app.post("/login")
async def login(user_credentials: UserLogin):
    user = fake_users_db.get(user_credentials.username)
    if not user or not verify_password(user_credentials.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невірний логін або пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }


@app.post("/change-password")
async def change_password(
        password_data: PasswordChange,
        current_user: dict = Depends(get_current_user)
):
    if not verify_password(password_data.current_password, current_user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Поточний пароль введено неправильно"
        )

    new_hashed_password = get_password_hash(password_data.new_password)
    current_user["hashed_password"] = new_hashed_password

    return {"message": "Пароль успішно змінений"}


@app.get("/profile", response_model=UserResponse)
async def get_profile(current_user: dict = Depends(get_current_user)):
    return {
        "username": current_user["username"],
        "email": current_user["email"],
        "message": "Профіль успішно отримано"
    }


@app.get("/")
async def root():
    return {
        "message": "FastAPI JWT Auth API",
        "endpoints": {
            "register": "/register (POST)",
            "login": "/login (POST)",
            "change_password": "/change-password (POST)",
            "profile": "/profile (GET) - Захищений ендпоїнт"
        }
    }


# Код для запуску сервера
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)