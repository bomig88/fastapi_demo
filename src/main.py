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


@app.post("/members/{member_id}/books/", response_model=schemas.Book)
def create_book_for_member(
        member_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)
):
    return crud.create_member_book(db=db, book=book, member_id=member_id)


@app.get("/books/", response_model=List[schemas.Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = crud.get_books(db=db, skip=skip, limit=limit)
    return books
