import asyncio
from typing import List, Dict, Any
from app.adapters.factory import AdapterFactory
from app.utils.connection_pool import ConnectionPool
from app.monitoring.metrics import (
    DEVICE_CONNECTIONS,
    CONFIG_APPLY_TIME,
    CONFIG_ERRORS
)


class BatchService:
    def __init__(self, max_workers: int = 10):
        self.semaphore = asyncio.Semaphore(max_workers)
        self.pool = ConnectionPool()

    @CONFIG_APPLY_TIME.time()
    async def deploy_batch(self, devices: List[Dict], config: Dict[str, Any]):
        async def _deploy(device):
            vendor = device.get('vendor', 'cisco')
            async with self.semaphore:
                try:
                    adapter = AdapterFactory.get_adapter(vendor)
                    await adapter.connect(device['ip'], device['credentials'])
                    DEVICE_CONNECTIONS.labels(vendor).inc()

                    result = await adapter.deploy_config(config)
                    return {
                        "device": device['ip'],
                        "status": "success",
                        "result": result
                    }
                except ConnectionError as e:
                    CONFIG_ERRORS.labels("connection").inc()
                    return {
                        "device": device['ip'],
                        "status": "failed",
                        "error": str(e)
                    }
                finally:
                    if adapter:
                        await adapter.disconnect()
                        DEVICE_CONNECTIONS.labels(vendor).dec()

        return await asyncio.gather(
            *[_deploy(device) for device in devices],
            return_exceptions=True
        )