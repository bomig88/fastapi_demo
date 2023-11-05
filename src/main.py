from os.path import realpath
from typing import List

from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles

from sqlalchemy.orm import Session
from sql_app import models, schemas, crud
from sql_app.database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 이렇게 하면 전체 API 서버 (app의로 정의한)에 모든 HTTP Status 코드에 따른 정적 파일을 리턴할 수 있다.
# /static 폴더에 404.html 405.html 파일들을 저장해두면 알아서 서빙한다.
def configure_static(_app):
    # _app.mount("/static", StaticFiles(directory='static'), name="static")
    _app.mount('/static', StaticFiles(directory=realpath(f'{realpath(__file__)}/../../static')), name='static')


def start_application():
    _app = FastAPI()
    configure_static(_app)
    return _app


app = start_application()


@app.get("/")
def read_root():
    return {'Hello': 'World'}


@app.post("/members/", response_model=schemas.Member)
def create_member(member: schemas.MemberCreate, db: Session = Depends(get_db)):
    db_member = crud.get_member_by_email(db, email=member.email)
    if db_member:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_member(db=db, member=member)


@app.get("/members/", response_model=List[schemas.Member])
def read_members(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    members = crud.get_members(db=db, skip=skip, limit=limit)
    return members


@app.get("/members/{member_id}", response_model=schemas.Member)
def read_member(member_id: int, db: Session = Depends(get_db)):
    db_member = crud.get_member(db=db, member_id=member_id)
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return db_member


@app.post("/members/{member_id}/orders/", response_model=schemas.Order)
def create_order_for_member(
        member_id: int, order: schemas.OrderCreate, order_products: List[schemas.OrderProductCreate],
        db: Session = Depends(get_db)
):
    order = crud.create_member_order(db=db, order=order, member_id=member_id)

    for op in order_products:
        crud.create_order_product(db=db, order_product=op, order_id=order.id)

    return crud.get_order(db=db, order_id=order.id)


@app.get("/orders/", response_model=List[schemas.Order])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = crud.get_orders(db=db, skip=skip, limit=limit)
    return orders


@app.get("/orders/{order_id}", response_model=schemas.Order)
def read_order(order_id: int, db: Session = Depends(get_db)):
    order = crud.get_order(db=db, order_id=order_id)
    return order


@app.get("/order-products/", response_model=List[schemas.Order])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = crud.get_order_products(db=db, skip=skip, limit=limit)
    return orders


@app.get("/orders-products/{order_product_id}", response_model=schemas.Order)
def read_order(order_product_id: int, db: Session = Depends(get_db)):
    order = crud.get_order_product(db=db, order_product_id=order_product_id)
    return order


@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db=db, product=product)


@app.get("/products/", response_model=List[schemas.Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = crud.get_products(db=db, skip=skip, limit=limit)
    return products


@app.get("/products/{product_id}", response_model=schemas.Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    products = crud.get_product(db=db, product_id=product_id)
    return products
