from app.schemas.table import TableCreate
from urllib.parse import quote
from google.cloud.firestore_v1.document import DocumentReference
from app import database


collection_ref = database.db.collection('tables')


async def createTable(table: TableCreate) -> DocumentReference:
    # The same the getRestaurant function would do
    restaurant = database.db.collection("restaurants").document(table.restaurantID)
    restaurantExists = restaurant.get().exists
    restaurantRef = restaurant if restaurantExists else None

    if restaurantRef:
        table_data = {
            "number": table.number,
            "restaurantID": restaurantRef,
            "link": f"www.dasandza.github.io/neemble-eat/"
        }
        ref = collection_ref.add(table_data)
        return ref[1]


async def getTable(table_id: str) -> DocumentReference or None:
    table = collection_ref.document(table_id)
    doc = table.get()
    return table if doc.exists else None


async def updateTable(table_id: str, update_data: dict) -> DocumentReference or None:
    table: DocumentReference or None = await getTable(table_id)
    if table:
        table.update(update_data)
    return table


async def deleteTable(table_id: str) -> DocumentReference or None:
    table: DocumentReference or None = await getTable(table_id)
    if table:
        table_data = table.get().to_dict()

        # Deleting the table ref from its restaurant
        restaurantRef: DocumentReference = table_data["restaurantID"]
        restaurantData = restaurantRef.get().to_dict()
        tables = list(filter(lambda x: x.id != table.id, restaurantData["tables"]))
        update_data = {
            "tables": tables
        }
        restaurantRef.update(update_data)
        table.delete()
    return table


