#Celery任务定义
from celery import Celery
from src.backend.app.utils.connection_pool import ConnectionPool
from src.backend.config import settings

celery = Celery(__name__, broker=settings.REDIS_URL)
pool = ConnectionPool(max_size=settings.MAX_CONNECTIONS)

@celery.task
async def deploy_to_device(device_info: dict, config: dict):
    adapter = await pool.get(device_info['vendor'])
    try:
        await adapter.connect(device_info['ip'], device_info['credentials'])
        result = await adapter.deploy_config(config)
        await pool.release(adapter)
        return {'device': device_info['ip'], 'result': result}
    except Exception as e:
        return {'device': device_info['ip'], 'error': str(e)}