import uvicorn
from fastapi import FastAPI
from helpers import success_response
from controllers import users, auth

# init app
app = FastAPI(title="User Management API")

# connect routes
app.include_router(users.router, prefix="/api", tags=["users"])
app.include_router(auth.router, prefix="/api", tags=["auth"])

# default routes
@app.get('/')
def read_root():
    return success_response(
        data = {
            "text": "Hello World!"
        },
        meta = {
            "page": 1,
            "count": 62
        }
    )


@app.get("/api/health")
def read_health():
    return success_response(
        data = {
            "text": "Service is healthy!"
        }
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)