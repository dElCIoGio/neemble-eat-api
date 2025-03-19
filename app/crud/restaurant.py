from google.cloud.firestore_v1.document import DocumentReference

from app.db import restaurants_collection_ref
from app.schemas.restaurant import RestaurantCreate



async def create_restaurant(restaurant: RestaurantCreate) -> DocumentReference:
    restaurant_data = {
        "name": restaurant.name,
        "address": restaurant.address,
        "phoneNumber": restaurant.phoneNumber,
        "bannerURL": restaurant.bannerURL,
        "description": restaurant.description,
    }
    ref = restaurants_collection_ref.add(restaurant_data)
    return ref[1]



async def get_restaurant(restaurant_id: str) -> DocumentReference or None:
    restaurant = restaurants_collection_ref.document(restaurant_id)
    doc = restaurant.get()
    return restaurant if doc.exists else None


def get_all_restaurants():
    return restaurants_collection_ref.get()


async def update_restaurant(restaurant_id: str, update_data: dict) -> DocumentReference or None:
    restaurant = await get_restaurant(restaurant_id)
    if restaurant:
        restaurant.update(update_data)
    return restaurant


async def delete_restaurant(restaurant_id: str) -> DocumentReference or None:
    restaurant = await get_restaurant(restaurant_id)
    if restaurant:
        restaurant.delete()
    return restaurant


