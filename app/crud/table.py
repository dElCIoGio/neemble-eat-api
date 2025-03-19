from app.schemas.table import TableCreate
from google.cloud.firestore_v1.document import DocumentReference
from app.db import tables_collection_ref, restaurants_collection_ref




async def create_table(table: TableCreate) -> DocumentReference:
    # The same the getRestaurant function would do
    restaurant = restaurants_collection_ref.document(table.restaurantID)
    restaurant_exists = restaurant.get().exists
    restaurant_ref = restaurant if restaurant_exists else None

    if restaurant_ref:
        table_data = {
            "number": table.number,
            "restaurantID": restaurant_ref,
            "link": f"www.dasandza.github.io/neemble-eat/"
        }
        ref = tables_collection_ref.add(table_data)
        return ref[1]


async def get_table(table_id: str) -> DocumentReference or None:
    table = tables_collection_ref.document(table_id)
    doc = table.get()
    return table if doc.exists else None


async def update_table(table_id: str, update_data: dict) -> DocumentReference or None:
    table: DocumentReference or None = await get_table(table_id)
    if table:
        table.update(update_data)
    return table


async def delete_table(table_id: str) -> DocumentReference or None:
    table: DocumentReference or None = await get_table(table_id)
    if table:
        table_data = table.get().to_dict()

        # Deleting the table ref from its restaurant
        restaurant_ref: DocumentReference = table_data["restaurantID"]
        restaurant_data = restaurant_ref.get().to_dict()
        tables = list(filter(lambda x: x.id != table.id, restaurant_data["tables"]))
        update_data = {
            "tables": tables
        }
        restaurant_ref.update(update_data)
        table.delete()
    return table


