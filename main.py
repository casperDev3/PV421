from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Demo", version="0.0.1")

@app.get("/")
async def root():
    return {
        "tasks": {
            "/lambda/filter": "Лямбда-функції для фільтрації",
            "/generators/fibonacci": "Генератор Фібоначчі",
            "/generators/primes": "Генератор простих чисел",
            "/closures/counter": "Демонстрація замикань",
            "/decorators/demo": "Демонстрація декораторів"
        }
    }

@app.get('/api/test')
async def test():
    return {
        "test": 25
    }


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8080)

