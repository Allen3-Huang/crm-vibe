from datetime import datetime
from pathlib import Path

import pandas as pd


class DataService:
    def __init__(self, data_dir: str = "../my_data"):
        self.data_dir = Path(data_dir)
        self._load_data()

    def _load_data(self):
        event_path = self.data_dir / "event_list.csv"
        course_path = self.data_dir / "course_list.csv"

        self.events_df = pd.read_csv(event_path, encoding="utf-8-sig")
        self.courses_df = pd.read_csv(course_path, encoding="utf-8-sig")

        self.events_df["date"] = pd.to_datetime(
            self.events_df["date"], format="%Y-%m-%d"
        ).dt.date
        self.courses_df["date"] = pd.to_datetime(
            self.courses_df["date"], format="%Y/%m/%d"
        ).dt.date

    def get_all_customers(self) -> list[dict]:
        event_customers = self.events_df[["email", "name"]].drop_duplicates()
        course_customers = self.courses_df[["email", "name"]].drop_duplicates()
        all_customers = pd.concat([event_customers, course_customers]).drop_duplicates(
            subset=["email"]
        )

        result = []
        for _, row in all_customers.iterrows():
            email = row["email"]
            event_count = len(self.events_df[self.events_df["email"] == email])
            course_count = len(self.courses_df[self.courses_df["email"] == email])
            result.append(
                {
                    "email": email,
                    "name": row["name"],
                    "event_count": event_count,
                    "course_count": course_count,
                }
            )

        return sorted(result, key=lambda x: x["email"])

    def get_customer_by_email(self, email: str) -> dict | None:
        event_records = self.events_df[self.events_df["email"] == email]
        course_records = self.courses_df[self.courses_df["email"] == email]

        if event_records.empty and course_records.empty:
            return None

        name = (
            event_records.iloc[0]["name"]
            if not event_records.empty
            else course_records.iloc[0]["name"]
        )

        events = [
            {
                "event_id": row["event_id"],
                "event_name": row["event_name"],
                "date": row["date"].isoformat(),
            }
            for _, row in event_records.iterrows()
        ]

        courses = [
            {
                "course_id": row["course_id"],
                "course_name": row["course_name"],
                "date": row["date"].isoformat(),
            }
            for _, row in course_records.iterrows()
        ]

        return {
            "email": email,
            "name": name,
            "events": events,
            "courses": courses,
            "event_count": len(events),
            "course_count": len(courses),
        }

    def get_all_events(self) -> list[dict]:
        event_groups = self.events_df.groupby(["event_id", "event_name"])
        result = []

        for (event_id, event_name), group in event_groups:
            attendees = [
                {"name": row["name"], "email": row["email"], "date": row["date"].isoformat()}
                for _, row in group.iterrows()
            ]
            result.append(
                {
                    "event_id": event_id,
                    "event_name": event_name,
                    "attendee_count": len(attendees),
                    "attendees": attendees,
                }
            )

        return sorted(result, key=lambda x: x["event_id"])

    def get_all_courses(self) -> list[dict]:
        course_groups = self.courses_df.groupby(["course_id", "course_name"])
        result = []

        for (course_id, course_name), group in course_groups:
            buyers = [
                {"name": row["name"], "email": row["email"], "date": row["date"].isoformat()}
                for _, row in group.iterrows()
            ]
            result.append(
                {
                    "course_id": course_id,
                    "course_name": course_name,
                    "buyer_count": len(buyers),
                    "buyers": buyers,
                }
            )

        return sorted(result, key=lambda x: x["course_id"])

    def get_analytics(self) -> dict:
        event_emails = set(self.events_df["email"].unique())
        course_emails = set(self.courses_df["email"].unique())
        all_emails = event_emails | course_emails
        converted_emails = event_emails & course_emails

        conversion_rate = (
            len(converted_emails) / len(event_emails) * 100 if event_emails else 0
        )

        event_correlations = []
        event_groups = self.events_df.groupby(["event_id", "event_name"])

        for (event_id, event_name), group in event_groups:
            attendee_emails = set(group["email"].unique())
            converted = attendee_emails & course_emails
            conv_rate = len(converted) / len(attendee_emails) * 100 if attendee_emails else 0

            course_counts = {}
            for email in converted:
                customer_courses = self.courses_df[self.courses_df["email"] == email]
                for _, row in customer_courses.iterrows():
                    course_name = row["course_name"]
                    course_counts[course_name] = course_counts.get(course_name, 0) + 1

            top_courses = [
                {"course_name": name, "count": count}
                for name, count in sorted(
                    course_counts.items(), key=lambda x: x[1], reverse=True
                )[:5]
            ]

            event_correlations.append(
                {
                    "event_id": event_id,
                    "event_name": event_name,
                    "event_attendees": len(attendee_emails),
                    "converted_to_course": len(converted),
                    "conversion_rate": round(conv_rate, 2),
                    "top_courses": top_courses,
                }
            )

        event_correlations.sort(key=lambda x: x["conversion_rate"], reverse=True)

        return {
            "total_customers": len(all_emails),
            "total_events": len(event_groups),
            "total_courses": len(self.courses_df.groupby("course_id")),
            "conversion_stats": {
                "total_event_attendees": len(event_emails),
                "total_course_buyers": len(course_emails),
                "converted_customers": len(converted_emails),
                "conversion_rate": round(conversion_rate, 2),
            },
            "event_correlations": event_correlations,
        }


data_service = DataService()
