import paramiko
import asyncio
from typing import Dict, Any
from ..utils.exceptions import SwitchConfigException


class SwitchConfigurator:
    def __init__(self, username: str, password: str, timeout: int = 10):
        self.username = username
        self.password = password
        self.timeout = timeout

    async def apply_config(self, switch_ip: str, config: Dict[str, Any]) -> str:
        """
        应用配置到交换机
        """
        try:
            # 根据配置类型调用不同的方法
            config_type = config.get("type", "").lower()

            if config_type == "vlan":
                return await self._configure_vlan(switch_ip, config)
            elif config_type == "interface":
                return await self._configure_interface(switch_ip, config)
            elif config_type == "acl":
                return await self._configure_acl(switch_ip, config)
            elif config_type == "route":
                return await self._configure_route(switch_ip, config)
            else:
                raise SwitchConfigException(f"Unsupported config type: {config_type}")
        except Exception as e:
            raise SwitchConfigException(str(e))

    async def _send_commands(self, switch_ip: str, commands: list) -> str:
        """
        发送命令到交换机
        """
        try:
            # 使用Paramiko建立SSH连接
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # 在异步上下文中运行阻塞操作
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                lambda: ssh.connect(
                    switch_ip,
                    username=self.username,
                    password=self.password,
                    timeout=self.timeout
                )
            )

            # 获取SSH shell
            shell = await loop.run_in_executor(None, ssh.invoke_shell)

            # 发送配置命令
            output = ""
            for cmd in commands:
                await loop.run_in_executor(None, shell.send, cmd + "\n")
                await asyncio.sleep(0.5)
                while shell.recv_ready():
                    output += (await loop.run_in_executor(None, shell.recv, 1024)).decode("utf-8")

            # 关闭连接
            await loop.run_in_executor(None, ssh.close)

            return output
        except Exception as e:
            raise SwitchConfigException(f"SSH connection failed: {str(e)}")

    async def _configure_vlan(self, switch_ip: str, config: Dict[str, Any]) -> str:
        """
        配置VLAN
        """
        vlan_id = config["vlan_id"]
        vlan_name = config.get("name", f"VLAN{vlan_id}")
        interfaces = config.get("interfaces", [])

        commands = [
            "configure terminal",
            f"vlan {vlan_id}",
            f"name {vlan_name}",
        ]

        # 配置接口
        for intf in interfaces:
            commands.extend([
                f"interface {intf['interface']}",
                f"switchport access vlan {vlan_id}",
                "exit"
            ])

        commands.append("end")

        return await self._send_commands(switch_ip, commands)

    async def _configure_interface(self, switch_ip: str, config: Dict[str, Any]) -> str:
        """
        配置接口
        """
        interface = config["interface"]
        ip_address = config.get("ip_address")
        description = config.get("description", "")
        vlan = config.get("vlan")
        state = config.get("state", "up")

        commands = [
            "configure terminal",
            f"interface {interface}",
            f"description {description}",
        ]

        if ip_address:
            commands.append(f"ip address {ip_address}")

        if vlan:
            commands.append(f"switchport access vlan {vlan}")

        if state.lower() == "up":
            commands.append("no shutdown")
        else:
            commands.append("shutdown")

        commands.extend(["exit", "end"])

        return await self._send_commands(switch_ip, commands)

    async def _configure_acl(self, switch_ip: str, config: Dict[str, Any]) -> str:
        """
        配置ACL
        """
        acl_id = config["acl_id"]
        acl_type = config.get("type", "standard")
        rules = config.get("rules", [])

        commands = ["configure terminal"]

        if acl_type == "standard":
            commands.append(f"access-list {acl_id} standard")
        else:
            commands.append(f"access-list {acl_id} extended")

        for rule in rules:
            action = rule.get("action", "permit")
            source = rule.get("source", "any")
            destination = rule.get("destination", "any")
            protocol = rule.get("protocol", "ip")

            if acl_type == "standard":
                commands.append(f"{action} {source}")
            else:
                commands.append(f"{action} {protocol} {source} {destination}")

        commands.append("end")

        return await self._send_commands(switch_ip, commands)

    async def _configure_route(self, switch_ip: str, config: Dict[str, Any]) -> str:
        """
        配置路由
        """
        network = config["network"]
        mask = config["mask"]
        next_hop = config["next_hop"]

        commands = [
            "configure terminal",
            f"ip route {network} {mask} {next_hop}",
            "end"
        ]

        return await self._send_commands(switch_ip, commands)