# 数据模型模块初始化文件
# 目前项目不使用数据库，此文件保持为空
# 未来如果需要添加数据库模型，可以在这里定义

from pydantic import BaseModel
from typing import Optional

# 示例：基础响应模型
class BaseResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    data: Optional[dict] = None

# 示例：交换机连接信息模型（如果需要存储交换机信息）
class SwitchInfo(BaseModel):
    ip: str
    username: str
    password: str
    model: Optional[str] = None
    description: Optional[str] = None

# 示例：配置历史记录模型
class ConfigHistory(BaseModel):
    command: str
    config: dict
    timestamp: float
    status: str  # success/failed
    error: Optional[str] = None

__all__ = ["BaseResponse", "SwitchInfo", "ConfigHistory"]