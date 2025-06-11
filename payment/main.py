import os
from dotenv import load_dotenv
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks
from redis_om import get_redis_connection, HashModel
from starlette.requests import Request
import requests
import time


# Load the environment variables from payment-specific file
env_path = Path(__file__).parent / '.env.payment'
load_dotenv(dotenv_path=env_path)
PRODUCT_SERVICE_URL = os.environ.get(
    "PRODUCT_SERVICE_URL", "http://localhost:8000")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*',],
    allow_headers=['*']
)

# This should be a different database
redis = get_redis_connection(
    host=os.environ["REDIS_HOST"],
    port=int(os.environ["REDIS_PORT"]),
    username=os.environ.get("REDIS_USERNAME"),
    password=os.environ.get("REDIS_PASSWORD"),
    decode_responses=True,
)


class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str  # Pending, completed, refunded

    class Meta:
        database = redis


@app.get('/orders/{pk}')
def get(pk: str):
    return Order.get(pk)


@app.post('/orders')
async def create(request: Request, background_tasks: BackgroundTasks):  # id, quantity
    body = await request.json()

    req = requests.get(f'{PRODUCT_SERVICE_URL}/products/{body["id"]}')
    product = req.json()

    order = Order(
        product_id=body['id'],
        price=product['price'],
        fee=0.2 * product['price'],
        total=1.2 * product['price'],
        quantity=body['quantity'],
        status='pending'
    )

    order.save()

    background_tasks.add_task(order_completed, order)

    return order


def order_completed(order: Order):
    time.sleep(5)
    order.status = 'completed'
    order.save()

    redis.xadd('order_completed', order.dict(), )
    # redis.xadd('order_completed', order.model_dump(), '*')
