from fastapi import APIRouter, FastAPI
from .endpoints import router

app=FastAPI()
app.include_router(router)

#__all__ = ["app","router"]