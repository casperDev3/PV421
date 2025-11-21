from models.user import user_db, User, UserCreate
from utils.id_generator import id_gen

class UserService:
    @staticmethod
    def create_user(user: UserCreate) -> User:
        new_user = User(
            id=next(id_gen),
            name=user.name,
            email=user.email,
            age=user.age
        )
        user_db.append(new_user)
        return new_user