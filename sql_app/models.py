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
    create_at = Column(DateTime(timezone=True), server_default=func.now())

    books = relationship("Book", back_populates="owner")


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    category = Column(String)
    price = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    create_at = Column(DateTime(timezone=True), server_default=func.now())

    owner_id = Column(Integer, ForeignKey("members.id"))
    owner = relationship("Member", back_populates="books")
