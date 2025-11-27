from fastapi import FastAPI
import strawberry
from strawberry.fastapi import GraphQLRouter
from typing import List, Optional, Generator, Any
import uvicorn


@strawberry.type
class User:
    id: int
    name: str
    email: str
    age: Optional[int] = None


@strawberry.type
class Post:
    id: int
    title: str
    content: str
    user_id: int


@strawberry.type
class UsersResponse:
    status: int
    success: bool
    data: List[User]
    meta: "MetaInfo"

@strawberry.type
class PostsResponse:
    status: int
    success: bool
    data: List[Post]
    meta: "MetaInfo"

@strawberry.type
class PostResponse:
    status: int
    success: bool
    data: Post
    meta: "MetaInfo"


@strawberry.type
class MetaInfo:
    total: int


@strawberry.type
class UserResponse:
    status: int
    success: bool
    data: User
    meta: MetaInfo


users_db = [
    User(id=1, name="Анна", email="anna@example.com", age=25),
    User(id=2, name="Петро", email="petro@example.com", age=30),
    User(id=3, name="Марія", email="maria@example.com")
]

posts_db = [
    Post(id=1, title="Мій перший пост", content="Привіт світ!", user_id=1),
    Post(id=2, title="Ще один пост", content="Це другий пост", user_id=1),
    Post(id=3, title="Python", content="Python - чудова мова", user_id=2)
]


@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello World!"

    @strawberry.field
    def users(self) -> UsersResponse:
        return UsersResponse(
            status=200,
            success=True,
            data=users_db,
            meta=MetaInfo(total=len(users_db))
        )
    @strawberry.field
    def posts(self)-> PostsResponse:
        return PostsResponse(
            status=200,
            success=True,
            data=posts_db,
            meta=MetaInfo(total=len(posts_db))
        )

    @strawberry.field
    def one_post(self, id: int) -> PostResponse:
        return PostResponse(
            success=True,
            status=200,
            data=posts_db[id - 1],
            meta=MetaInfo(total=len(posts_db))
        )


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_user(self, name: str, email: str, age: Optional[int] = None) -> UserResponse:
        new_id = len(users_db) + 1
        new_user = User(
            id=new_id,
            name=name,
            email=email,
            age=age
        )
        users_db.append(new_user)
        return UserResponse(
            status=201,
            success=True,
            data=new_user,
            meta=MetaInfo(total=len(users_db))
        )

    @strawberry.mutation
    def create_post(self, title: str, content: str, user_id: int) -> PostResponse:
        new_id = len(posts_db) + 1
        new_post = Post(id=new_id, title=title, content=content, user_id=user_id)
        posts_db.append(new_post)
        return PostResponse(
            status=201,
            success=True,
            data=new_post,
            meta=MetaInfo(total=len(posts_db))
        )

    @strawberry.mutation
    def update_post(self, post_id: int, title: Optional[str]=None) -> PostResponse:
        changed_post = None
        for post in posts_db:
            if post.id == post_id:
                if title:
                    post.title = title
                changed_post = post


        return PostResponse(
            success=True,
            status=200,
            data=changed_post,
            meta=MetaInfo(total=len(posts_db))
        )

    @strawberry.mutation
    def delete_post(self, id: int) -> bool:
        global posts_db
        posts_db = [post for post in posts_db if post.id != id]
        return True



schema = strawberry.Schema(query=Query, mutation=Mutation)
app = FastAPI(title="GraphQL test!")

app.include_router(GraphQLRouter(schema), prefix="/graphql")


@app.get('/')
def root():
    return {
        "status": 200
    }


@app.get("/rest/users")
def get_users() -> dict:
    return {
        "status": 200,
        "success": True,
        "data": users_db,
        "meta": {
            "total": len(users_db)
        }
    }


def main():
    uvicorn.run(app, host="0.0.0.0", port=3000)


if __name__ == '__main__':
    main()