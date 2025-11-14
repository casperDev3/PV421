"""
Демонстрація основних концепцій Python з FastAPI:
- Кортежі (Tuples)
- Словники (Dictionaries)
- Лямбда-функції
- Генератори
- Замикання (Closures)
- Декоратори
"""

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Dict, Tuple, Optional
from functools import wraps
import time
from datetime import datetime
import uvicorn

app = FastAPI(title="Python Concepts Demo", version="1.0")


# ===== ДЕКОРАТОРИ =====
def timer_decorator(func):
    """Декоратор для вимірювання часу виконання функції"""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        end = time.time()
        print(f"⏱️ {func.__name__} виконано за {end - start:.4f} секунд")
        return result

    return wrapper


def log_request(func):
    """Декоратор для логування запитів"""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"📝 [{timestamp}] Виклик функції: {func.__name__}")
        result = await func(*args, **kwargs)
        print(f"✅ [{timestamp}] Функція {func.__name__} виконана успішно")
        return result

    return wrapper


def validate_positive(func):
    """Декоратор для валідації позитивних чисел"""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        if 'number' in kwargs and kwargs['number'] <= 0:
            raise HTTPException(status_code=400, detail="Число має бути додатнім")
        return await func(*args, **kwargs)

    return wrapper


# ===== ЗАМИКАННЯ =====
def create_counter():
    """Замикання для створення лічильника"""
    count = 0

    def increment():
        nonlocal count
        count += 1
        return count

    return increment


def create_multiplier(factor):
    """Замикання для створення функції множення"""

    def multiply(x):
        return x * factor

    return multiply


def create_filter_function(threshold):
    """Замикання для створення функції фільтрації"""

    def filter_values(values):
        return [v for v in values if v > threshold]

    return filter_values


# Глобальні лічильники через замикання
request_counter = create_counter()
double = create_multiplier(2)
triple = create_multiplier(3)


# ===== ГЕНЕРАТОРИ =====
def fibonacci_generator(n: int):
    """Генератор чисел Фібоначчі"""
    a, b = 0, 1
    count = 0
    while count < n:
        yield a
        a, b = b, a + b
        count += 1


def prime_generator(limit: int):
    """Генератор простих чисел до заданого ліміту"""

    def is_prime(num):
        if num < 2:
            return False
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                return False
        return True

    for num in range(2, limit + 1):
        if is_prime(num):
            yield num


def batch_processor(data: List, batch_size: int):
    """Генератор для обробки даних пакетами"""
    for i in range(0, len(data), batch_size):
        yield data[i:i + batch_size]


# ===== КОРТЕЖІ =====
# Зберігаємо дані студентів як кортежі (незмінні)
STUDENTS_DATA: Tuple[Tuple[str, int, str], ...] = (
    ("Іван", 20, "Програмування"),
    ("Марія", 22, "Математика"),
    ("Петро", 21, "Фізика"),
    ("Ольга", 19, "Хімія"),
    ("Андрій", 23, "Біологія")
)

# Координати міст (широта, довгота, назва)
CITIES: Tuple[Tuple[float, float, str], ...] = (
    (50.4501, 30.5234, "Київ"),
    (49.8397, 24.0297, "Львів"),
    (48.4647, 35.0462, "Дніпро"),
    (46.4825, 30.7233, "Одеса")
)

# ===== СЛОВНИКИ =====
# База даних товарів (словники)
products_db: Dict[int, Dict[str, any]] = {
    1: {"name": "Ноутбук", "price": 25000, "category": "Електроніка", "stock": 15},
    2: {"name": "Телефон", "price": 15000, "category": "Електроніка", "stock": 30},
    3: {"name": "Книга", "price": 300, "category": "Література", "stock": 100},
    4: {"name": "Навушники", "price": 2000, "category": "Аксесуари", "stock": 50}
}

# Користувачі з вкладеними словниками
users_db: Dict[str, Dict[str, any]] = {
    "user1": {"name": "Іван", "age": 25, "purchases": [1, 3], "balance": 30000},
    "user2": {"name": "Марія", "age": 30, "purchases": [2], "balance": 20000},
    "user3": {"name": "Петро", "age": 28, "purchases": [], "balance": 50000}
}


# ===== МОДЕЛІ PYDANTIC =====
class Product(BaseModel):
    id: int
    name: str
    price: float
    category: str
    stock: int


class Student(BaseModel):
    name: str
    age: int
    major: str


