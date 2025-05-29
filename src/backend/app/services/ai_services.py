import json
import httpx
from typing import Dict, Any
from src.backend.app.utils.exceptions import SiliconFlowAPIException


class AIService:
    def __init__(self, api_key: str, api_url: str):
        self.api_key = api_key
        self.api_url = api_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def parse_command(self, command: str) -> Dict[str, Any]:
        """
        调用硅基流动API解析中文命令
        """
        prompt = f"""
        你是一个网络设备配置专家，请将以下中文命令转换为网络设备配置JSON。
        支持的配置包括：VLAN、端口、路由、ACL等。
        返回格式必须为JSON，包含配置类型和详细参数。

        命令：{command}
        """

        data = {
            "model": "text-davinci-003",
            "prompt": prompt,
            "max_tokens": 1000,
            "temperature": 0.3
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/completions",
                    headers=self.headers,
                    json=data,
                    timeout=30
                )

                if response.status_code != 200:
                    raise SiliconFlowAPIException(response.text)

                result = response.json()
                config_str = result["choices"][0]["text"].strip()

                # 确保返回的是有效的JSON
                try:
                    config = json.loads(config_str)
                    return config
                except json.JSONDecodeError:
                    # 尝试修复可能的多余字符
                    if config_str.startswith("```json"):
                        config_str = config_str[7:-3].strip()
                        return json.loads(config_str)
                    raise SiliconFlowAPIException("Invalid JSON format returned from AI")
        except httpx.HTTPError as e:
            raise SiliconFlowAPIException(str(e))