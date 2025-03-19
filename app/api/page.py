
from fastapi import APIRouter, HTTPException
from app.services import pages as pages_service
from app.utils import restaurant as restaurant_utils
from app.schemas import restaurant as restaurant_schema
from fastapi_cache.decorator import cache
from app.api import CacheTime

router = APIRouter()

@router.get("/{table_id}/menu")
@cache(expire=CacheTime.GET_MENU_PAGE)
async def get_menu(table_id: str):
    response = await pages_service.get_menu_page(table_id=table_id)
    if not response:
        raise HTTPException(status_code=404, detail="Table not found")
    menu, restaurant_ref = response
    restaurant_data = restaurant_utils.json(restaurant_ref)
    return {
        "menu": menu,
         "restaurant": restaurant_schema.RestaurantDisplay(**restaurant_data)
    }