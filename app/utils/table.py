from google.cloud.firestore_v1.document import DocumentReference


def json(table_ref: DocumentReference):
    table_data = table_ref.get().to_dict()
    table_data["id"] = table_ref.id
    table_data["created_time"] = table_ref.get().create_time.isoformat()
    if "currentSessionID" in table_data:
        if table_data["currentSessionID"]:
            session_ref: DocumentReference = table_data["currentSessionID"]
            table_data["currentSessionID"] = session_ref.id
    if "restaurantID" in table_data:
        if table_data["restaurantID"]:
            restaurant_ref: DocumentReference = table_data["restaurantID"]
            table_data["restaurantID"] = restaurant_ref.id
    if "sessionOrders" in table_data:
        if table_data["sessionOrders"]:
            orders: list[DocumentReference] = table_data["sessionOrders"]
            orders = list(map(lambda order: order.id, orders))
            table_data["sessionOrders"] = orders
    return table_data