import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    generation_count = Column(Integer, default=0) # Track monthly usage
    last_reset_date = Column(DateTime, default=datetime.datetime.utcnow) # Track when the count was last reset

    history_items = relationship("GenerationHistory", back_populates="owner")
    subscription = relationship("Subscription", back_populates="user", uselist=False, cascade="all, delete-orphan")

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
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    plan_id = Column(Integer, ForeignKey("plans.id"), nullable=False)
    stripe_subscription_id = Column(String, unique=True, index=True, nullable=False)
    status = Column(String, nullable=False) # e.g., "active", "canceled", "past_due"
    current_period_end = Column(DateTime, nullable=False)
    
    user = relationship("User", back_populates="subscription")
    plan = relationship("Plan")

class GenerationHistory(Base):
    __tablename__ = "generation_history"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True, nullable=False)
    title = Column(String, nullable=False)
    status = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="history_items")
