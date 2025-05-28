from fastapi import APIRouter
from ...monitoring.healthcheck import check_redis, check_ai_service

router = APIRouter()

@router.get("/live")
async def liveness_check():
    return {"status": "alive"}

@router.get("/ready")
async def readiness_check():
    redis_ok = await check_redis()
    ai_ok = await check_ai_service()
    return {
        "redis": redis_ok,
        "ai_service": ai_ok
    }