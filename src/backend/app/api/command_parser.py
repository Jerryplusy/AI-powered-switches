from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from ...config import settings
from ..services.ai_service import call_ai_api
import logging

router = APIRouter()

logger = logging.getLogger(__name__)


class CommandRequest(BaseModel):
    command: str
    device_type: Optional[str] = "switch"
    vendor: Optional[str] = "cisco"


class CommandResponse(BaseModel):
    original_command: str
    parsed_config: dict
    success: bool
    message: Optional[str] = None


@router.post("", response_model=CommandResponse)
async def parse_command(request: CommandRequest):
    """
    解析中文网络配置命令，返回JSON格式的配置

    参数:
    - command: 中文配置命令，如"创建VLAN 100，名称为财务部"
    - device_type: 设备类型，默认为switch
    - vendor: 设备厂商，默认为cisco

    返回:
    - 解析后的JSON配置
    """
    try:
        logger.info(f"Received command: {request.command}")

        # 调用AI服务解析命令
        ai_response = await call_ai_api(
            command=request.command,
            device_type=request.device_type,
            vendor=request.vendor,
            api_key=settings.ai_api_key
        )

        if not ai_response.get("success"):
            raise HTTPException(
                status_code=400,
                detail=ai_response.get("message", "Failed to parse command")
            )

        return CommandResponse(
            original_command=request.command,
            parsed_config=ai_response["config"],
            success=True,
            message="Command parsed successfully"
        )

    except Exception as e:
        logger.error(f"Error parsing command: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing command: {str(e)}"
        )