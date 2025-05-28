from .base import BaseAdapter
from .cisco import CiscoAdapter
from .huawei import HuaweiAdapter
from .factory import AdapterFactory

# 自动注册所有适配器类
__all_adapters__ = {
    'cisco': CiscoAdapter,
    'huawei': HuaweiAdapter
}

def get_supported_vendors() -> list:
    """获取当前支持的设备厂商列表"""
    return list(__all_adapters__.keys())

def init_adapters():
    """初始化适配器工厂"""
    AdapterFactory.register_adapters(__all_adapters__)

# 应用启动时自动初始化
init_adapters()

__all__ = [
    'BaseAdapter',
    'CiscoAdapter',
    'HuaweiAdapter',
    'AdapterFactory',
    'get_supported_vendors'
]