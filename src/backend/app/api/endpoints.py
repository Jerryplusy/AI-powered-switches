from fastapi import APIRouter, Depends, HTTPException
from typing import Any
from pydantic import BaseModel

from src.backend.app.services.ai_services import AIService
from src.backend.app.api.network_config import SwitchConfigurator
from src.backend.config import settings

router = APIRouter(prefix="/api", tags=["API"])

@router.get("/test")
async def test_endpoint():
    return {"message": "Hello World"}

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