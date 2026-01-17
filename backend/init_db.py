"""初始化資料庫並匯入 CSV 資料"""
from datetime import datetime
from pathlib import Path

import pandas as pd

from app.database import engine, SessionLocal, Base
from app.models import Customer, Event, Course, EventAttendance, CoursePurchase


def init_database():
    """建立資料表"""
    Base.metadata.create_all(bind=engine)
    print("資料表建立完成")


def import_data(data_dir: str = "../my_data"):
    """從 CSV 匯入資料到資料庫"""
    data_path = Path(data_dir)
    db = SessionLocal()

    try:
        # 讀取 CSV
        events_df = pd.read_csv(data_path / "event_list.csv", encoding="utf-8-sig")
        courses_df = pd.read_csv(data_path / "course_list.csv", encoding="utf-8-sig")

        events_df["date"] = pd.to_datetime(events_df["date"], format="%Y-%m-%d").dt.date
        courses_df["date"] = pd.to_datetime(courses_df["date"], format="%Y/%m/%d").dt.date

        # 建立顧客 (從兩個來源合併)
        all_customers = {}
        for _, row in events_df.iterrows():
            all_customers[row["email"]] = row["name"]
        for _, row in courses_df.iterrows():
            if row["email"] not in all_customers:
                all_customers[row["email"]] = row["name"]

        customer_map = {}
        for email, name in all_customers.items():
            customer = Customer(email=email, name=name)
            db.add(customer)
            db.flush()
            customer_map[email] = customer.id

        print(f"匯入 {len(customer_map)} 位顧客")

        # 建立活動
        event_map = {}
        unique_events = events_df[["event_id", "event_name"]].drop_duplicates()
        for _, row in unique_events.iterrows():
            event = Event(event_id=row["event_id"], event_name=row["event_name"])
            db.add(event)
            db.flush()
            event_map[row["event_id"]] = event.id

        print(f"匯入 {len(event_map)} 個活動")

        # 建立課程
        course_map = {}
        unique_courses = courses_df[["course_id", "course_name"]].drop_duplicates()
        for _, row in unique_courses.iterrows():
            course = Course(course_id=row["course_id"], course_name=row["course_name"])
            db.add(course)
            db.flush()
            course_map[row["course_id"]] = course.id

        print(f"匯入 {len(course_map)} 個課程")

        # 建立活動參加紀錄
        attendance_count = 0
        for _, row in events_df.iterrows():
            attendance = EventAttendance(
                customer_id=customer_map[row["email"]],
                event_id=event_map[row["event_id"]],
                date=row["date"],
            )
            db.add(attendance)
            attendance_count += 1

        print(f"匯入 {attendance_count} 筆活動參加紀錄")

        # 建立課程購買紀錄
        purchase_count = 0
        for _, row in courses_df.iterrows():
            purchase = CoursePurchase(
                customer_id=customer_map[row["email"]],
                course_id=course_map[row["course_id"]],
                date=row["date"],
            )
            db.add(purchase)
            purchase_count += 1

        print(f"匯入 {purchase_count} 筆課程購買紀錄")

        db.commit()
        print("資料匯入完成！")

    except Exception as e:
        db.rollback()
        print(f"匯入失敗: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("初始化資料庫...")
    init_database()
    print("\n匯入資料...")
    import_data()
