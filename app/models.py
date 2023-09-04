from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.orm import Relationship, relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), nullable=False)
    content = Column(String(255), nullable=False)
    published = Column(Boolean, nullable=False, default=True) 
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    # created_at = Column(DateTime, server_default=text('now()'))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = Relationship("User")
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(300), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))