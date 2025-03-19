from google.cloud.firestore_v1.document import DocumentReference


def json(user_ref: DocumentReference):
    user_data = user_ref.get().to_dict()
    user_data["id"] = user_ref.id
    user_data["created_time"] = user_ref.get().create_time.isoformat()
    if "restaurantID" in user_data:
        if user_data["restaurantID"]:
            restaurant_ref: DocumentReference = user_data["restaurantID"]
            user_data["restaurantID"] = restaurant_ref.id
    return user_data
