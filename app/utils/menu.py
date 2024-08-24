from google.cloud.firestore_v1.document import DocumentReference


def json(menu_ref: DocumentReference):
    menu_data = menu_ref.get().to_dict()
    menu_data["id"] = menu_ref.id
    menu_data["created_time"] = menu_ref.get().create_time.isoformat()
    if "restaurantID" in menu_data:
        restaurant_ref: DocumentReference = menu_data["restaurantID"]
        menu_data["restaurantID"] = restaurant_ref.id
    if "categories" in menu_data:
        if menu_data["categories"]:
            categories: list[DocumentReference] = menu_data["categories"]
            categories = list(map(lambda category: category.id, categories))
            menu_data["categories"] = categories
    return menu_data


