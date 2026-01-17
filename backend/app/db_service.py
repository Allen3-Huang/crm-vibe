from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models


class DBService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_customers(self) -> list[dict]:
        customers = self.db.query(models.Customer).all()
        result = []
        for c in customers:
            result.append({
                "email": c.email,
                "name": c.name,
                "event_count": len(c.event_attendances),
                "course_count": len(c.course_purchases),
            })
        return sorted(result, key=lambda x: x["email"])

    def get_customer_by_email(self, email: str) -> dict | None:
        customer = self.db.query(models.Customer).filter(
            models.Customer.email == email
        ).first()

        if not customer:
            return None

        events = [
            {
                "event_id": a.event.event_id,
                "event_name": a.event.event_name,
                "date": a.date.isoformat(),
            }
            for a in customer.event_attendances
        ]

        courses = [
            {
                "course_id": p.course.course_id,
                "course_name": p.course.course_name,
                "date": p.date.isoformat(),
            }
            for p in customer.course_purchases
        ]

        return {
            "email": customer.email,
            "name": customer.name,
            "events": events,
            "courses": courses,
            "event_count": len(events),
            "course_count": len(courses),
        }

    def get_all_events(self) -> list[dict]:
        events = self.db.query(models.Event).all()
        result = []

        for event in events:
            attendees = [
                {
                    "name": a.customer.name,
                    "email": a.customer.email,
                    "date": a.date.isoformat(),
                }
                for a in event.attendances
            ]
            result.append({
                "event_id": event.event_id,
                "event_name": event.event_name,
                "attendee_count": len(attendees),
                "attendees": attendees,
            })

        return sorted(result, key=lambda x: x["event_id"])

    def get_all_courses(self) -> list[dict]:
        courses = self.db.query(models.Course).all()
        result = []

        for course in courses:
            buyers = [
                {
                    "name": p.customer.name,
                    "email": p.customer.email,
                    "date": p.date.isoformat(),
                }
                for p in course.purchases
            ]
            result.append({
                "course_id": course.course_id,
                "course_name": course.course_name,
                "buyer_count": len(buyers),
                "buyers": buyers,
            })

        return sorted(result, key=lambda x: x["course_id"])

    def get_analytics(self) -> dict:
        # 取得有參加活動的顧客 email
        event_customers = self.db.query(models.Customer).join(
            models.EventAttendance
        ).distinct().all()
        event_emails = {c.email for c in event_customers}

        # 取得有購買課程的顧客 email
        course_customers = self.db.query(models.Customer).join(
            models.CoursePurchase
        ).distinct().all()
        course_emails = {c.email for c in course_customers}

        all_emails = event_emails | course_emails
        converted_emails = event_emails & course_emails

        conversion_rate = (
            len(converted_emails) / len(event_emails) * 100 if event_emails else 0
        )

        # 分析每個活動的轉換率
        events = self.db.query(models.Event).all()
        event_correlations = []

        for event in events:
            attendee_emails = {a.customer.email for a in event.attendances}
            converted = attendee_emails & course_emails
            conv_rate = (
                len(converted) / len(attendee_emails) * 100 if attendee_emails else 0
            )

            # 統計轉換顧客購買的課程
            course_counts: dict[str, int] = {}
            for email in converted:
                customer = self.db.query(models.Customer).filter(
                    models.Customer.email == email
                ).first()
                if customer:
                    for p in customer.course_purchases:
                        name = p.course.course_name
                        course_counts[name] = course_counts.get(name, 0) + 1

            top_courses = [
                {"course_name": name, "count": count}
                for name, count in sorted(
                    course_counts.items(), key=lambda x: x[1], reverse=True
                )[:5]
            ]

            event_correlations.append({
                "event_id": event.event_id,
                "event_name": event.event_name,
                "event_attendees": len(attendee_emails),
                "converted_to_course": len(converted),
                "conversion_rate": round(conv_rate, 2),
                "top_courses": top_courses,
            })

        event_correlations.sort(key=lambda x: x["conversion_rate"], reverse=True)

        total_events = self.db.query(models.Event).count()
        total_courses = self.db.query(models.Course).count()

        return {
            "total_customers": len(all_emails),
            "total_events": total_events,
            "total_courses": total_courses,
            "conversion_stats": {
                "total_event_attendees": len(event_emails),
                "total_course_buyers": len(course_emails),
                "converted_customers": len(converted_emails),
                "conversion_rate": round(conversion_rate, 2),
            },
            "event_correlations": event_correlations,
        }
