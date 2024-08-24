from google.cloud.firestore_v1.document import DocumentReference


def json(representant_ref: DocumentReference):
    representant_data = representant_ref.get().to_dict()
    representant_data["id"] = representant_ref.id
    representant_data["created_time"] = representant_ref.get().create_time.isoformat()
    if "restaurantID" in representant_data:
        if representant_data["restaurantID"]:
            restaurant_ref: DocumentReference = representant_data["restaurantID"]
            representant_data["restaurantID"] = restaurant_ref.id
    return representant_data
