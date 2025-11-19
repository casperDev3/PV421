from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional, Generator
import time
import uvicorn

app = FastAPI(title="User Management API")

# Декоратор для логування
def log_execution_time(endpoint_name: str):
    def decorator(func):
        def wrapper():
            start_time = time.time()
            result = func()
            execution_time = time.time() - start_time
            print(f"{endpoint_name} executed in {execution_time:.4f} seconds")
            return result
        return  wrapper
    return decorator

# моделі Pydantic
class UserCreate(BaseModel):
    name: str
    email: str
    age: int

class User(UserCreate):
    id: int

#  Збереження даних в аптаймі
users_db = []
user_id_counter = 1


def user_id_generator() -> Generator[int, None, None]:
    global user_id_counter
    while True:
        yield user_id_counter
        user_id_counter += 1

id_gen = user_id_generator()

# lambda filters
filter_adults = lambda users: [user for user in users if user.age >= 18]
filter_by_name = lambda name: lambda users: [user for user in users if name.lower() == user.name.lower()]

def get_user_or_404(user_id: int):
    user = next((user for user in users_db if user.id == user_id), None)
    if not user:
        return {
            "success": False,
            "message": "User not Found!",
            "data": {}
        }
    return {
        "success": True,
        "message": "Ok",
        "data": {
            "user": user
        }
    }


@app.get('/')
@log_execution_time("Root Request / ")
def read_root():
    return {
        "status": 200,
        "success": True,
        "data": {
            "text": "Hello World!"
        },
        "meta": {
            "page": 1,
            "count": 62,
            "per_page": 10
        }
    }

@app.get("/api/health")
def read_health():
    return {
        "status": 200,
        "success": True,
        "data": {
            "message": "Ok"
        },
        "meta": {}
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)