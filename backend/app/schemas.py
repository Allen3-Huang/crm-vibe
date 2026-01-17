from datetime import date
from pydantic import BaseModel


class EventAttendance(BaseModel):
    event_id: str
    event_name: str
    date: date


class CoursePurchase(BaseModel):
    course_id: str
    course_name: str
    date: date


class Customer(BaseModel):
    email: str
    name: str
    events: list[EventAttendance]
    courses: list[CoursePurchase]
    event_count: int
    course_count: int


class CustomerSummary(BaseModel):
    email: str
    name: str
    event_count: int
    course_count: int


class Event(BaseModel):
    event_id: str
    event_name: str
    attendee_count: int
    attendees: list[dict]


class Course(BaseModel):
    course_id: str
    course_name: str
    buyer_count: int
    buyers: list[dict]


class ConversionStats(BaseModel):
    total_event_attendees: int
    total_course_buyers: int
    converted_customers: int
    conversion_rate: float


class EventCourseCorrelation(BaseModel):
    event_id: str
    event_name: str
    event_attendees: int
    converted_to_course: int
    conversion_rate: float
    top_courses: list[dict]


class AnalyticsSummary(BaseModel):
    total_customers: int
    total_events: int
    total_courses: int
    conversion_stats: ConversionStats
    event_correlations: list[EventCourseCorrelation]
