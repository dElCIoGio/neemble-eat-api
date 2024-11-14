from app.schemas.menu import MenuCreate
from google.cloud.firestore_v1.document import DocumentReference
from app import database
from app.crud import restaurant as restaurant_crud


collection_ref = database.db.collection('menus')


async def createMenu(menu: MenuCreate) -> DocumentReference:
    restaurant_ref = await restaurant_crud.getRestaurant(menu.restaurantID)
    if restaurant_ref:
        menu_data = {
            "restaurantID": restaurant_ref,
            "name": menu.name,
            "description": menu.description or "",
        }
        ref = collection_ref.add(menu_data)
        return ref[1]


async def getMenu(menu_id: str) -> DocumentReference or None:
    menu = collection_ref.document(menu_id)
    doc = menu.get()
    return menu if doc.exists else None


async def updateMenu(menu_id: str, update_data: dict):
    menu = await getMenu(menu_id)
    if menu:
        menu.update(update_data)
    return menu


async def deleteMenu(menu_id: str):
    menu = await getMenu(menu_id)
    if menu:
        menu.delete()
    return menu
