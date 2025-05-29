from typing import Dict, Any
from src.backend.app.services.ai_services import AIService
from src.backend.config import settings


class CommandParser:
    def __init__(self):
        self.ai_service = AIService(settings.SILICONFLOW_API_KEY, settings.SILICONFLOW_API_URL)

    async def parse(self, command: str) -> Dict[str, Any]:
        """
        解析中文命令并返回配置
        """
        # 首先尝试本地简单解析
        local_parsed = self._try_local_parse(command)
        if local_parsed:
            return local_parsed

        # 本地无法解析则调用AI服务
        return await self.ai_service.parse_command(command)

    def _try_local_parse(self, command: str) -> Dict[str, Any]:
        """
        尝试本地解析常见命令
        """
        command = command.lower().strip()

        # VLAN配置
        if "vlan" in command and "创建" in command:
            parts = command.split()
            vlan_id = next((p for p in parts if p.isdigit()), None)
            if vlan_id:
                return {
                    "type": "vlan",
                    "vlan_id": int(vlan_id),
                    "name": f"VLAN{vlan_id}",
                    "interfaces": []
                }

        # 接口配置
        if any(word in command for word in ["接口", "端口"]) and any(
                word in command for word in ["启用", "关闭", "配置"]):
            parts = command.split()
            interface = next((p for p in parts if p.startswith(("gi", "fa", "te", "eth"))), None)
            if interface:
                config = {
                    "type": "interface",
                    "interface": interface,
                    "state": "up" if "启用" in command else "down"
                }

                if "ip" in command and "地址" in command:
                    ip_part = next((p for p in parts if "." in p and p.count(".") == 3), None)
                    if ip_part:
                        config["ip_address"] = ip_part

                if "描述" in command:
                    desc_start = command.find("描述") + 2
                    description = command[desc_start:].strip()
                    config["description"] = description

                if "vlan" in command:
                    vlan_id = next((p for p in parts if p.isdigit()), None)
                    if vlan_id:
                        config["vlan"] = int(vlan_id)

                return config

        return None