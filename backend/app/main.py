import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .database import get_db, engine, Base
from .db_service import DBService
from .models import User
from .auth import (
    verify_google_token,
    create_access_token,
    get_current_user,
    get_customer_admin_user,
    get_or_create_user,
)

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


# ============ 認證相關 API ============


class GoogleLoginRequest(BaseModel):
    token: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


@app.post("/api/auth/google", response_model=AuthResponse)
def google_login(request: GoogleLoginRequest, db: Session = Depends(get_db)):
    """Google OAuth 登入"""
    # 驗證 Google token
    google_user = verify_google_token(request.token)

    # 查找或創建用戶
    user = get_or_create_user(
        db=db,
        email=google_user["email"],
        name=google_user["name"],
        picture=google_user["picture"],
    )

    # 生成 JWT token
    access_token = create_access_token(data={"sub": user.email})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "picture": user.picture,
        },
    }


@app.get("/api/auth/me")
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """獲取當前登入用戶資訊"""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
        "picture": current_user.picture,
    }


# ============ 公開 API ============


@app.get("/")
def root():
    return {"message": "CRM API is running", "database": "PostgreSQL"}


# ============ 受保護的 API ============


@app.get("/api/customers")
def get_customers(
    service: DBService = Depends(get_service),
    current_user: User = Depends(get_customer_admin_user),
):
    """取得所有顧客列表（僅限授權用戶）"""
    return service.get_all_customers()


@app.get("/api/customers/{email:path}")
def get_customer(
    email: str,
    service: DBService = Depends(get_service),
    current_user: User = Depends(get_customer_admin_user),
):
    """取得單一顧客詳細資料（僅限授權用戶）"""
    customer = service.get_customer_by_email(email)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@app.get("/api/events")
def get_events(
    service: DBService = Depends(get_service),
    current_user: User = Depends(get_current_user),
):
    """取得所有活動列表"""
    return service.get_all_events()


@app.get("/api/courses")
def get_courses(
    service: DBService = Depends(get_service),
    current_user: User = Depends(get_current_user),
):
    """取得所有課程列表"""
    return service.get_all_courses()


@app.get("/api/analytics")
def get_analytics(
    service: DBService = Depends(get_service),
    current_user: User = Depends(get_current_user),
):
    """取得活動與課程的關聯性分析"""
    return service.get_analytics()
