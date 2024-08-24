from google.cloud.firestore_v1.document import DocumentReference


def json(invoice_ref: DocumentReference):
    invoice_data = invoice_ref.get().to_dict()
    invoice_data["id"] = invoice_ref.id
    invoice_data["created_time"] = invoice_ref.get().create_time.isoformat()
    if "orders" in invoice_data:
        if invoice_data["orders"]:
            orders: list[DocumentReference] = invoice_data["orders"]
            orders = list(map(lambda order: order.id, orders))
            invoice_data["orders"] = orders
    if "sessionID" in invoice_data:
        session_ref: DocumentReference = invoice_data["sessionID"]
        invoice_data["sessionID"] = session_ref.id
    return invoice_data
