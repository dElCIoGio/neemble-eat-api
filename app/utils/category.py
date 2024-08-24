from google.cloud.firestore_v1.document import DocumentReference


def json(category_ref: DocumentReference):
    category_data = category_ref.get().to_dict()
    if category_data:
        category_data["id"] = category_ref.id
        category_data["created_time"] = category_ref.get().create_time.isoformat()
        if "menuID" in category_data:
            menu: DocumentReference = category_data["menuID"]
            category_data["menuID"] = menu.id
        if "items" in category_data:
            items: list[DocumentReference] = category_data["items"]
            items = list(map(lambda item: item.id, items))
            category_data["items"] = items
        return category_data
