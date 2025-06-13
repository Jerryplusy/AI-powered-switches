import asyncio
import logging
import telnetlib3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Union
from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, wait_exponential
import aiofiles
import asyncssh


# ----------------------
# 数据模型
# ----------------------
class SwitchConfig(BaseModel):
    type: str  # vlan/interface/acl/route
    vlan_id: Optional[int] = None
    interface: Optional[str] = None
    name: Optional[str] = None
    ip_address: Optional[str] = None
    vlan: Optional[int] = None  # 兼容eNSP模式


# ----------------------
# 异常类
# ----------------------
class SwitchConfigException(Exception):
    pass


class EnspConnectionException(SwitchConfigException):
    pass


class SSHConnectionException(SwitchConfigException):
    pass


# ----------------------
# 核心配置器
# ----------------------
class SwitchConfigurator:
    def __init__(
            self,
            username: str = "admin",
            password: str = "admin",
            timeout: int = 10,
            max_workers: int = 5,
            ensp_mode: bool = False,
            ensp_port: int = 2000,
            ensp_command_delay: float = 0.5,
            **ssh_options
    ):
        self.username = username
        self.password = password
        self.timeout = timeout
        self.semaphore = asyncio.Semaphore(max_workers)
        self.backup_dir = Path("config_backups")
        self.backup_dir.mkdir(exist_ok=True)
        self.ensp_mode = ensp_mode
        self.ensp_port = ensp_port
        self.ensp_delay = ensp_command_delay
        self.ssh_options = ssh_options
        self._connection_pool = {}  # SSH连接池

    # ====================
    # 公开API方法
    # ====================
    async def apply_config(self, ip: str, config: Union[Dict, SwitchConfig]) -> Dict:
        """
        应用配置到交换机（主入口）
        返回格式:
        {
            "status": "success"|"failed",
            "output": str,
            "backup_path": str,
            "error": Optional[str],
            "timestamp": str
        }
        """
        if isinstance(config, dict):
            config = SwitchConfig(**config)

        result = await self.safe_apply(ip, config)
        result["timestamp"] = datetime.now().isoformat()
        return result

    # ====================
    # 内部实现方法
    # ====================
    async def _apply_config(self, ip: str, config: SwitchConfig) -> str:
        """实际配置逻辑"""
        commands = (
            self._generate_ensp_commands(config)
            if self.ensp_mode
            else self._generate_standard_commands(config)
        )
        return await self._send_commands(ip, commands)

    async def _send_commands(self, ip: str, commands: List[str]) -> str:
        """双模式命令发送"""
        return (
            await self._send_ensp_commands(ip, commands)
            if self.ensp_mode
            else await self._send_ssh_commands(ip, commands)
        )

    async def _send_ensp_commands(self, ip: str, commands: List[str]) -> str:
        """Telnet协议执行（eNSP）"""
        try:
            reader, writer = await telnetlib3.open_connection(
                host=ip,
                port=self.ensp_port,
                connect_minwait=self.timeout,
                connect_maxwait=self.timeout
            )

            # 登录流程
            await reader.readuntil(b"Username:")
            writer.write(f"{self.username}\n")
            await reader.readuntil(b"Password:")
            writer.write(f"{self.password}\n")
            await asyncio.sleep(1)

            # 执行命令
            output = ""
            for cmd in commands:
                writer.write(f"{cmd}\n")
                await asyncio.sleep(self.ensp_delay)
                while True:
                    try:
                        data = await asyncio.wait_for(reader.read(1024), timeout=1)
                        if not data:
                            break
                        output += data
                    except asyncio.TimeoutError:
                        break

            writer.close()
            return output
        except Exception as e:
            raise EnspConnectionException(f"eNSP连接失败: {str(e)}")

    async def _send_ssh_commands(self, ip: str, commands: List[str]) -> str:
        """SSH协议执行"""
        async with self.semaphore:
            try:
                if ip not in self._connection_pool:
                    self._connection_pool[ip] = await asyncssh.connect(
                        host=ip,
                        username=self.username,
                        password=self.password,
                        connect_timeout=self.timeout,
                        **self.ssh_options
                    )

                results = []
                for cmd in commands:
                    result = await self._connection_pool[ip].run(cmd)
                    results.append(result.stdout)
                return "\n".join(results)
            except asyncssh.Error as e:
                if ip in self._connection_pool:
                    self._connection_pool[ip].close()
                    del self._connection_pool[ip]
                raise SSHConnectionException(f"SSH操作失败: {str(e)}")

    @staticmethod
    def _generate_ensp_commands(config: SwitchConfig) -> List[str]:
        """生成eNSP命令序列"""
        commands = ["system-view"]
        if config.type == "vlan":
            commands.extend([
                f"vlan {config.vlan_id}",
                f"description {config.name or ''}"
            ])
        elif config.type == "interface":
            commands.extend([
                f"interface {config.interface}",
                "port link-type access",
                f"port default vlan {config.vlan}" if config.vlan else "",
                f"ip address {config.ip_address}" if config.ip_address else ""
            ])
        commands.append("return")
        return [c for c in commands if c.strip()]

    @staticmethod
    def _generate_standard_commands(config: SwitchConfig) -> List[str]:
        """生成标准CLI命令"""
        commands = []
        if config.type == "vlan":
            commands.extend([
                f"vlan {config.vlan_id}",
                f"name {config.name or ''}"
            ])
        elif config.type == "interface":
            commands.extend([
                f"interface {config.interface}",
                f"switchport access vlan {config.vlan}" if config.vlan else "",
                f"ip address {config.ip_address}" if config.ip_address else ""
            ])
        return commands

    async def _get_current_config(self, ip: str) -> str:
        """获取当前配置"""
        commands = (
            ["display current-configuration"]
            if self.ensp_mode
            else ["show running-config"]
        )
        try:
            return await self._send_commands(ip, commands)
        except (EnspConnectionException, SSHConnectionException) as e:
            raise SwitchConfigException(f"配置获取失败: {str(e)}")

    async def _backup_config(self, ip: str) -> Path:
        """备份配置到文件"""
        backup_path = self.backup_dir / f"{ip}_{datetime.now().isoformat()}.cfg"
        config = await self._get_current_config(ip)
        async with aiofiles.open(backup_path, "w") as f:
            await f.write(config)
        return backup_path

    async def _restore_config(self, ip: str, backup_path: Path) -> bool:
        """从备份恢复配置"""
        try:
            async with aiofiles.open(backup_path) as f:
                config = await f.read()
            commands = (
                ["system-view", config, "return"]
                if self.ensp_mode
                else [f"configure terminal\n{config}\nend"]
            )
            await self._send_commands(ip, commands)
            return True
        except Exception as e:
            logging.error(f"恢复失败: {str(e)}")
            return False

    @retry(
        stop=stop_after_attempt(2),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def safe_apply(
            self,
            ip: str,
            config: Union[Dict, SwitchConfig]
    ) -> Dict[str, Union[str, bool, Path]]:
        """安全配置应用（自动回滚）"""
        backup_path = await self._backup_config(ip)
        try:
            result = await self._apply_config(ip, config)
            if not await self._validate_config(ip, config):
                raise SwitchConfigException("配置验证失败")
            return {
                "status": "success",
                "output": result,
                "backup_path": str(backup_path)
            }
        except (EnspConnectionException, SSHConnectionException, SwitchConfigException) as e:
            restore_status = await self._restore_config(ip, backup_path)
            return {
                "status": "failed",
                "error": str(e),
                "backup_path": str(backup_path),
                "restore_success": restore_status
            }

    async def _validate_config(self, ip: str, config: SwitchConfig) -> bool:
        """验证配置是否生效"""
        current = await self._get_current_config(ip)
        if config.type == "vlan":
            return f"vlan {config.vlan_id}" in current
        elif config.type == "interface" and config.vlan:
            return f"switchport access vlan {config.vlan}" in current
        return True

    async def close(self):
        """清理所有连接"""
        for conn in self._connection_pool.values():
            conn.close()
        self._connection_pool.clear()