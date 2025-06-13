from fastapi import APIRouter, HTTPException
from typing import List, Dict
from pydantic import BaseModel
from ...config import settings
from ..services.network_scanner import NetworkScanner
from ..api.network_config import SwitchConfigurator, SwitchConfig

router = APIRouter(prefix="/api", tags=["API"])
scanner = NetworkScanner()


# ====================
# 请求模型
# ====================
class BatchConfigRequest(BaseModel):
    config: Dict
    switch_ips: List[str]


class CommandRequest(BaseModel):
    command: str


class ConfigRequest(BaseModel):
    config: Dict
    switch_ip: str


# ====================
# API端点
# ====================
@router.post("/batch_apply_config")
async def batch_apply_config(request: BatchConfigRequest):
    """
    批量配置交换机
    - 支持同时配置多台设备
    - 自动处理连接池
    - 返回每个设备的详细结果
    """
    configurator = SwitchConfigurator(
        username=settings.SWITCH_USERNAME,
        password=settings.SWITCH_PASSWORD,
        timeout=settings.SWITCH_TIMEOUT
    )

    results = {}
    try:
        for ip in request.switch_ips:
            try:
                # 使用公开的apply_config方法
                results[ip] = await configurator.apply_config(ip, request.config)
            except Exception as e:
                results[ip] = {
                    "status": "failed",
                    "error": str(e)
                }
        return {"results": results}
    finally:
        await configurator.close()


@router.post("/apply_config", response_model=Dict)
async def apply_config(request: ConfigRequest):
    """
    单设备配置
    - 更详细的错误处理
    - 自动备份和回滚
    """
    configurator = SwitchConfigurator(
        username=settings.SWITCH_USERNAME,
        password=settings.SWITCH_PASSWORD,
        timeout=settings.SWITCH_TIMEOUT
    )

    try:
        result = await configurator.apply_config(request.switch_ip, request.config)
        if result["status"] != "success":
            raise HTTPException(
                status_code=500,
                detail=result.get("error", "配置失败")
            )
        return result
    finally:
        await configurator.close()


# ====================
# 其他原有端点（保持不动）
# ====================
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


@router.post("/parse_command", response_model=Dict)
async def parse_command(request: CommandRequest):
    """
    解析中文命令并返回JSON配置
    - 依赖AI服务
    - 返回标准化配置
    """
    try:
        from ..services.ai_services import AIService  # 延迟导入避免循环依赖
        ai_service = AIService(settings.SILICONFLOW_API_KEY, settings.SILICONFLOW_API_URL)
        config = await ai_service.parse_command(request.command)
        return {"success": True, "config": config}
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to parse command: {str(e)}"
        )