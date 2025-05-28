#连接池
# /backend/app/utils/connection_pool.py
import asyncio
from collections import deque
from ..adapters import cisco, huawei

class ConnectionPool:
    def __init__(self, max_size=10):
        self.max_size = max_size
        self.pool = deque(maxlen=max_size)
        self.lock = asyncio.Lock()

    async def get(self, vendor: str):
        async with self.lock:
            if self.pool:
                return self.pool.pop()
            return CiscoAdapter() if vendor == 'cisco' else HuaweiAdapter()

    async def release(self, adapter):
        async with self.lock:
            if len(self.pool) < self.max_size:
                self.pool.append(adapter)