from app.schemas.menu import MenuCreate
from google.cloud.firestore_v1.document import DocumentReference
from app import database


collection_ref = database.db.collection('menus')


def createMenu(menu: MenuCreate) -> DocumentReference:
    menu_data = {
        "restaurantID": menu.restaurantID,
        "name": menu.name,
        "description": menu.description or "",
    }
    ref = collection_ref.add(menu_data)
    return ref[1]


def getMenu(menu_id: str) -> DocumentReference or None:
    menu = collection_ref.document(menu_id)
    doc = menu.get()
    return menu if doc.exists else None


def updateMenu(menu_id: str, update_data: dict):
    menu = getMenu(menu_id)
    if menu:
        menu.update(update_data)
    return menu


def deleteMenu(menu_id: str):
    menu = getMenu(menu_id)
    if menu:
        menu.delete()
    return menu
