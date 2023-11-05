from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, Text, ForeignKey
from sqlalchemy.orm import relationship

from sql_app.database import Base


class Member(Base):
    __tablename__ = 'members'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(40))
    email = Column(String, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    status = Column(String(20))
    create_at = Column(DateTime(timezone=True), server_default=func.now())
    update_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    orders = relationship("Order", back_populates="owner")


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    status = Column(String(40))
    paid_price = Column(Integer, default=0)
    paid_at = Column(DateTime(timezone=True), nullable=True)
    refund_price = Column(Integer, default=0)
    refund_at = Column(DateTime(timezone=True), nullable=True)
    create_at = Column(DateTime(timezone=True), server_default=func.now())
    update_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    owner_id = Column(Integer, ForeignKey("members.id"))
    owner = relationship("Member", back_populates="orders")

    order_products = relationship("OrderProduct", back_populates="order")


class OrderProduct(Base):
    __tablename__ = 'order_products'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(120), index=True)
    price = Column(Integer, default=0)
    total_price = Column(Integer, default=0)
    status = Column(String(40))
    cnt = Column(Integer, default=0)
    paid_at = Column(DateTime(timezone=True), nullable=True)
    refund_at = Column(DateTime(timezone=True), nullable=True)
    create_at = Column(DateTime(timezone=True), server_default=func.now())
    update_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    order_id = Column(Integer, ForeignKey("orders.id"))
    order = relationship("Order", back_populates="order_products")

    product_id = Column(Integer, ForeignKey("products.id"))


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(120), index=True)
    description = Column(Text)
    category = Column(String(60))
    price = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    is_delete = Column(Boolean, default=False)
    create_at = Column(DateTime(timezone=True), server_default=func.now())
    update_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
