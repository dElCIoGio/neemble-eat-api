from google.cloud.firestore_v1.document import DocumentReference


def json(table_session_ref: DocumentReference):
    table_session_data = table_session_ref.get().to_dict()
    table_session_data["id"] = table_session_ref.id
    table_session_data["created_time"] = table_session_ref.get().create_time.isoformat()
    if "invoiceID" in table_session_data:
        if table_session_data["invoiceID"]:
            invoice_ref: DocumentReference = table_session_data["invoiceID"]
            table_session_data["invoiceID"] = invoice_ref.id
    if "tableID" in table_session_data:
        table_ref: DocumentReference = table_session_data["tableID"]
        table_session_data["tableID"] = table_ref.id
    if "restaurantID" in table_session_data:
        restaurant_ref: DocumentReference = table_session_data["restaurantID"]
        table_session_data["restaurantID"] = restaurant_ref.id
    if "orders" in table_session_data:
        if table_session_data["orders"]:
            orders: list[DocumentReference] = table_session_data["orders"]
            orders = list(map(lambda order: order.id, orders))
            table_session_data["orders"] = orders
    return table_session_data

