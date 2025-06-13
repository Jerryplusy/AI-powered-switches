import asyncio
from typing import List, Dict
from dataclasses import dataclass
from .connection_pool import SwitchConnectionPool

@dataclass
class BulkSwitchConfig:
    vlan_id: int = None
    interface: str = None
    operation: str = "create"  # 仅业务字段，无测试相关

class BulkConfigurator:
    """生产环境批量配置器（无测试代码）"""
    def __init__(self, max_concurrent: int = 50):
        self.pool = SwitchConnectionPool()
        self.semaphore = asyncio.Semaphore(max_concurrent)

    async def _configure_device(self, ip: str, config: BulkSwitchConfig) -> str:
        """核心配置方法"""
        conn = await self.pool.get_connection(ip, "admin", "admin")
        try:
            commands = self._generate_commands(config)
            results = [await conn.run(cmd) for cmd in commands]
            return "\n".join(r.stdout for r in results)
        finally:
            await self.pool.release_connection(ip, conn)

    def _generate_commands(self, config: BulkSwitchConfig) -> List[str]:
        """命令生成（纯业务逻辑）"""
        commands = []
        if config.vlan_id:
            commands.append(f"vlan {config.vlan_id}")
            if config.operation == "create":
                commands.extend([
                    f"name VLAN_{config.vlan_id}",
                    "commit"
                ])
        return commands

    async def run_bulk(self, ip_list: List[str], config: BulkSwitchConfig) -> Dict[str, str]:
        """批量执行入口"""
        tasks = {
            ip: asyncio.create_task(self._configure_device(ip, config))
            for ip in ip_list
        }
        return {ip: await task for ip, task in tasks.items()}