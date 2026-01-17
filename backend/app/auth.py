import os
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from google.oauth2 import id_token
from google.auth.transport import requests
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from .database import get_db
from .models import User

# 配置
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_HOURS = 24

security = HTTPBearer()


def verify_google_token(token: str) -> dict:
    """驗證 Google ID Token 並返回用戶資訊"""
    try:
        idinfo = id_token.verify_oauth2_token(
            token, requests.Request(), GOOGLE_CLIENT_ID
        )
        return {
            "email": idinfo["email"],
            "name": idinfo.get("name", ""),
            "picture": idinfo.get("picture", ""),
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid Google token: {str(e)}",
        )


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """生成 JWT access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(hours=JWT_EXPIRE_HOURS))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """FastAPI 依賴項：從 JWT token 獲取當前用戶"""
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception

    return user


def get_or_create_user(db: Session, email: str, name: str, picture: str) -> User:
    """查找或創建用戶"""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(email=email, name=name, picture=picture)
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        # 更新用戶資訊
        user.name = name
        user.picture = picture
        db.commit()
        db.refresh(user)
    return user
