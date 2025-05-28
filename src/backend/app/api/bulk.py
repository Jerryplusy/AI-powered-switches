from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List
from app.services.batch import BatchService
from app.utils.decorators import async_retry

router = APIRouter()

class BulkDeviceConfig(BaseModel):
    device_ips: List[str]
    config: dict
    credentials: dict
    vendor: str = "cisco"
    timeout: int = 30

@router.post("/config")
@async_retry(max_attempts=3, delay=1)
async def bulk_apply_config(request: BulkDeviceConfig, bg_tasks: BackgroundTasks):
    """
    批量配置设备接口
    示例请求体:
    {
        "device_ips": ["192.168.1.1", "192.168.1.2"],
        "config": {"vlans": [{"id": 100, "name": "test"}]},
        "credentials": {"username": "admin", "password": "secret"},
        "vendor": "cisco"
    }
    """
    devices = [{
        "ip": ip,
        "credentials": request.credentials,
        "vendor": request.vendor
    } for ip in request.device_ips]

    try:
        batch = BatchService()
        bg_tasks.add_task(batch.deploy_batch, devices, request.config)
        return {"message": "Batch job started", "device_count": len(devices)}
    except Exception as e:
        raise HTTPException(500, detail=str(e))