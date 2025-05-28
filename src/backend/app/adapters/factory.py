from . import BaseAdapter
from .cisco import CiscoAdapter
from .huawei import HuaweiAdapter

class AdapterFactory:
    _adapters = {}

    @classmethod
    def register_adapters(cls, adapters: dict):
        """注册适配器字典"""
        cls._adapters.update(adapters)

    @classmethod
    def get_adapter(vendor: str)->BaseAdapter:
        adapters = {
            'cisco': CiscoAdapter,
            'huawei': HuaweiAdapter
        }
        if vendor not in cls._adapters:
            raise ValueError(f"Unsupported vendor: {vendor}")
        return cls._adapters[vendor]()
