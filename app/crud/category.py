from app.schemas.category import CategoryCreate
from google.cloud.firestore_v1.document import DocumentReference
from app.crud import menu as menu_crud
from app.db import categories_collection_ref


async def get_category(category_id: str) -> DocumentReference or None:
    category = categories_collection_ref.document(category_id)
    doc = category.get()
    return category if doc.exists else None


async def create_category(category: CategoryCreate) -> DocumentReference:
    menu_ref = await menu_crud.get_menu(category.menuID)
    if menu_ref:
        category_data = {
            "name": category.name,
            "description": category.description or "",
            "menuID": menu_ref,
            "items": []
        }
        if category.items:
            category_data["items"] = category.items
        ref = categories_collection_ref.add(category_data)
        return ref[1]


async def update_category(category_id: str, update_data: dict) -> DocumentReference or None:
    category = await get_category(category_id)
    if category:
        category.update(update_data)
    return category


async def delete_category(category_id: str) -> DocumentReference or None:
    category = await get_category(category_id)
    if category:
        category.delete()
    return category
