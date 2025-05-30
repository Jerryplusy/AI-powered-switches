from fastapi import APIRouter, Depends, HTTPException
from typing import Any
from pydantic import BaseModel

from ...app.services.ai_services import AIService
from ...app.api.network_config import SwitchConfigurator
from ...config import settings
from ..services.network_scanner import NetworkScanner

router = APIRouter(prefix="/api", tags=["API"])
scanner = NetworkScanner()

@router.get("/test")
async def test_endpoint():
    return {"message": "Hello World"}

@router.get("/scan_network", summary="扫描网络中的交换机")
async def scan_network(subnet: str = "192.168.1.0/24"):
    try:
        devices = scanner.scan_subnet(subnet)
        return {
            "success": True,
            "devices": devices,
            "count": len(devices)
        }
    except Exception as e:
        raise HTTPException(500, f"扫描失败: {str(e)}")

@router.get("/list_devices", summary="列出已发现的交换机")
async def list_devices():
    return {
        "devices": scanner.load_cached_devices()
    }

class CommandRequest(BaseModel):
    command: str

class ConfigRequest(BaseModel):
    config: dict
    switch_ip: str

@router.post("/parse_command", response_model=dict)
async def parse_command(request: CommandRequest):
    """
    解析中文命令并返回JSON配置
    """
    try:
        ai_service = AIService(settings.SILICONFLOW_API_KEY, settings.SILICONFLOW_API_URL)
        config = await ai_service.parse_command(request.command)
        return {"success": True, "config": config}
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to parse command: {str(e)}"
        )

@router.post("/apply_config", response_model=dict)
async def apply_config(request: ConfigRequest):
    """
    应用配置到交换机
    """
    try:
        configurator = SwitchConfigurator(
            username=settings.SWITCH_USERNAME,
            password=settings.SWITCH_PASSWORD,
            timeout=settings.SWITCH_TIMEOUT
        )
        result = await configurator.apply_config(request.switch_ip, request.config)
        return {"success": True, "result": result}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to apply config: {str(e)}"
        )