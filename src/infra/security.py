from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
from jose import JWTError, jwt
from fastapi import HTTPException, status

from src.settings import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
)


# 🔐 =========================
# HASH DE SENHA
# 🔐 =========================

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha plain corresponde ao hash"""
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8"),
        )
    except Exception:
        return False


def get_password_hash(password: str) -> str:
    """Gera hash da senha"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


# 🔑 =========================
# TOKENS JWT
# 🔑 =========================

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Cria access token JWT (curta duração)"""
    to_encode = data.copy()

    expire = (
        datetime.now(timezone.utc) + expires_delta
        if expires_delta
        else datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode.update({
        "exp": expire,
        "type": "access"
    })

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict) -> str:
    """Cria refresh token JWT (longa duração)"""
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update({
        "exp": expire,
        "type": "refresh"
    })

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# 🔍 =========================
# VALIDAÇÃO DE TOKENS
# 🔍 =========================

def verify_access_token(token: str) -> dict:
    """Verifica e decodifica access token JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido - não é access token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return payload

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )


def verify_refresh_token(token: str) -> dict:
    """Verifica e decodifica refresh token JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido - não é refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return payload

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )