from fastapi import APIRouter, Depends, HTTPException, Response
from app.crud import restaurant as restaurant_crud
from app.schemas import restaurant as restaurant_schema
from app.schemas import order as order_schema
from app.schemas import menu as menu_schema
from app.schemas import table as table_schema
from app.schemas import tableSession as table_session_schema
from app.utils import table as table_utils
from app.utils import order as order_utils
from app.utils import restaurant as restaurant_utils
from app.utils import tableSession as table_session_utils
from app.services import restaurant as restaurant_service


router = APIRouter()


@router.post("/", response_model=restaurant_schema.RestaurantDisplay)
def create_restaurant(restaurant: restaurant_schema.RestaurantCreate):
    restaurant_ref = restaurant_service.create_restaurant(restaurant=restaurant)
    if restaurant_ref is None:
        raise HTTPException(status_code=400, detail="There was an error creating the restaurant account")
    restaurant_data = restaurant_utils.json(restaurant_ref)
    return restaurant_schema.RestaurantDisplay(**restaurant_data)


@router.get("/{restaurant_id}", response_model=restaurant_schema.RestaurantDisplay)
def read_restaurant(restaurant_id: str):
    restaurant_ref = restaurant_crud.getRestaurant(restaurant_id=restaurant_id)
    if restaurant_ref is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    restaurant_data = restaurant_utils.json(restaurant_ref)
    return restaurant_schema.RestaurantDisplay(**restaurant_data)


@router.put("/{restaurant_id}", response_model=restaurant_schema.RestaurantDisplay)
def update_restaurant(restaurant_id: str, restaurant: restaurant_schema.RestaurantBase):
    restaurant_ref = restaurant_crud.updateRestaurant(restaurant_id, restaurant.dict(exclude_unset=True))
    if restaurant_ref is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    restaurant_data = restaurant_utils.json(restaurant_ref)
    return restaurant_schema.RestaurantDisplay(**restaurant_data)


@router.delete("/{restaurant_id}", status_code=204)
def delete_restaurant(restaurant_id: str):
    restaurant_ref = restaurant_crud.deleteRestaurant(restaurant_id)
    if restaurant_ref is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return Response(status_code=204)


# Service


@router.put("/{restaurant_id}/{representant_id}/representant", response_model=restaurant_schema.RestaurantDisplay)
def add_manager(restaurant_id: str, representant_id: str):
    restaurant_ref = restaurant_service.assign_manager(restaurant_id, representant_id)
    if not restaurant_ref:
        raise HTTPException(status_code=404, detail="Restaurant not found.")
    restaurant_data = restaurant_utils.json(restaurant_ref)
    return restaurant_schema.RestaurantDisplay(**restaurant_data)


@router.put("/{restaurant_id}/tables", response_model=table_schema.TableDisplay)
def add_table(restaurant_id: str):
    table_ref = restaurant_service.add_table(restaurant_id)
    if not table_ref:
        raise HTTPException(status_code=404, detail="Restaurant not found.")
    table_data = table_utils.json(table_ref)
    return table_schema.TableDisplay(**table_data)


@router.put("/{restaurant_id}/menus", response_model=restaurant_schema.RestaurantDisplay)
def add_menu(restaurant_id: str, menu: menu_schema.MenuCreate):
    restaurant_ref = restaurant_service.add_menu(restaurant_id, menu)
    if not restaurant_ref:
        raise HTTPException(status_code=404, detail="Restaurant not found.")
    restaurant_data = restaurant_utils.json(restaurant_ref)
    return restaurant_schema.RestaurantDisplay(**restaurant_data)


@router.get("/{restaurant_id}/orders", response_model=list[order_schema.OrderDisplay])
def get_all_orders(restaurant_id: str):
    all_orders_ref = restaurant_service.get_orders(restaurant_id)
    if not all_orders_ref:
        raise HTTPException(status_code=404, detail="Restaurant not found.")
    all_orders = list(map(lambda order: order_utils.json(order), all_orders_ref))
    return list(map(lambda order: order_schema.OrderDisplay(**order), all_orders))


@router.get("/{restaurant_id}/{table_number}/open-session", response_model=table_session_schema.TableSessionDisplay)
def get_restaurant_table_open(restaurant_id: str, table_number: str):
    table_session_ref = restaurant_service.get_restaurant_table_open(restaurant_id, int(table_number))
    if not table_session_ref:
        raise HTTPException(status_code=404, detail="Session not found.")
    table_session_data = table_session_utils.json(table_session_ref)
    return table_session_schema.TableSessionDisplay(**table_session_data)

