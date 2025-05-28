from .task_service import celery_app
from .ai_service import AIService
from .topology import TopologyService
from .batch import BatchService

# 单例服务实例
ai_service = AIService()
topology_service = TopologyService()
batch_service = BatchService()

__all__ = [
    'celery_app',
    'ai_service',
    'topology_service',
    'batch_service'
]