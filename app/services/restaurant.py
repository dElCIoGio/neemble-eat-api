from app.crud import restaurant as restaurant_crud
from app.crud import representant as representant_crud
from app.crud import table as table_crud
from app.crud import menu as menu_crud
from app.crud import tableSession as table_session_crud
from app.schemas import table as table_schema
from app.schemas import menu as menu_shema
from app.schemas import tableSession as table_session_schema
from app.schemas import restaurant as restaurant_schema
from app.services import table as table_service
from google.cloud.firestore_v1.document import DocumentReference
from app.googleCloudStorage import uploadFile


def create_restaurant(restaurant: restaurant_schema.RestaurantCreate) -> DocumentReference or None:
    restaurant_ref = restaurant_crud.createRestaurant(restaurant)
    if restaurant_ref:
        bannerURL = uploadFile(
            image_url=restaurant.bannerURL,
            filename="banner.jpg",
            folder_path=f"{restaurant_ref.id}",
        )
        if bannerURL:
            restaurant_ref.update({"banner": bannerURL})
            return restaurant_ref
        else:
            restaurant_ref.delete()
    return None


def assign_manager(restaurant_id: str, representant_id: str):
    restaurant_ref = restaurant_crud.getRestaurant(restaurant_id)
    representant_ref = representant_crud.getRepresentant(representant_id)
    if restaurant_ref and representant_ref:
        restaurant_data = restaurant_ref.get().to_dict()
        if "representants" in restaurant_data:
            representants: list[DocumentReference] = restaurant_data["representants"]
        else:
            representants: list[DocumentReference] = []
        representants.append(representant_ref)
        restaurant_ref.update({
            "representants": representants
        })
        representant_ref.update({
            "restaurant": restaurant_ref
        })
        return restaurant_ref


def add_session(table_id: str, restaurant_id: str) -> DocumentReference or None:
    restaurant_ref = restaurant_crud.getRestaurant(restaurant_id)
    table_ref = table_crud.getTable(table_id)
    if table_ref and restaurant_ref:
        restaurant_data = restaurant_ref.get().to_dict()
        if "sessions" in restaurant_data:
            sessions: list[DocumentReference] = restaurant_data["sessions"]
        else:
            sessions: list[DocumentReference] = []
        session = table_session_schema.TableSessionCreate(
            invoiceID=None,
            startTime=None,
            endTime=None,
            tableID=table_ref.id,
            tableNumber=None,
            restaurantID=restaurant_ref.id,
            orders=None,
            status=None
        )
        session_ref = table_session_crud.createTableSession(session)
        sessions.append(session_ref)
        restaurant_ref.update({
            "sessions": sessions
        })
        table_ref.update({
            "currentSessionID": session_ref,
            "sessionStatus": "Open",
            "sessionOrders": []
        })
        return session_ref


def add_table(restaurant_id: str) -> DocumentReference or None:
    restaurant_ref = restaurant_crud.getRestaurant(restaurant_id)
    if restaurant_ref:
        restaurant_data = restaurant_ref.get().to_dict()
        if "tables" in restaurant_data:
            tables: list[DocumentReference] = restaurant_data["tables"]
        else:
            tables: list[DocumentReference] = []
        table = table_schema.TableCreate(
            restaurantID=restaurant_id,
            number=len(tables) + 1,
        )
        table_ref = table_crud.createTable(table)
        tables.append(table_ref)
        add_session(table_ref.id, restaurant_id)
        restaurant_ref.update({
            "tables": tables
        })
        return table_ref


def add_menu(restaurant_id: str, menu: menu_shema.MenuCreate) -> DocumentReference or None:
    restaurant_ref = restaurant_crud.getRestaurant(restaurant_id)
    if restaurant_ref:
        restaurant_data = restaurant_ref.get().to_dict()
        if "menus" in restaurant_data:
            menus: list[DocumentReference] = restaurant_data["menus"]
        else:
            menus: list[DocumentReference] = []
        menu_ref = menu_crud.createMenu(menu)
        menus.append(menu_ref)
        restaurant_ref.update({
            "menus": menus
        })
        return restaurant_ref


def get_orders(restaurant_id: str) -> list[DocumentReference] or None:
    restaurant_ref = restaurant_crud.getRestaurant(restaurant_id)
    if restaurant_ref:
        restaurant_data = restaurant_ref.get().to_dict()
        if "sessions" in restaurant_data:
            all_orders: list[DocumentReference] = []
            sessions: list[DocumentReference] = restaurant_data["sessions"]
            for session in sessions:
                print(type(session))
                print(session)
                session_data = session.get().to_dict()
                if "orders" in session_data:
                    orders: list[DocumentReference] = session_data["orders"]
                    all_orders += orders

            return all_orders
        return None


def get_restaurant_table_open(restaurant_id: str, table_number: int) -> DocumentReference or None:
    restaurant_ref = restaurant_crud.getRestaurant(restaurant_id)
    if restaurant_ref:
        restaurant_data = restaurant_ref.get().to_dict()
        if "tables" in restaurant_data:
            tables: list[DocumentReference] = restaurant_data["tables"]
            for table_ref in tables:
                if table_ref.get().exists:
                    table_data = table_ref.get().to_dict()
                    if "number" in table_data:
                        if table_data["number"] != int(table_number):
                            continue
                        return table_data["currentSessionID"]




