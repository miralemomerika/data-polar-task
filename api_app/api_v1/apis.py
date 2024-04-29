from fastapi import APIRouter

from api_app.api_v1.endpoints import data_pipeline, inventory

api_router = APIRouter()
api_router.include_router(data_pipeline.router, prefix="/data", tags=["data_pipeline"])
api_router.include_router(inventory.router, prefix="/inventory", tags=["inventory"])
