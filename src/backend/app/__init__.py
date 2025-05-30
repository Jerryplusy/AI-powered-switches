from fastapi import FastAPI
from src.backend.app.api.endpoints import router
from src.backend.app.utils.logger import setup_logging
from src.backend.config import settings

app = FastAPI()
app.include_router(router,prefix="/api")

def create_app() -> FastAPI:
    # 设置日志
    setup_logging()

    # 创建FastAPI应用
    app = FastAPI(
        title=settings.APP_NAME,
        debug=settings.DEBUG,
        docs_url=f"{settings.API_PREFIX}/docs",
        redoc_url=f"{settings.API_PREFIX}/redoc",
        openapi_url=f"{settings.API_PREFIX}/openapi.json"
    )

    # 添加API路由
    app.include_router(router, prefix=settings.API_PREFIX)

    return app