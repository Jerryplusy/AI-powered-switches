from fastapi import APIRouter
from src.backend.app.api.command_parser import router as command_router
from src.backend.app.api.network_config import router as config_router

router = APIRouter()
router.include_router(command_router, prefix="/parse_command", tags=["Command Parsing"])
router.include_router(config_router, prefix="/apply_config", tags=["Configuration"])