class City(BaseModel):
    latitude: float
    longitude: float
    name: str


# ===== API ENDPOINTS =====

@app.get("/")
async def root():
    """Головна сторінка з описом API"""
    return {
        "message": "🐍 Демонстрація Python концепцій з FastAPI",
        "endpoints": {
            "/tuples/students": "Робота з кортежами (студенти)",
            "/tuples/cities": "Робота з кортежами (міста)",
            "/dicts/products": "Робота зі словниками (товари)",
            "/lambda/filter": "Лямбда-функції для фільтрації",
            "/generators/fibonacci": "Генератор Фібоначчі",
            "/generators/primes": "Генератор простих чисел",
            "/closures/counter": "Демонстрація замикань",
            "/decorators/demo": "Демонстрація декораторів"
        }
    }


@app.get("/tuples/students", response_model=List[Student])
@log_request
async def get_students():
    """Отримати список студентів (демонстрація кортежів)"""
    return [{"name": s[0], "age": s[1], "major": s[2]} for s in STUDENTS_DATA]


@app.get("/tuples/cities", response_model=List[City])
async def get_cities():
    """Отримати координати міст (демонстрація кортежів)"""
    return [{"latitude": c[0], "longitude": c[1], "name": c[2]} for c in CITIES]


@app.get("/dicts/products", response_model=List[Product])
async def get_products(
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None
):
    """Отримати товари з фільтрацією (демонстрація словників)"""
    result = []

    for pid, product in products_db.items():
        if category and product["category"] != category:
            continue
        if min_price and product["price"] < min_price:
            continue
        if max_price and product["price"] > max_price:
            continue
        result.append({"id": pid, **product})

    return result


@app.get("/lambda/filter")
async def lambda_filter_demo(threshold: int = Query(default=1000)):
    """Демонстрація лямбда-функцій для фільтрації та сортування"""
    prices = [p["price"] for p in products_db.values()]

    # Лямбда-функції для різних операцій
    filter_expensive = lambda x: x > threshold
    double_price = lambda x: x * 2
    format_price = lambda x: f"{x:.2f} грн"

    expensive_prices = list(filter(filter_expensive, prices))
    doubled_prices = list(map(double_price, prices))
    sorted_prices = sorted(prices, key=lambda x: -x)  # Сортування за спаданням

    return {
        "original_prices": prices,
        "expensive_prices": expensive_prices,
        "doubled_prices": doubled_prices,
        "sorted_desc": sorted_prices,
        "formatted": list(map(format_price, prices))
    }


@app.get("/generators/fibonacci")
@timer_decorator
async def get_fibonacci(n: int = Query(default=10, ge=1, le=50)):
    """Генератор чисел Фібоначчі"""
    fib_numbers = list(fibonacci_generator(n))
    return {
        "count": n,
        "fibonacci_sequence": fib_numbers,
        "sum": sum(fib_numbers),
        "is_generator": "Використано генератор для економії пам'яті"
    }


@app.get("/generators/primes")
@timer_decorator
@log_request
async def get_primes(limit: int = Query(default=100, ge=2, le=1000)):
    """Генератор простих чисел"""
    prime_numbers = list(prime_generator(limit))
    return {
        "limit": limit,
        "primes": prime_numbers,
        "count": len(prime_numbers),
        "largest": prime_numbers[-1] if prime_numbers else None
    }


@app.get("/closures/counter")
async def closure_counter_demo():
    """Демонстрація замикань"""
    count = request_counter()

    # Використання різних замикань
    filter_gt_1000 = create_filter_function(1000)
    prices = [p["price"] for p in products_db.values()]

    return {
        "request_number": count,
        "double_of_10": double(10),
        "triple_of_10": triple(10),
        "prices": prices,
        "expensive_products": filter_gt_1000(prices),
        "explanation": "Кожна функція зберігає свій власний стан через замикання"
    }


@app.get("/decorators/demo")
@timer_decorator
@log_request
@validate_positive
async def decorators_demo(number: int = Query(default=5, ge=1)):
    """Демонстрація всіх декораторів разом"""

    # Комбінація всіх концепцій
    fib = list(fibonacci_generator(number))
    doubled = list(map(lambda x: x * 2, fib))

    return {
        "input": number,
        "fibonacci": fib,
        "doubled": doubled,
        "decorators_applied": ["timer", "log_request", "validate_positive"],
        "message": "Перевірте консоль для логів декораторів!"
    }


if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8000)