from app.schemas.menuItem import MenuItemCreate
from app import database
from google.cloud.firestore_v1.document import DocumentReference
from app.crud import category as category_crud


collection_ref = database.db.collection('menu items')


def createMenuItem(menu_item: MenuItemCreate) -> DocumentReference:
    category_ref = category_crud.getCategory(menu_item.categoryID)
    if category_ref:
        item_data = {
            "name": menu_item.name,
            "description": menu_item.description or "",
            "categoryID": category_ref,
            "availability": menu_item.availability or True,
            "imageURL": menu_item.imageURL,
            "price": menu_item.price,
        }
        ref = collection_ref.add(item_data)
        return ref[1]


def getMenuItem(menu_item_id: str) -> DocumentReference or None:
    item = collection_ref.document(menu_item_id)
    doc = item.get()
    return item if doc.exists else None


def updateMenuItem(menu_item_id: str, update_data: dict) -> DocumentReference or None:
    item = getMenuItem(menu_item_id)
    if item:
        item.update(update_data)
    return item


def deleteMenuItem(menu_item_id: str) -> DocumentReference or None:
    item = getMenuItem(menu_item_id)
    if item:
        item.delete()
    return item

