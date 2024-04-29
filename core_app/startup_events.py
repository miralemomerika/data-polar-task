from database_app.database import get_connection


async def create_inventory_table():
    async with get_connection() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                item_id INTEGER,
                quantity FLOAT,
                date_production_start TIMESTAMP,
                date_received_into_inventory TIMESTAMP,
                date_shipped_from_inventory TIMESTAMP
            );
        """)
