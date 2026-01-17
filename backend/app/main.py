import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import get_db, engine, Base
from .db_service import DBService

# 啟動時建立資料表（如果不存在）
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CRM API",
    description="顧客關係管理系統 - 追蹤活動參與與課程購買",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "https://crm-vibe.zeabur.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_service(db: Session = Depends(get_db)) -> DBService:
    return DBService(db)


@app.get("/")
def root():
    return {"message": "CRM API is running", "database": "PostgreSQL"}


@app.get("/api/customers")
def get_customers(service: DBService = Depends(get_service)):
    """取得所有顧客列表"""
    return service.get_all_customers()


@app.get("/api/customers/{email:path}")
def get_customer(email: str, service: DBService = Depends(get_service)):
    """取得單一顧客詳細資料"""
    customer = service.get_customer_by_email(email)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@app.get("/api/events")
def get_events(service: DBService = Depends(get_service)):
    """取得所有活動列表"""
    return service.get_all_events()


@app.get("/api/courses")
def get_courses(service: DBService = Depends(get_service)):
    """取得所有課程列表"""
    return service.get_all_courses()


@app.get("/api/analytics")
def get_analytics(service: DBService = Depends(get_service)):
    """取得活動與課程的關聯性分析"""
    return service.get_analytics()
