import nmap
import json
from pathlib import Path
from typing import List, Dict
from ..utils.logger import logger
import os

class NetworkScanner:
    def __init__(self, cache_path: str = "switch_devices.json"):
        self.cache_path = Path(cache_path)
        os.environ["PATH"] += r";D:\Program Files\Nmap"
        self.nm = nmap.PortScanner()

    def scan_subnet(self, subnet: str = "192.168.1.0/24") -> List[Dict]:
        """扫描指定子网的交换机设备"""
        logger.info(f"Scanning subnet: {subnet}")

        # 扫描开放22(SSH)或23(Telnet)端口的设备
        self.nm.scan(
            hosts=subnet,
            arguments="-p 22,23 --open -T4"
        )

        devices = []
        for host in self.nm.all_hosts():
            if self.nm[host].state() == "up":
                device = {
                    "ip": host,
                    "ports": list(self.nm[host]["tcp"].keys()),
                    "mac": self.nm[host].get("addresses", {}).get("mac", "unknown")
                }
                devices.append(device)
                logger.debug(f"Found device: {device}")

        self._save_to_cache(devices)
        return devices

    def _save_to_cache(self, devices: List[Dict]):
        """保存扫描结果到本地文件"""
        with open(self.cache_path, "w") as f:
            json.dump(devices, f, indent=2)
        logger.info(f"Saved {len(devices)} devices to cache")

    def load_cached_devices(self) -> List[Dict]:
        """从缓存加载设备列表"""
        if not self.cache_path.exists():
            return []

        with open(self.cache_path) as f:
            return json.load(f)