from sqlalchemy.orm import Session

from sql_app import models, schemas
from sql_app.enum import OrderStatus, OrderProductStatus, MemberStatus


def get_member(db: Session, member_id: int):
    return db.query(models.Member).filter(models.Member.id == member_id).first()


def get_member_by_email(db: Session, email: str):
    return db.query(models.Member).filter(models.Member.email == email).first()


def get_members(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Member).offset(skip).limit(limit).all()


def create_member(db: Session, member: schemas.MemberCreate):
    fake_hashed_password = member.password # + "notreallyhashed"
    db_member = models.Member(name=member.name,
                              email=member.email,
                              hashed_password=fake_hashed_password,
                              status=MemberStatus.JOIN.value)
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()


def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Order).offset(skip).limit(limit).all()


def create_member_order(db: Session, order: schemas.OrderCreate, member_id: int):
    db_order = models.Order(**order.model_dump(), owner_id=member_id, status=OrderStatus.ALL_PAID)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def get_order_product(db: Session, order_product_id: int):
    return db.query(models.OrderProduct).filter(models.OrderProduct.id == order_product_id).first()


def get_order_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.OrderProduct).offset(skip).limit(limit).all()


def create_order_product(db: Session, order_product: schemas.OrderProductCreate, order_id: int):
    db_order_product = models.OrderProduct(**order_product.model_dump(),
                                           order_id=order_id,
                                           status=OrderProductStatus.PAID.value)
    db.add(db_order_product)
    db.commit()
    db.refresh(db_order_product)
    return db_order_product


def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()


def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

