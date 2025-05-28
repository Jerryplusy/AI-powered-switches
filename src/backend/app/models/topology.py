#拓补数据结构
from enum import Enum
from typing import Dict, List
from pydantic import BaseModel

class TopologyType(str, Enum):
    SPINE_LEAF = "spine-leaf"
    CORE_ACCESS = "core-access"
    RING = "ring"

class DeviceRole(str, Enum):
    CORE = "core"
    SPINE = "spine"
    LEAF = "leaf"
    ACCESS = "access"

class NetworkTopology(BaseModel):
    type: TopologyType
    devices: Dict[DeviceRole, List[str]]
    links: Dict[str, List[str]]