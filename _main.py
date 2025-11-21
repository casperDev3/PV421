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

        return wrapper

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


@app.post("/api/users/")
# @log_execution_time("Create User: ")
def create_user(user: UserCreate):
    try:
        new_user = {
            "id": next(id_gen),
            "name": user.name,
            "email": user.email,
            "age": user.age
        }
        users_db.append(new_user)
        return {
            "status": 201,
            "success": True,
            "data": {
                "user": new_user
            },
            "meta": {}
        }
    except Exception as err:
        return {
            "status": 500,
            "success": False,
            "data": {
                "message": f"{err}"
            },
            "meta": {}
        }


@app.get("/api/users/")
@log_execution_time("Get all users: ")
def get_all_users(
        adult_only: bool = False,
        name_filter: Optional[str] = None
):
    filtered_users = users_db

    if adult_only:
        filtered_users = filter_adults(filtered_users)

    if name_filter:
        filtered_users = filter_by_name(filtered_users)

    return {
        "status": 200,
        "success": True,
        "data": {
            "users": filtered_users
        },
        "meta": {
            "all_users": len(users_db),
            "result_users": len(filtered_users)
        }
    }


@app.get("/api/users/{user_id}")
@log_execution_time("Get One User")
def get_user(user: User = Depends(get_user_or_404)):
    return {
        "status": 200,
        "success": True,
        "data": {
            **user.dict()
        },
        "meta": {

        }
    }


@app.put("/api/users/{user_id}")
@log_execution_time("Update User")
def update_user(
        user_id: int,
        updated_user: UserCreate,
        current_user: User = Depends(get_user_or_404)
):
    user_index = next(i for i, user in enumerate(users_db) if user.id == user_id)
    users_db[user_index] = User(id=user_id, **updated_user.dict())
    return {
        "status": 200,
        "success": True,
        "data": {
            **users_db[user_index].dict()
        },
        "meta": {}
    }

@app.delete("/api/users/{user_id}")
@log_execution_time("Delete User")
def delete_user(user: User = Depends(get_user_or_404)):
    users_db[:] = [u for u in users_db if u.id != user.id]
    return {
        "status": 204,
        "success": True,
        "data": {
            "message": "User was deleted!"
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
