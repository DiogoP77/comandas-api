from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import datetime, timezone
import psutil

from src.infra.database import get_db

router = APIRouter(
    prefix="/health",
    tags=["Health"]
)


# ==============================
# 🟢 HEALTH GERAL
# ==============================
@router.get("/")
async def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


# ==============================
# 🗄️ HEALTH DATABASE
# ==============================
@router.get("/database")
async def database_health(
    db: Session = Depends(get_db)
):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "healthy"}
    except Exception:
        raise HTTPException(status_code=503, detail="Database error")


# ==============================
# 💻 HEALTH SISTEMA
# ==============================
@router.get("/system")
async def system_health():
    memory = psutil.virtual_memory().percent
    cpu = psutil.cpu_percent()

    return {
        "memory": memory,
        "cpu": cpu,
        "status": "healthy" if memory < 90 and cpu < 80 else "warning"
    }