from fastapi import FastAPI
from api_app.api_v1.apis import api_router
from core_app.settings import settings
from core_app.startup_events import create_inventory_table
from database_app.database import init_pool, close_pool
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.include_router(api_router, prefix=settings.API_V1_STR)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
async def startup_event():
    await init_pool()
    await create_inventory_table()


@app.on_event("shutdown")
async def shutdown_event():
    await close_pool()
