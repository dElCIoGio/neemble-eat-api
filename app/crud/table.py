from app.schemas.table import TableCreate
from urllib.parse import quote
from google.cloud.firestore_v1.document import DocumentReference
from app import database


collection_ref = database.db.collection('tables')


def createTable(table: TableCreate) -> DocumentReference:
    # The same the getRestaurant function would do
    restaurant = database.db.collection("restaurants").document(table.restaurantID)
    restaurantExists = restaurant.get().exists
    restaurantRef = restaurant if restaurantExists else None

    if restaurantRef:
        table_data = {
            "number": table.number,
            "restaurantID": restaurantRef,
            "link": f"www.dasandza.github.io/neemble-eat/menu/{restaurantRef.id}/{restaurantRef.get().to_dict()['menus'][0].id}/{table.number}"
        }
        ref = collection_ref.add(table_data)
        return ref[1]


def getTable(table_id: str) -> DocumentReference or None:
    table = collection_ref.document(table_id)
    doc = table.get()
    return table if doc.exists else None


def updateTable(table_id: str, update_data: dict) -> DocumentReference or None:
    table = getTable(table_id)
    if table:
        table.update(update_data)
    return table


def updateAllFields(table_id: str) -> DocumentReference or None:
    table = getTable(table_id)
    if table:
        table_doc = table.get()
        table_data = table_doc.to_dict()
        restaurantRef = table_data["restaurantID"]
        sessionRef = table_data["currentSessionID"] if "currentSessionID" in table_data else None
        table_data["link"] = f"www.dasandza.github.io/neemble-eat/b/{quote(restaurantRef.get().to_dict()['name'])}/{table.number}"
        if sessionRef:
            table_data["currentSessionID"] = sessionRef
            table_data["sessionStatus"] = sessionRef.get().to_dict()["status"]
            table_data["sessionOrders"] = sessionRef.get().to_dict()["orders"]
        table.update(table_data)
        return table


def deleteTable(table_id: str) -> DocumentReference or None:
    table = getTable(table_id)
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


