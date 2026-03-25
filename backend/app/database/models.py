import datetime
from sqlalchemy import Integer, String, ForeignKey, DateTime, Boolean, Enum as SAEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column
import enum
from typing import List, Optional
from .base import Base
from app.utils.helpers import get_password_hash

class SubscriptionStatus(str, enum.Enum):
    active = "active"
    inactive = "inactive"
    canceled = "canceled"

class GenerationStatus(str, enum.Enum):
    pending = "pending"
    processing = "processing"
    completed = "completed"
    failed = "failed"

class User(Base):
    __tablename__ = "users"
 
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    
    subscription: Mapped[Optional["Subscription"]] = relationship(back_populates="user", uselist=False)
    history_items: Mapped[List["GenerationHistory"]] = relationship(back_populates="owner")

    @staticmethod
    def get_password_hash(password: str) -> str:
        return get_password_hash(password)

class Plan(Base):
    __tablename__ = "plans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False) # cents
    generations_limit: Mapped[int] = mapped_column(Integer, nullable=False)
    stripe_price_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)

class Subscription(Base):
    __tablename__ = "subscriptions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    plan: Mapped[str] = mapped_column(String, default="Free")
    status: Mapped[SubscriptionStatus] = mapped_column(SAEnum(SubscriptionStatus), default=SubscriptionStatus.inactive)
    renewal_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)
    
    user: Mapped["User"] = relationship(back_populates="subscription")

class GenerationHistory(Base):
    __tablename__ = "generation_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    url: Mapped[str] = mapped_column(String, index=True, nullable=False)
    title: Mapped[Optional[str]] = mapped_column(String, nullable=True) # nullable if pending
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    bullet_points: Mapped[Optional[str]] = mapped_column(String, nullable=True) # store as JSON string or text block
    keywords_report: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    status: Mapped[GenerationStatus] = mapped_column(SAEnum(GenerationStatus), default=GenerationStatus.pending)
    date: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    owner: Mapped["User"] = relationship(back_populates="history_items")
