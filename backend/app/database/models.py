import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Integer, default=1)

    history_items = relationship("GenerationHistory", back_populates="owner")

class GenerationHistory(Base):
    __tablename__ = "generation_history"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True, nullable=False)
    title = Column(String, nullable=False)
    status = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="history_items")
