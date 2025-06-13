import asyncio
import logging
import telnetlib3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Union

import aiofiles
import asyncssh
from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, wait_exponential


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
# 核心配置器（完整双模式）
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

    async def _apply_config(self, ip: str, config: Union[Dict, SwitchConfig]) -> str:
        """实际配置逻辑"""
        if isinstance(config, dict):
            config = SwitchConfig(**config)

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

    # --------- eNSP模式专用 ---------
    async def _send_ensp_commands(self, ip: str, commands: List[str]) -> str:
        """Telnet协议执行（eNSP）"""
        try:
            # 修复点：使用正确的timeout参数
            reader, writer = await telnetlib3.open_connection(
                host=ip,
                port=self.ensp_port,
                connect_minwait=self.timeout,  # telnetlib3的实际可用参数
                connect_maxwait=self.timeout
            )

            # 登录流程（增加超时处理）
            try:
                await asyncio.wait_for(reader.readuntil(b"Username:"), timeout=self.timeout)
                writer.write(f"{self.username}\n")

                await asyncio.wait_for(reader.readuntil(b"Password:"), timeout=self.timeout)
                writer.write(f"{self.password}\n")

                # 等待登录完成
                await asyncio.sleep(1)
            except asyncio.TimeoutError:
                raise EnspConnectionException("登录超时")

            # 执行命令
            output = ""
            for cmd in commands:
                writer.write(f"{cmd}\n")
                await writer.drain()  # 确保命令发送完成

                # 读取响应（增加超时处理）
                try:
                    while True:
                        data = await asyncio.wait_for(reader.read(1024), timeout=1)
                        if not data:
                            break
                        output += data
                except asyncio.TimeoutError:
                    continue  # 单次读取超时不视为错误

            # 关闭连接
            writer.close()
            try:
                await writer.wait_closed()
            except:
                logging.debug("连接关闭时出现异常", exc_info=True)  # 至少记录异常信息
                pass

            return output
        except Exception as e:
            raise EnspConnectionException(f"eNSP连接失败: {str(e)}")

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

    # --------- SSH模式专用（使用AsyncSSH） ---------
    async def _send_ssh_commands(self, ip: str, commands: List[str]) -> str:
        """AsyncSSH执行命令"""
        async with self.semaphore:
            try:
                async with asyncssh.connect(
                        host=ip,
                        username=self.username,
                        password=self.password,
                        connect_timeout=self.timeout,  # AsyncSSH的正确参数名
                        **self.ssh_options
                ) as conn:
                    results = []
                    for cmd in commands:
                        result = await conn.run(cmd, check=True)
                        results.append(result.stdout)
                    return "\n".join(results)
            except asyncssh.Error as e:
                raise SSHConnectionException(f"SSH操作失败: {str(e)}")
            except Exception as e:
                raise SSHConnectionException(f"连接异常: {str(e)}")

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

    # --------- 通用功能 ---------
    async def _validate_config(self, ip: str, config: SwitchConfig) -> bool:
        """验证配置是否生效"""
        current = await self._get_current_config(ip)
        if config.type == "vlan":
            return f"vlan {config.vlan_id}" in current
        elif config.type == "interface" and config.vlan:
            return f"switchport access vlan {config.vlan}" in current
        return True

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


# ----------------------
# 使用示例
# ----------------------
async def demo():
    # 示例1: eNSP设备配置（Telnet模式）
    ensp_configurator = SwitchConfigurator(
        ensp_mode=True,
        ensp_port=2000,
        username="admin",
        password="admin",
        timeout=15
    )
    ensp_result = await ensp_configurator.safe_apply("127.0.0.1", {
        "type": "interface",
        "interface": "GigabitEthernet0/0/1",
        "vlan": 100,
        "ip_address": "192.168.1.2 255.255.255.0"
    })
    print("eNSP配置结果:", ensp_result)

    # 示例2: 真实设备配置（SSH模式）
    ssh_configurator = SwitchConfigurator(
        username="cisco",
        password="cisco123",
        timeout=15
    )
    ssh_result = await ssh_configurator.safe_apply("192.168.1.1", {
        "type": "vlan",
        "vlan_id": 200,
        "name": "Production"
    })
    print("SSH配置结果:", ssh_result)


if __name__ == "__main__":
    asyncio.run(demo())