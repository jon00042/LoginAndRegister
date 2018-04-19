from sqlalchemy.orm import relationship, backref, joinedload
from sqlalchemy import Column, DateTime, String, Integer, Float, ForeignKey, func, UniqueConstraint

from db.base import Base, inverse_relationship, create_tables 

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)

    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
