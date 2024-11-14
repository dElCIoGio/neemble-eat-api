from fastapi import APIRouter, HTTPException, Response, File, UploadFile, Form
from app.crud import restaurant as restaurant_crud
from app.schemas import restaurant as restaurant_schema
from app.schemas import order as order_schema
from app.schemas import table as table_schema
from app.schemas import menu as menu_schema
from app.schemas import tableSession as table_session_schema
from app.utils import table as table_utils
from app.utils import order as order_utils
from app.utils import restaurant as restaurant_utils
from app.utils import tableSession as table_session_utils
from app.utils import menu as menu_utils
from app.services import restaurant as restaurant_service

from pathlib import Path
from typing import List, Tuple
import os
import aiofiles


router = APIRouter()
base_path = Path(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIRECTORY = base_path.parent / "uploads"
# UPLOAD_DIRECTORY.parent.mkdir(parents=True, exist_ok=True)


@router.post("/", response_model=restaurant_schema.RestaurantDisplay)
async def create_restaurant(
          name: str = Form(...),
          address: str = Form(...),
          phoneNumber: str = Form(...),
          description: str = Form(...),
          bannerFile: UploadFile = File(...)
        ):
    safe_filename = bannerFile.filename.replace("/", "_").replace("\\", "_").replace("..", "_")
    file_location = UPLOAD_DIRECTORY / safe_filename
    try:
        async with aiofiles.open(file_location, "wb") as buffer:
            await buffer.write(await bannerFile.read())

        restaurant = restaurant_schema.RestaurantCreate(
            name=name,
            address=address,
            phoneNumber=phoneNumber,
            representants=None,
            bannerURL=str(file_location),
            description=description,
            sessions=None,
            menus=None,
            tables=None
        )

        restaurant_ref = await restaurant_service.create_restaurant(restaurant=restaurant)
        if restaurant_ref is None:
            raise HTTPException(status_code=400, detail="There was an error creating the restaurant account")
        restaurant_data = restaurant_utils.json(restaurant_ref)
        if file_location.exists():
            os.remove(file_location)
        return restaurant_schema.RestaurantDisplay(**restaurant_data)

    except Exception as error:
        print("Error: ", error)


@router.get("/{restaurant_id}", response_model=restaurant_schema.RestaurantDisplay)
async def read_restaurant(restaurant_id: str):
    restaurant_ref = await restaurant_crud.getRestaurant(restaurant_id=restaurant_id)
    if restaurant_ref is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    restaurant_data = restaurant_utils.json(restaurant_ref)
    return restaurant_schema.RestaurantDisplay(**restaurant_data)


@router.put("/{restaurant_id}", response_model=restaurant_schema.RestaurantDisplay)
async def update_restaurant(restaurant_id: str, restaurant: restaurant_schema.RestaurantBase):
    restaurant_ref = await restaurant_crud.updateRestaurant(restaurant_id, restaurant.model_dump(exclude_unset=True))
    if restaurant_ref is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    restaurant_data = restaurant_utils.json(restaurant_ref)
    return restaurant_schema.RestaurantDisplay(**restaurant_data)


@router.delete("/{restaurant_id}", status_code=204)
async def delete_restaurant(restaurant_id: str):
    restaurant_ref = await restaurant_crud.deleteRestaurant(restaurant_id)
    if restaurant_ref is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return Response(status_code=204)


# Service


@router.put("/{restaurant_id}/{representant_id}/representant", response_model=restaurant_schema.RestaurantDisplay)
async def add_manager(restaurant_id: str, representant_id: str):
    restaurant_ref = await restaurant_service.assign_manager(restaurant_id, representant_id)
    if not restaurant_ref:
        raise HTTPException(status_code=404, detail="Restaurant not found.")
    restaurant_data = restaurant_utils.json(restaurant_ref)
    return restaurant_schema.RestaurantDisplay(**restaurant_data)


@router.put("/{restaurant_id}/tables", response_model=table_schema.TableDisplay)
async def add_table(restaurant_id: str):
    table_ref = await restaurant_service.add_table(restaurant_id)
    if not table_ref:
        raise HTTPException(status_code=404, detail="Restaurant not found.")
    table_data = table_utils.json(table_ref)
    return table_schema.TableDisplay(**table_data)


@router.put("/{restaurant_id}/menus", response_model=menu_schema.MenuDisplay)
async def add_menu(restaurant_id: str, menu: menu_schema.MenuCreate):
    menu_ref = await restaurant_service.add_menu(restaurant_id, menu)
    if not menu_ref:
        raise HTTPException(status_code=404, detail="Restaurant not found.")
    menu_data = menu_utils.json(menu_ref)
    return menu_schema.MenuDisplay(**menu_data)


@router.get("/{restaurant_id}/orders", response_model=list[order_schema.OrderDisplay])
async def get_all_orders(restaurant_id: str):
    all_orders_ref = await restaurant_service.get_all_orders(restaurant_id)
    if not all_orders_ref:
        raise HTTPException(status_code=404, detail="Restaurant not found.")
    all_orders = list(map(lambda order: order_utils.json(order), all_orders_ref))
    return list(map(lambda order: order_schema.OrderDisplay(**order), all_orders))


@router.get("/{restaurant_id}/{table_number}/open-session", response_model=table_session_schema.TableSessionDisplay)
async def get_restaurant_table_open(restaurant_id: str, table_number: str):
    table_session_ref = await restaurant_service.get_restaurant_table_open(restaurant_id, int(table_number))
    if not table_session_ref:
        raise HTTPException(status_code=404, detail="Session not found.")
    table_session_data = table_session_utils.json(table_session_ref)
    return table_session_schema.TableSessionDisplay(**table_session_data)


@router.get("/{restaurant_id}/last-orders", response_model=List[Tuple[str, int]])
async def most_ordered_last_seven_days(restaurant_id: str):
    orders: List[Tuple[str, int]] = \
        await restaurant_service.most_ordered_last_seven_days(restaurant_id)
    if not orders:
        raise HTTPException(status_code=404, detail="Restaurant not found.")
    return orders


@router.get("/{restautant_id}/last-sessions", response_model=List[table_session_schema.TableSessionDisplay])
async def get_last_sessions(restautant_id: str):
    sessions = await restaurant_service.get_last_sessions(restautant_id)
    return sessions
