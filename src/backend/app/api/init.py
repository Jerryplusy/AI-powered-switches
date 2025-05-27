from fastapi import APIRouter
from .command_parser import router as command_router
from .network_config import router as config_router

router = APIRouter()
router.include_router(command_router, prefix="/parse_command", tags=["Command Parsing"])
router.include_router(config_router, prefix="/apply_config", tags=["Configuration"])