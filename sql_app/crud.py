from sqlalchemy.orm import Session

from sql_app import models, schemas


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
                              hashed_password=fake_hashed_password)
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()


def create_member_book(db: Session, book: schemas.BookCreate, member_id: int):
    db_book = models.Book(**book.model_dump(), owner_id=member_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
