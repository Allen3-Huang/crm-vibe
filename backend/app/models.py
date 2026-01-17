from datetime import date, datetime
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    """用戶模型 - 存儲 Google OAuth 登入的用戶"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    picture = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)

    event_attendances = relationship("EventAttendance", back_populates="customer")
    course_purchases = relationship("CoursePurchase", back_populates="customer")


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String, unique=True, index=True, nullable=False)
    event_name = Column(String, nullable=False)

    attendances = relationship("EventAttendance", back_populates="event")


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(String, unique=True, index=True, nullable=False)
    course_name = Column(String, nullable=False)

    purchases = relationship("CoursePurchase", back_populates="course")


class EventAttendance(Base):
    __tablename__ = "event_attendances"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    date = Column(Date, nullable=False)

    customer = relationship("Customer", back_populates="event_attendances")
    event = relationship("Event", back_populates="attendances")


class CoursePurchase(Base):
    __tablename__ = "course_purchases"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    date = Column(Date, nullable=False)

    customer = relationship("Customer", back_populates="course_purchases")
    course = relationship("Course", back_populates="purchases")
