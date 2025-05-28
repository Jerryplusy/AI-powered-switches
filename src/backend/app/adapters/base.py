# /backend/app/adapters/base.py
from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAdapter(ABC):
    @abstractmethod
    async def connect(self, ip: str, credentials: Dict[str, str]):
        pass

    @abstractmethod
    async def deploy_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def get_status(self) -> Dict[str, Any]:
        pass
