from app.schemas import category as category_schema
from app.crud import category as category_crud
from app.crud import menu as menu_crud
from google.cloud.firestore_v1.document import DocumentReference
from app.services import category as category_service


async def add_category(menu_id: str, category: category_schema.CategoryCreate):
    menu_ref = await menu_crud.getMenu(menu_id)
    if menu_ref:
        category_ref = await category_crud.createCategory(category)
        if not category_ref:
            return None
        menu_data = menu_ref.get().to_dict()
        if "categories" in menu_data:
            categories: list[DocumentReference] = menu_data["categories"]

        else:
            categories: list[DocumentReference] = []
        categories.append(category_ref)
        update_data = {
            "categories": categories
        }
        menu_ref.update(update_data)
        return category_ref


async def remove_category(menu_id: str, category_id: str) -> DocumentReference or None:
    menu_ref = await menu_crud.getMenu(menu_id)
    category_ref = await category_service.delete_category_and_items(category_id)
    if menu_ref and category_ref:
        menu_data = menu_ref.get().to_dict()
        if "categories" in menu_data:
            categories: list[DocumentReference] = menu_data["categories"]
            categories = list(filter(lambda category: category.id != category_id, categories))
            menu_ref.update({
                "categories": categories
            })
        return menu_ref


async def delete_menu_and_categories(menu_id: str) -> DocumentReference or None:
    menu_ref = await menu_crud.getMenu(menu_id)
    if menu_ref:
        menu_data = menu_ref.get().to_dict()
        if "categories" in menu_data:
            categories: list[DocumentReference] = menu_data["categories"]
            for category_ref in categories:
                await category_service.delete_category_and_items(category_ref.id)
        menu_ref.delete()
    return menu_ref


async def get_parsed_menu(menu_id: str):
    menu_ref = await menu_crud.getMenu(menu_id)
    if menu_ref:
        menu_data = menu_ref.get().to_dict()
        if "categories" in menu_data:
            all_categories = []
            categories = menu_data["categories"]
            for category_ref in categories:
                category = await category_service.get_parsed_category(category_ref.id)
                all_categories.append(category)
            menu_data["id"] = menu_ref.id
            menu_data["created_time"] = menu_ref.get().create_time.isoformat()
            menu_data["restaurantID"] = menu_data["restaurantID"].id
            menu_data["categories"] = list(filter(lambda category: category is not None, all_categories))
            return menu_data
