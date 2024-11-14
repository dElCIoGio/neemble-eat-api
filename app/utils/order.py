from google.cloud.firestore_v1.document import DocumentReference


def json(order_ref: DocumentReference):
    order_data = order_ref.get().to_dict()
    order_data["id"] = order_ref.id
    order_data["created_time"] = order_ref.get().create_time.isoformat()
    if "sessionID" in order_data:
        session_ref: DocumentReference = order_data["sessionID"]
        order_data["sessionID"] = session_ref.id
    if "itemID" in order_data:
        item_ref: DocumentReference = order_data["itemID"]
        order_data["itemID"] = item_ref.id
    return order_data


