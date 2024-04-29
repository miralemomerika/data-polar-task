from api_app.dependencies import templates
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from database_app.database import get_connection

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def current_item_quantity(request: Request):
    async with get_connection() as conn:
        result = await conn.fetch(
            """
                SELECT 
                    item_id, 
                    SUM(quantity) AS total_quantity
                FROM inventory
                GROUP BY item_id
                ORDER BY item_id;
            """
        )

    # Ensure the result is passed as a list of dictionaries to the context
    items = [dict(row) for row in result]

    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"items": items},
    )


@router.get("/item/{item_id}")
async def inventory_item(request: Request, item_id: int):
    async with get_connection() as conn:
        result = await conn.fetch(
            """
            SELECT 
                item_id,
                date_received_into_inventory,
                date_shipped_from_inventory,
                SUM(quantity) as total_quantity
            FROM inventory
            WHERE item_id = $1
            GROUP BY item_id, date_received_into_inventory, date_shipped_from_inventory
            ORDER BY COALESCE(date_received_into_inventory, date_shipped_from_inventory) DESC;
            """,
            item_id
        )
    items = [dict(row) for row in result]
    return templates.TemplateResponse(
        request=request,
        name="list.html",
        context={"items": items, "list_title": f"Inventory Transactions for Item {item_id}"},
    )
