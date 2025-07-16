import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum
from .base import Base
from app.utils.helpers import get_password_hash

class User(Base):
    __tablename__ = "users"
 
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    subscription = relationship("Subscription", back_populates="user", uselist=False)
    generation_history = relationship("GenerationHistory", back_populates="user")

    def __init__(self, email, password):
        self.email = email
        self.hashed_password = self.get_password_hash(password)

    @staticmethod
    def get_password_hash(password):
        return get_password_hash(password)

class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False) # e.g., "Freemium", "Starter", "Pro"
    price = Column(Integer, nullable=False) # Store in cents to avoid floating point issues
    generations_limit = Column(Integer, nullable=False)
    stripe_price_id = Column(String, unique=True, nullable=False) # From your Stripe dashboard

class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    plan = Column(String, default="Free")
    status = Column(Enum("active", "inactive", "canceled", name="subscription_status"), default="inactive")
    renewal_date = Column(DateTime, nullable=True)  # Can be None for 'inactive' or 'canceled' subscriptions
    user = relationship("User", back_populates="subscription")

class GenerationHistory(Base):
    __tablename__ = "generation_history"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True, nullable=False)
    title = Column(String, nullable=False)
    status = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="history_items")
