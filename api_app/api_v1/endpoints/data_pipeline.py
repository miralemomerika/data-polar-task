from pathlib import Path

from fastapi import UploadFile, File, APIRouter
from core_app.settings import settings
import polars as pl
import io
import aiofiles

from database_app.database import get_connection

router = APIRouter()


@router.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    if file.filename.endswith('.csv'):
        data = await file.read()
        await process_csv(data)
        return {"status": "success", "message": "CSV processed and data stored in PostgreSQL"}
    return {"status": "error", "message": "Invalid file format"}


@router.post("/trigger-data-pipeline/")
async def trigger_data_pipeline():
    file_path = Path(settings.BASE_DIR, 'test-project-data.csv')
    if file_path.exists() and file_path.suffix == '.csv':
        async with aiofiles.open(file_path, mode='rb') as file:
            data = await file.read()
            await process_csv(data)
            return {"status": "success", "message": "CSV processed and data stored in PostgreSQL"}
    return {"status": "error", "message": "File does not exist or is not a CSV file."}


async def process_csv(data: bytes):
    stream = io.BytesIO(data)

    df = pl.read_csv(stream)

    df = df.with_columns([
        pl.col("item_id").cast(pl.Int32).alias("item_id"),
        pl.col("quantity").cast(pl.Float64).alias("quantity"),
        pl.col("date_production_start").str.strptime(pl.Datetime, "%Y-%m-%d %H:%M:%S", strict=False).alias(
            "date_production_start"),
        pl.col("date_received_into_inventory").str.strptime(pl.Datetime, "%Y-%m-%d %H:%M:%S", strict=False).alias(
            "date_received_into_inventory"),
        pl.col("date_shipped_from_inventory").str.strptime(pl.Datetime, "%Y-%m-%d %H:%M:%S", strict=False).alias(
            "date_shipped_from_inventory"),
    ])

    # Remove duplicates
    # df = df.distinct()

    await upload_to_postgres(df)


async def upload_to_postgres(df: pl.DataFrame):
    async with get_connection() as conn:
        try:
            await conn.copy_records_to_table('inventory', records=df.rows())
        except Exception as e:
            # could log to a file or monitoring service
            print(f"An error occurred: {e}")
            raise e
