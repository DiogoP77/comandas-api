from fastapi import APIRouter, HTTPException, status
from sqlalchemy import text
from datetime import datetime, timezone
import psutil

from infra.database import get_db
from infra.orm.FuncionarioModel import FuncionarioDB

router = APIRouter()


# 🔎 BASIC HEALTH
@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": "comandas-api",
        "version": "1.0.0"
    }


# 🗄️ DATABASE HEALTH
@router.get("/health/database")
async def database_health():
    db = next(get_db())
    try:
        result = db.execute(text("SELECT 1")).fetchone()

        if result and result[0] == 1:
            return {
                "status": "healthy",
                "database": "connected",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }

        raise HTTPException(503, "Database query failed")

    except Exception as e:
        raise HTTPException(503, f"Database unavailable: {str(e)}")

    finally:
        db.close()


# 📊 TABLES HEALTH
@router.get("/health/database/tables")
async def database_tables_health():
    db = next(get_db())

    try:
        checks = {}

        # Funcionários
        try:
            count = db.query(FuncionarioDB).count()
            checks["funcionarios"] = {
                "status": "healthy",
                "count": count
            }
        except Exception as e:
            checks["funcionarios"] = {
                "status": "error",
                "error": str(e)
            }

        all_healthy = all(c["status"] == "healthy" for c in checks.values())

        return {
            "status": "healthy" if all_healthy else "unhealthy",
            "tables": checks,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    except Exception as e:
        raise HTTPException(503, f"Tables check failed: {str(e)}")

    finally:
        db.close()


# 🖥️ SYSTEM HEALTH
@router.get("/health/system")
async def system_health():
    try:
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage(".")
        cpu = psutil.cpu_percent(interval=1)

        memory_info = {
            "percent": memory.percent,
            "status": "healthy" if memory.percent < 90 else "warning"
        }

        disk_percent = (disk.used / disk.total) * 100
        disk_info = {
            "percent": disk_percent,
            "status": "healthy" if disk_percent < 90 else "warning"
        }

        cpu_info = {
            "percent": cpu,
            "status": "healthy" if cpu < 80 else "warning"
        }

        overall = all([
            memory_info["status"] == "healthy",
            disk_info["status"] == "healthy",
            cpu_info["status"] == "healthy"
        ])

        return {
            "status": "healthy" if overall else "warning",
            "memory": memory_info,
            "disk": disk_info,
            "cpu": cpu_info,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    except Exception as e:
        raise HTTPException(503, f"System health failed: {str(e)}")


# 🔥 FULL HEALTH
@router.get("/health/full")
async def full_health_check():
    checks = {}

    # API
    checks["api"] = {"status": "healthy"}

    # DB
    try:
        db = next(get_db())
        db.execute(text("SELECT 1"))
        db.close()
        checks["database"] = {"status": "healthy"}
    except Exception as e:
        checks["database"] = {"status": "unhealthy", "error": str(e)}

    # SYSTEM
    try:
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage(".")
        cpu = psutil.cpu_percent(interval=1)

        ok = (
            memory.percent < 90 and
            (disk.used / disk.total) < 0.9 and
            cpu < 80
        )

        checks["system"] = {
            "status": "healthy" if ok else "warning"
        }

    except Exception as e:
        checks["system"] = {"status": "error", "error": str(e)}

    # OVERALL
    overall = "healthy"
    for c in checks.values():
        if c["status"] in ["unhealthy", "error"]:
            overall = "unhealthy"
            break
        elif c["status"] == "warning":
            overall = "warning"

    return {
        "status": overall,
        "checks": checks,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


# 🚀 READINESS
@router.get("/ready")
async def readiness_check():
    try:
        db = next(get_db())
        db.execute(text("SELECT 1"))
        db.close()
    except Exception as e:
        raise HTTPException(503, f"Not ready: {str(e)}")

    return {
        "status": "ready",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


# ❤️ LIVENESS
@router.get("/live")
async def liveness_check():
    return {
        "status": "alive",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }