from app.schemas.menuItem import MenuItemCreate
from app.db import menu_items_collection_ref
from google.cloud.firestore_v1.document import DocumentReference
from app.crud import category as category_crud



async def create_menu_item(menu_item: MenuItemCreate) -> DocumentReference:
    category_ref = await category_crud.get_category(menu_item.categoryID)
    if category_ref:
        item_data = {
            "name": menu_item.name,
            "description": menu_item.description or "",
            "categoryID": category_ref,
            "availability": menu_item.availability or True,
            "imageURL": menu_item.imageURL,
            "price": menu_item.price,
        }
        ref = menu_items_collection_ref.add(item_data)
        return ref[1]


async def get_menu_item(menu_item_id: str) -> DocumentReference or None:
    item = menu_items_collection_ref.document(menu_item_id)
    doc = item.get()
    return item if doc.exists else None


async def update_menu_item(menu_item_id: str, update_data: dict) -> DocumentReference or None:
    item = await get_menu_item(menu_item_id)
    if item:
        item.update(update_data)
    return item


async def delete_menu_item(menu_item_id: str) -> DocumentReference or None:
    item = await get_menu_item(menu_item_id)
    if item:
        item.delete()
    return item

