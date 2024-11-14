from app.schemas.category import CategoryCreate
from google.cloud.firestore_v1.document import DocumentReference
from app import database
from app.crud import menu as meun_crud


collection_ref = database.db.collection('categories')


async def getCategory(category_id: str) -> DocumentReference or None:
    category = collection_ref.document(category_id)
    doc = category.get()
    return category if doc.exists else None


async def createCategory(category: CategoryCreate) -> DocumentReference:
    menu_ref = await meun_crud.getMenu(category.menuID)
    if menu_ref:
        category_data = {
            "name": category.name,
            "description": category.description or "",
            "menuID": menu_ref
        }
        if category.items:
            category_data["items"] = category.items
        ref = collection_ref.add(category_data)
        return ref[1]


async def updateCategory(category_id: str, update_data: dict) -> DocumentReference or None:
    category = await getCategory(category_id)
    if category:
        category.update(update_data)
    return category


async def deleteCategory(category_id: str) -> DocumentReference or None:
    category = await getCategory(category_id)
    if category:
        category.delete()
    return category
