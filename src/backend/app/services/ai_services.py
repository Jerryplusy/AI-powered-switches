# 调用api
import requests
import json
from ...config import Config
from ...exceptions import AIServiceError


def get_network_config(command: str) -> list:
    """调用AI服务生成配置"""
    headers = {
        "Authorization": f"Bearer {Config.AI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "command": command,
        "vendor": "cisco",
        "strict_mode": True
    }

    try:
        response = requests.post(
            Config.AI_API_ENDPOINT,
            headers=headers,
            json=payload,
            timeout=8
        )
        response.raise_for_status()

        result = response.json()
        if not result.get('success'):
            raise AIServiceError(result.get('message', 'AI服务返回错误'))

        return result['config']

    except requests.exceptions.Timeout:
        raise AIServiceError("AI服务响应超时")
    except requests.exceptions.RequestException as e:
        raise AIServiceError(f"API请求失败: {str(e)}")


# --------------- backend/config.py ---------------
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # 应用配置
    ENV = os.getenv("FLASK_ENV", "production")
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")

    # AI服务配置
    AI_API_KEY = os.getenv("AI_API_KEY", "")
    AI_API_ENDPOINT = os.getenv("AI_API_ENDPOINT", "https://api.siliconflow.ai/v1/network")

    # 网络设备配置
    SWITCH_USERNAME = os.getenv("SWITCH_USER", "admin")
    SWITCH_PASSWORD = os.getenv("SWITCH_PASS", "Cisco123!")
    DEFAULT_DEVICE_IP = os.getenv("DEFAULT_DEVICE_IP", "192.168.1.1")