from pydantic import BaseModel
from typing import List

class UserCreate(BaseModel):
    name: str
    email: str
    age: int

class User(UserCreate):
    id: int

class UserInDB(User):
    hashed_password: str

# imitation db
user_db: List[User] = []