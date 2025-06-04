import paramiko
import asyncio
from typing import Dict, List, Optional, Union
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from pydantic import BaseModel
import logging


# ----------------------
# 数据模型定义
# ----------------------
class SwitchConfig(BaseModel):
    """交换机配置模型"""
    type: str  # vlan/interface/acl/route
    vlan_id: Optional[int] = None
    interface: Optional[str] = None
    name: Optional[str] = None
    ip_address: Optional[str] = None
    acl_id: Optional[int] = None
    rules: Optional[List[Dict]] = None


# ----------------------
# 异常类
# ----------------------
class SwitchConfigException(Exception):
    """交换机配置异常基类"""
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
            is_emulated: bool = False,
            emulated_delay: float = 2.0
    ):
        """
        初始化配置器

        :param username: 登录用户名
        :param password: 登录密码
        :param timeout: SSH超时时间(秒)
        :param max_workers: 最大并发数
        :param is_emulated: 是否模拟器环境
        :param emulated_delay: 模拟器命令间隔延迟(秒)
        """
        self.username = username
        self.password = password
        self.timeout = timeout
        self.is_emulated = is_emulated
        self.emulated_delay = emulated_delay
        self.semaphore = asyncio.Semaphore(max_workers)
        self.logger = logging.getLogger(__name__)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(SwitchConfigException)
    )
    async def safe_apply(self, ip: str, config: Union[Dict, SwitchConfig]) -> str:
        """安全执行配置（带重试机制）"""
        async with self.semaphore:
            return await self.apply_config(ip, config)

    async def batch_configure(
            self,
            config: Union[Dict, SwitchConfig],
            ips: List[str]
    ) -> Dict[str, Union[str, Exception]]:
        """批量配置多台设备"""
        tasks = [self.safe_apply(ip, config) for ip in ips]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return {ip: result for ip, result in zip(ips, results)}

    async def apply_config(
            self,
            switch_ip: str,
            config: Union[Dict, SwitchConfig]
    ) -> str:
        """应用配置到单台设备"""
        try:
            if isinstance(config, dict):
                config = SwitchConfig(**config)

            config_type = config.type.lower()
            if config_type == "vlan":
                return await self._configure_vlan(switch_ip, config)
            elif config_type == "interface":
                return await self._configure_interface(switch_ip, config)
            elif config_type == "acl":
                return await self._configure_acl(switch_ip, config)
            elif config_type == "route":
                return await self._configure_route(switch_ip, config)
            else:
                raise SwitchConfigException(f"不支持的配置类型: {config_type}")
        except Exception as e:
            self.logger.error(f"{switch_ip} 配置失败: {str(e)}")
            raise SwitchConfigException(str(e))

    # ----------------------
    # 协议实现
    # ----------------------
    async def _send_commands(self, ip: str, commands: List[str]) -> str:
        """发送命令到设备（自动适配模拟器）"""
        try:
            # 自动选择凭证
            username, password = (
                ("admin", "Admin@123") if self.is_emulated
                else (self.username, self.password)
            )

            # 自动调整超时
            timeout = 15 if self.is_emulated else self.timeout

            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                lambda: ssh.connect(
                    ip,
                    username=username,
                    password=password,
                    timeout=timeout,
                    look_for_keys=False
                )
            )

            # 执行命令
            shell = ssh.invoke_shell()
            output = ""
            for cmd in commands:
                shell.send(cmd + "\n")
                if self.is_emulated:
                    await asyncio.sleep(self.emulated_delay)
                while shell.recv_ready():
                    recv = await loop.run_in_executor(None, shell.recv, 1024)
                    output += recv.decode("gbk" if self.is_emulated else "utf-8")

            ssh.close()
            return output
        except Exception as e:
            raise SwitchConfigException(f"SSH连接错误: {str(e)}")

    async def _configure_vlan(self, ip: str, config: SwitchConfig) -> str:
        """配置VLAN（自动适配语法）"""
        commands = [
            "system-view" if self.is_emulated else "configure terminal",
            f"vlan {config.vlan_id}",
            f"name {config.name or ''}"
        ]

        # 端口加入VLAN
        for intf in getattr(config, "interfaces", []):
            if self.is_emulated:
                commands.extend([
                    f"interface {intf['interface']}",
                    "port link-type access",
                    f"port default vlan {config.vlan_id}",
                    "quit"
                ])
            else:
                commands.extend([
                    f"interface {intf['interface']}",
                    f"switchport access vlan {config.vlan_id}",
                    "exit"
                ])

        commands.append("return" if self.is_emulated else "end")
        return await self._send_commands(ip, commands)

    async def _configure_interface(self, ip: str, config: SwitchConfig) -> str:
        """配置接口"""
        commands = [
            "system-view" if self.is_emulated else "configure terminal",
            f"interface {config.interface}",
            f"description {config.description or ''}"
        ]

        if config.ip_address:
            commands.append(f"ip address {config.ip_address}")

        if hasattr(config, "vlan"):
            if self.is_emulated:
                commands.extend([
                    "port link-type access",
                    f"port default vlan {config.vlan}"
                ])
            else:
                commands.append(f"switchport access vlan {config.vlan}")

        state = getattr(config, "state", "up")
        commands.append("undo shutdown" if state == "up" else "shutdown")
        commands.append("return" if self.is_emulated else "end")

        return await self._send_commands(ip, commands)

    async def _configure_acl(self, ip: str, config: SwitchConfig) -> str:
        """配置ACL"""
        commands = ["system-view" if self.is_emulated else "configure terminal"]

        if self.is_emulated:
            commands.append(f"acl number {config.acl_id}")
            for rule in config.rules or []:
                commands.append(
                    f"rule {'permit' if rule.get('action') == 'permit' else 'deny'} "
                    f"{rule.get('source', 'any')} {rule.get('destination', 'any')}"
                )
        else:
            commands.append(f"access-list {config.acl_id} extended")
            for rule in config.rules or []:
                commands.append(
                    f"{rule.get('action', 'permit')} {rule.get('protocol', 'ip')} "
                    f"{rule.get('source', 'any')} {rule.get('destination', 'any')}"
                )

        commands.append("return" if self.is_emulated else "end")
        return await self._send_commands(ip, commands)

    async def _configure_route(self, ip: str, config: SwitchConfig) -> str:
        """配置路由"""
        commands = [
            "system-view" if self.is_emulated else "configure terminal",
            f"ip route-static {config.network} {config.mask} {config.next_hop}",
            "return" if self.is_emulated else "end"
        ]
        return await self._send_commands(ip, commands)


# ----------------------
# 使用示例
# ----------------------
async def main():
    # eNSP模拟环境配置
    ens_configurator = SwitchConfigurator(is_emulated=True)
    await ens_configurator.batch_configure(
        {
            "type": "vlan",
            "vlan_id": 100,
            "name": "TestVLAN",
            "interfaces": [{"interface": "GigabitEthernet0/0/1"}]
        },
        ["192.168.1.200"]  # eNSP设备IP
    )

    # 真实设备配置
    real_configurator = SwitchConfigurator(
        username="real_admin",
        password="SecurePass123!",
        is_emulated=False
    )
    await real_configurator.batch_configure(
        {
            "type": "interface",
            "interface": "Gi1/0/24",
            "description": "Uplink",
            "state": "up"
        },
        ["10.1.1.1"]  # 真实设备IP
    )


if __name__ == "__main__":
    asyncio.run(main())