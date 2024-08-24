from fastapi import APIRouter, Depends, HTTPException, Response
from app.crud import menuItem as menu_item_crud
from app.schemas import menuItem as menu_item_schema
from app.utils import menuItem as menu_item_utils


router = APIRouter()


@router.post("/", summary="Creates a Menu Item", response_model=menu_item_schema.MenuItemDisplay)
def create_menu_item(menu_item: menu_item_schema.MenuItemCreate):
    menu_item_ref = menu_item_crud.createMenuItem(menu_item=menu_item)
    menu_item_data = menu_item_utils.json(menu_item_ref)
    return menu_item_schema.MenuItemDisplay(**menu_item_data)


@router.get("/{menu_item_id}", summary="Retrieve an item by its ID from the database.", response_model=menu_item_schema.MenuItemDisplay)
def read_menu_item(menu_item_id: str):
    """
    Retrieve an item by its ID from the database.

    Args:
        menu_item_id (str): The unique identifier for the item.

    Returns:
        Item: The retrieved item object.

    Raises:
        HTTPException: 404 error if the item is not found in the database.

    Examples:
        curl -X GET "http://localhost:8000/items/123" -H  "accept: application/json"
    """
    menu_item_ref = menu_item_crud.getMenuItem(menu_item_id=menu_item_id)
    if menu_item_ref is None:
        raise HTTPException(status_code=404, detail="Menu item not found")
    menu_item_data = menu_item_utils.json(menu_item_ref)
    return menu_item_schema.MenuItemDisplay(**menu_item_data)


@router.put("/{menu_item_id}", response_model=menu_item_schema.MenuItemDisplay)
def update_menu_item(menu_item_id: str, menu_item: menu_item_schema.MenuItemBase):
    menu_item_ref = menu_item_crud.updateMenuItem(menu_item_id, menu_item.dict(exclude_unset=True))
    if menu_item_ref is None:
        raise HTTPException(status_code=404, detail="Menu item not found")
    menu_item_data = menu_item_utils.json(menu_item_ref)
    return menu_item_schema.MenuItemDisplay(**menu_item_data)


@router.delete("/{menu_item_id}", status_code=204)
def delete_menu_item(menu_item_id: str):
    menu_item_ref = menu_item_crud.deleteMenuItem(menu_item_id)
    if menu_item_ref is None:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return Response(status_code=204)
