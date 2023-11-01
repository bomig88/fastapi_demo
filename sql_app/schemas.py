from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: str
    price: int
    is_active: bool
    create_at: Optional[datetime] = None


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int
    owner_id: int

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
    is_active: bool
    books: List[Book] = []

    class Config:
        from_attributes = True
