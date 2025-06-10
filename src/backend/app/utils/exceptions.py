from fastapi import HTTPException, status
from typing import Optional

class AICommandParseException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"AI command parse error: {detail}"
        )

class SwitchConfigException(HTTPException):
    def __init__(
        self,
        detail: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    ):
        super().__init__(
            status_code=status_code,
            detail=f"Switch error: {detail}"
        )

class ConfigBackupException(SwitchConfigException):
    """配置备份失败异常"""
    def __init__(self, ip: str):
        super().__init__(
            detail=f"无法备份设备 {ip} 的配置",
            recovery_guide="检查设备存储空间或权限"
        )

class ConfigRollbackException(SwitchConfigException):
    """回滚失败异常"""
    def __init__(self, ip: str, original_error: str):
        super().__init__(
            detail=f"设备 {ip} 回滚失败（原始错误：{original_error}）",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )
