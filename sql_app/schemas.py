from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class ProductBase(BaseModel):
    title: str
    description: str
    category: str
    price: int = 0
    is_active: bool
    is_delete: Optional[bool] = False

    create_at: Optional[datetime] = None
    update_at: Optional[datetime] = None


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True


class OrderProductBase(BaseModel):
    title: str
    price: int = 0
    total_price: int = 0
    cnt: int = 0
    paid_at: Optional[datetime] = None
    refund_at: Optional[datetime] = None

    product_id: int

    create_at: Optional[datetime] = None
    update_at: Optional[datetime] = None


class OrderProductCreate(OrderProductBase):
    pass


class OrderProduct(OrderProductBase):
    id: int
    status: str
    order_id: int

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    title: str
    paid_price: int = 0
    paid_at: Optional[datetime] = None
    refund_price: int = 0
    refund_at: Optional[datetime] = None

    create_at: Optional[datetime] = None
    update_at: Optional[datetime] = None


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    id: int
    status: str
    owner_id: int
    order_products: List[OrderProduct] = []

    class Config:
        from_attributes = True


class MemberBase(BaseModel):
    name: str
    email: str
    create_at: Optional[datetime] = None


class MemberCreate(MemberBase):
    password: str


class Member(MemberBase):
    id: int
    status: str
    is_active: bool
    orders: List[Order] = []

    class Config:
        from_attributes = True
