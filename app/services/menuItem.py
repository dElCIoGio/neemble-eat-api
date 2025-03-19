
from app.googleCloudStorage import uploadFile
from app.crud import menuItem as menu_item_crud
from app.crud import restaurant as restaurant_crud

from google.cloud.firestore_v1.document import DocumentReference


async def update_menu_item(
        menu_item_id: str,
        restaurant_id: str,
        name: str = None,
        description: str = None,
        file_path: str = None,
        price: float = None,
        category_id: str = None,
        availability: bool = None) -> DocumentReference or None:
    restaurant_ref = await restaurant_crud.get_restaurant(restaurant_id)
    if restaurant_ref:
        image_url = uploadFile(
            file_path=file_path,
            filename=f"{menu_item_id}.jpg",
            folder_path=f"{restaurant_id}/items"
        ) if file_path else None

        update = update_dict(
            name=name,
            category_id=category_id,
            availability=availability,
            description=description,
            price=price,
            image_url=image_url)
        if len(update):
            return await menu_item_crud.update_menu_item(menu_item_id, update)
        return None


def update_dict(
        name: str = None,
        description: str = None,
        image_url: str = None,
        price: float = None,
        category_id: str = None,
        availability: bool = None):
    update = {}
    if name is not None:
        update["name"] = name
    if description is not None:
        update["description"] = description
    if category_id is not None:
        update["categoryID"] = category_id
    if availability is not None:
        update["availability"] = availability
    if price is not None:
        update["price"] = price
    if image_url is not None:
        update["imageURL"] = image_url
    return update
