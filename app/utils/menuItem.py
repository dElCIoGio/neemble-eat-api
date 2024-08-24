from google.cloud.firestore_v1.document import DocumentReference


def json(item_ref: DocumentReference):
    item_data = item_ref.get().to_dict()
    item_data["id"] = item_ref.id
    item_data["created_time"] = item_ref.get().create_time.isoformat()
    if "categoryID" in item_data:
        category_ref: DocumentReference = item_data["categoryID"]
        item_data["categoryID"] = category_ref.id
    return item_data
