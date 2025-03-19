from typing import List
from google.cloud.firestore_v1.document import DocumentReference
from app.crud import category as category_crud
from app.crud import menuItem as menu_item_crud
from app.schemas import menuItem as menu_item_schema
from app.utils import menuItem as menu_item_utils

from app.googleCloudStorage import uploadFile


async def add_item(category_id: str, menu_item: menu_item_schema.MenuItemCreate):
    category_ref = await category_crud.get_category(category_id)
    if category_ref:
        item_ref = await menu_item_crud.create_menu_item(menu_item)
        if not item_ref:
            return None
        category_data = category_ref.get().to_dict()
        menu_ref: DocumentReference = category_data["menuID"]
        menu_data = menu_ref.get().to_dict()
        restaurant_ref: DocumentReference = menu_data["restaurantID"]
        image_url = uploadFile(
            file_path=menu_item.imageURL,
            filename=f"{item_ref.id}.jpg",
            folder_path=f"{restaurant_ref.id}/items"
        )
        item_ref.update({
            "imageURL": image_url
        })
        if "items" in category_data:
            category_data = category_ref.get().to_dict()
            items: list[DocumentReference] = category_data["items"]
        else:
            items: list[DocumentReference] = []
        items.append(item_ref)
        update_data = {
            "items": items
        }
        category_ref.update(update_data)
        return item_ref


async def remove_item(category_id: str, menu_item_id: str) -> DocumentReference or None:
    category_ref = await category_crud.get_category(category_id)
    item_ref = await menu_item_crud.get_menu_item(menu_item_id)
    if category_ref and item_ref:
        category_data = category_ref.get().to_dict()
        if "items" in category_data:
            items: list[DocumentReference] = category_data["items"]
            items = list(filter(lambda item: item.id != menu_item_id, items))
            category_data.update({
                "items": items
            })
        return category_ref


async def remove_items(category_id: str, menu_item_ids: List[str]) -> DocumentReference or None:
    category_ref = None
    for menu_item_id in menu_item_ids:
        category_ref = await remove_item(category_id, menu_item_id)
    return category_ref


async def delete_category_and_items(category_id: str):
    category_ref = await category_crud.get_category(category_id)
    if category_ref:
        category_data = category_ref.get().to_dict()
        if "items" in category_data:
            items: list[DocumentReference] = category_data["items"]
            for item_ref in items:
                item_ref.delete()
        category_ref.delete()
    return category_ref


async def get_parsed_category(category_id: str):
    category_ref = await category_crud.get_category(category_id)
    if category_ref:
        category_data = category_ref.get().to_dict()
        if "items" in category_data:
            all_items = []
            items = category_data["items"]
            for item_ref in items:
                item = await menu_item_crud.get_menu_item(item_ref.id)
                if item:
                    item = menu_item_utils.json(item)
                    all_items.append(item)
        else:
            all_items = []

        category_data["id"] = category_ref.id
        category_data["menuID"] = category_data["menuID"].id
        category_data["items"] = all_items
        return category_data


