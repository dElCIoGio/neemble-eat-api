from google.cloud.firestore_v1.document import DocumentReference
from app import database
from app.schemas.restaurant import RestaurantCreate


collection_ref = database.db.collection('restaurants')


async def createRestaurant(restaurant: RestaurantCreate) -> DocumentReference:
    restaurant_data = {
        "name": restaurant.name,
        "address": restaurant.address,
        "phoneNumber": restaurant.phoneNumber,
        "bannerURL": restaurant.bannerURL,
        "description": restaurant.description,
    }
    ref = collection_ref.add(restaurant_data)
    return ref[1]


async def getRestaurant(restaurant_id: str) -> DocumentReference or None:
    restaurant = collection_ref.document(restaurant_id)
    doc = restaurant.get()
    return restaurant if doc.exists else None


async def updateRestaurant(restaurant_id: str, update_data: dict) -> DocumentReference or None:
    restaurant = await getRestaurant(restaurant_id)
    if restaurant:
        restaurant.update(update_data)
    return restaurant


async def deleteRestaurant(restaurant_id: str) -> DocumentReference or None:
    restaurant = await getRestaurant(restaurant_id)
    if restaurant:
        restaurant.delete()
    return restaurant
