from pydantic import BaseModel
from typing import Optional

class DeviceCredentials(BaseModel):
    username: str
    password: str
    enable_password: Optional[str] = None

class DeviceInfo(BaseModel):
    ip: str
    vendor: str
    model: Optional[str] = None
    os_version: Optional[str] = None
    credentials: DeviceCredentials