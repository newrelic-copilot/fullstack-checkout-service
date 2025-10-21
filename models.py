from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum


class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    image_url: str
    stock: int


class CartItem(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


class CheckoutRequest(BaseModel):
    items: List[CartItem]
    customer_name: str
    customer_email: str
    shipping_address: str
    payment_method: str


class OrderItem(BaseModel):
    product_id: int
    product_name: str
    quantity: int
    price: float
    subtotal: float


class Order(BaseModel):
    order_id: str
    customer_name: str
    customer_email: str
    shipping_address: str
    payment_method: str
    items: List[OrderItem]
    total_amount: float
    status: OrderStatus
    created_at: datetime
