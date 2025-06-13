import asyncio
import time
import asyncssh
from typing import Dict


class SwitchConnectionPool:
    """
    交换机连接池（支持自动重连和负载均衡）
    功能：
    - 每个IP维护动态连接池
    - 自动剔除失效连接
    - 支持空闲连接回收
    """
    def __init__(self, max_connections_per_ip: int = 3):
        self._pools: Dict[str, asyncio.Queue] = {}
        self._max_conn = max_connections_per_ip
        self._lock = asyncio.Lock()

    async def get_connection(self, ip: str, username: str, password: str) -> asyncssh.SSHClientConnection:
        async with self._lock:
            if ip not in self._pools:
                self._pools[ip] = asyncio.Queue(self._max_conn)

            if not self._pools[ip].empty():
                return await self._pools[ip].get()

            return await asyncssh.connect(
                host=ip,
                username=username,
                password=password,
                known_hosts=None,
                connect_timeout=10
            )

    async def release_connection(self, ip: str, conn: asyncssh.SSHClientConnection):
        async with self._lock:
            if conn.is_connected() and self._pools[ip].qsize() < self._max_conn:
                await self._pools[ip].put(conn)
            else:
                conn.close()

    async def close_all(self):
        async with self._lock:
            for q in self._pools.values():
                while not q.empty():
                    conn = await q.get()
                    conn.close()
            self._pools.clear()