from google.cloud.firestore_v1.document import DocumentReference


def json(restaurant_ref: DocumentReference):
    restaurant_data = restaurant_ref.get().to_dict()
    restaurant_data["id"] = restaurant_ref.id
    restaurant_data["created_time"] = restaurant_ref.get().create_time.isoformat()
    print(restaurant_data)
    if "menus" in restaurant_data:
        menus: list[DocumentReference] = restaurant_data["menus"]
        menus = list(map(lambda menu: menu.id, menus))
        restaurant_data["menus"] = menus
    if "tables" in restaurant_data:
        tables: list[DocumentReference] = restaurant_data["tables"]
        tables = list(map(lambda table: table.id, tables))
        restaurant_data["tables"] = tables
    if "representants" in restaurant_data:
        representants: list[DocumentReference] = restaurant_data["representants"]
        representants = list(map(lambda representant: representant.id, representants))
        restaurant_data["representants"] = representants
    if "sessions" in restaurant_data:
        sessions: list[DocumentReference] = restaurant_data["sessions"]
        sessions = list(map(lambda session: session.id, sessions))
        restaurant_data["sessions"] = sessions
    if "orders" in restaurant_data:
        orders: list[DocumentReference] = restaurant_data["orders"]
        orders = list(map(lambda order: order.id, orders))
        restaurant_data["orders"] = orders
    return restaurant_data
