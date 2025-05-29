from fastapi import HTTPException, status

class AICommandParseException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"AI command parse error: {detail}"
        )

class SwitchConfigException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Switch configuration error: {detail}"
        )

class SiliconFlowAPIException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"SiliconFlow API error: {detail}"
        )