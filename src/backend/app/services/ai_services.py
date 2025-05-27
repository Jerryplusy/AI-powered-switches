import aiohttp
import logging
from typing import Dict, Any
from src.backend.config import settings

logger = logging.getLogger(__name__)


async def call_ai_api(command: str, device_type: str, vendor: str, api_key: str) -> Dict[str, Any]:
    """
    调用硅基流动API解析中文命令

    参数:
    - command: 中文配置命令
    - device_type: 设备类型
    - vendor: 设备厂商
    - api_key: API密钥

    返回:
    - 解析后的配置和状态信息
    """
    url = settings.ai_api_url

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "command": command,
        "device_type": device_type,
        "vendor": vendor,
        "output_format": "json"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                if response.status != 200:
                    error = await response.text()
                    logger.error(f"AI API error: {error}")
                    return {
                        "success": False,
                        "message": f"AI API returned {response.status}: {error}"
                    }

                data = await response.json()
                return {
                    "success": True,
                    "config": data.get("config", {}),
                    "message": data.get("message", "Command parsed successfully")
                }

    except Exception as e:
        logger.error(f"Error calling AI API: {str(e)}")
        return {
            "success": False,
            "message": f"Error calling AI API: {str(e)}"
        }
