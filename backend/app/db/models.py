import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Text, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.db.database import Base

class UserModel(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(120), unique=True, index=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    trips = relationship("TripPlanModel", back_populates="user", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "full_name": self.full_name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

class TripPlanModel(Base):
    __tablename__ = "trip_plans"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True, index=True)
    origin = Column(String(100), nullable=False)
    destination = Column(String(100), nullable=False)
    duration_days = Column(Integer, nullable=False)
    budget = Column(Float, nullable=False)
    currency = Column(String(10), default="INR")
    travel_style = Column(String(50), default="Standard")
    interests = Column(JSON, default=list)
    itinerary_json = Column(JSON, nullable=False)
    raw_response = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("UserModel", back_populates="trips")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "origin": self.origin,
            "destination": self.destination,
            "duration_days": self.duration_days,
            "budget": self.budget,
            "currency": self.currency,
            "travel_style": self.travel_style,
            "interests": self.interests,
            "itinerary": self.itinerary_json,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
