import uvicorn
from fastapi import FastAPI
from helpers import success_response

app = FastAPI(title="User Management API")

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