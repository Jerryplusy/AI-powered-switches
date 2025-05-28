import httpx
from .base import BaseAdapter

class HuaweiAdapter(BaseAdapter):
    def __init__(self):
        self.client = None
        self.base_url = None

    async def connect(self, ip: str, credentials: dict):
        self.base_url = f"https://{ip}/restconf"
        self.client = httpx.AsyncClient(
            auth=(credentials['username'], credentials['password']),
            verify=False,
            timeout=30.0
        )

    async def deploy_config(self, config: dict):
        headers = {"Content-Type": "application/yang-data+json"}
        url = f"{self.base_url}/data/ietf-restconf:operations/network-topology:deploy"
        response = await self.client.post(url, json=config, headers=headers)
        response.raise_for_status()
        return response.json()

    async def disconnect(self):
        if self.client:
            await self.client.aclose()