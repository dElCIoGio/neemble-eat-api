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
        categoryID: str = None,
        availability: bool = None) -> DocumentReference or None:
    restaurant_ref = await restaurant_crud.getRestaurant(restaurant_id)
    if restaurant_ref:
        imageURL = uploadFile(
            file_path=file_path,
            filename=f"{menu_item_id}.jpg",
            folder_path=f"{restaurant_id}/items"
        ) if file_path else None

        update = update_dict(
            name=name,
            categoryID=None,
            availability=availability,
            description=description,
            price=price,
            imageURL=imageURL)
        print(update)
        if len(update):
            return await menu_item_crud.updateMenuItem(menu_item_id, update)
        return None


def update_dict(
        name: str = None,
        description: str = None,
        imageURL: str = None,
        price: float = None,
        categoryID: str = None,
        availability: bool = None):
    update = {}
    if name is not None:
        update["name"] = name
    if description is not None:
        update["description"] = description
    if categoryID is not None:
        update["categoryID"] = categoryID
    if availability is not None:
        update["availability"] = availability
    if price is not None:
        update["price"] = price
    if imageURL is not None:
        update["imageURL"] = imageURL
    return update
