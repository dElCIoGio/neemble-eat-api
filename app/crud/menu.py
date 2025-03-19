from app.schemas.menu import MenuCreate
from google.cloud.firestore_v1.document import DocumentReference
from app.db import menus_collection_ref
from app.crud import restaurant as restaurant_crud



async def create_menu(menu: MenuCreate) -> DocumentReference:
    restaurant_ref = await restaurant_crud.get_restaurant(menu.restaurantID)
    if restaurant_ref:
        menu_data = {
            "restaurantID": restaurant_ref,
            "name": menu.name,
            "description": menu.description or "",
        }
        ref = menus_collection_ref.add(menu_data)
        return ref[1]


async def get_menu(menu_id: str) -> DocumentReference or None:
    menu = menus_collection_ref.document(menu_id)
    doc = menu.get()
    return menu if doc.exists else None


async def update_menu(menu_id: str, update_data: dict):
    menu = await get_menu(menu_id)
    if menu:
        menu.update(update_data)
    return menu


async def delete_menu(menu_id: str):
    menu = await get_menu(menu_id)
    if menu:
        menu.delete()
    return menu
