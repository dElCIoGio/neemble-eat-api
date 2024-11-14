from app.crud import restaurant as restaurant_crud
from app.crud import representant as representant_crud
from app.crud import table as table_crud
from app.crud import menu as menu_crud
from app.crud import tableSession as table_session_crud
from app.schemas import table as table_schema
from app.schemas import menu as menu_shema
from app.schemas import tableSession as table_session_schema
from app.schemas import restaurant as restaurant_schema
from app.schemas import order as order_schema
from app.googleCloudStorage import uploadFile
from app.utils import order as order_service
from app.utils import tableSession as table_session_utils

from google.cloud.firestore_v1.document import DocumentReference
from datetime import datetime, timedelta, timezone
from typing import List, Tuple
from collections import defaultdict
import asyncio


async def create_restaurant(restaurant: restaurant_schema.RestaurantCreate) -> DocumentReference or None:
    restaurant_ref = await restaurant_crud.createRestaurant(restaurant)
    if restaurant_ref:
        bannerURL = uploadFile(
            file_path=restaurant.bannerURL,
            filename="banner.jpg",
            folder_path=f"{restaurant_ref.id}",
        )
        if bannerURL:
            restaurant_ref.update({"banner": bannerURL})
            return restaurant_ref
        else:
            restaurant_ref.delete()
    return None


async def assign_manager(restaurant_id: str, representant_id: str):
    restaurant_ref = await restaurant_crud.getRestaurant(restaurant_id)
    representant_ref = await representant_crud.getRepresentant(representant_id)
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
            "restaurantID": restaurant_ref
        })
        return restaurant_ref


async def add_session(table_id: str, restaurant_id: str) -> DocumentReference or None:
    restaurant_ref = await restaurant_crud.getRestaurant(restaurant_id)
    table_ref = await table_crud.getTable(table_id)
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
        session_ref = await table_session_crud.createTableSession(session)
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


async def add_table(restaurant_id: str) -> DocumentReference or None:
    restaurant_ref = await restaurant_crud.getRestaurant(restaurant_id)
    if restaurant_ref:
        restaurant_data = restaurant_ref.get().to_dict()
        if "tables" in restaurant_data:
            tables = restaurant_data["tables"]
        else:
            tables = []
        table = table_schema.TableCreate(
            restaurantID=restaurant_id,
            number=len(tables) + 1,
        )
        table_ref = await table_crud.createTable(table)
        tables.append(table_ref)
        await add_session(table_ref.id, restaurant_id)
        restaurant_ref.update({
            "tables": tables
        })
        return table_ref


async def add_menu(restaurant_id: str, menu: menu_shema.MenuCreate) -> DocumentReference or None:
    restaurant_ref = await restaurant_crud.getRestaurant(restaurant_id)
    if restaurant_ref:
        restaurant_data = restaurant_ref.get().to_dict()
        if "menus" in restaurant_data:
            menus: list[DocumentReference] = restaurant_data["menus"]
        else:
            menus: list[DocumentReference] = []
        menu_ref = await menu_crud.createMenu(menu)
        menus.append(menu_ref)
        restaurant_ref.update({
            "menus": menus
        })
        return menu_ref


async def get_orders(restaurant_id: str) -> list[DocumentReference] or None:
    restaurant_ref = await restaurant_crud.getRestaurant(restaurant_id)
    if restaurant_ref:
        restaurant_data = restaurant_ref.get().to_dict()
        if "sessions" in restaurant_data:
            all_orders: list[DocumentReference] = []
            sessions: list[DocumentReference] = restaurant_data["sessions"]
            for session in sessions:
                session_data = session.get().to_dict()
                if "orders" in session_data:
                    print(session_data["orders"])
                    orders: list[DocumentReference] = session_data["orders"]
                    all_orders += orders
            return all_orders
        return None


async def get_all_orders(restaurant_id: str) -> list[DocumentReference] or None:
    restaurant_ref = await restaurant_crud.getRestaurant(restaurant_id)
    if restaurant_ref:
        restaurant_data = restaurant_ref.get().to_dict()
        if "orders" in restaurant_data:
            return restaurant_data["orders"]
        return []


async def get_restaurant_table_open(restaurant_id: str, table_number: int) -> DocumentReference or None:
    restaurant_ref = await restaurant_crud.getRestaurant(restaurant_id)
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


async def save_order(restaurant_id: str, order: DocumentReference) -> DocumentReference or None:
    restaurant_ref = await restaurant_crud.getRestaurant(restaurant_id)
    order_exists: bool = order.get().exists
    if restaurant_ref and order_exists:
        restaurant_data = restaurant_ref.get().to_dict()
        if "orders" in restaurant_data:
            orders: list[DocumentReference] = restaurant_data["orders"]
        else:
            orders: list[DocumentReference] = []
        orders.append(order)
        restaurant_ref.update({
            "orders": orders
        })
        return restaurant_ref


async def most_ordered_last_seven_days(restaurant_id: str) -> List[Tuple[str, int]]:
    orders = await get_all_orders(restaurant_id)
    if orders:
        orders = list(map(lambda order: order_schema.OrderDisplay(**order_service.json(order)), orders))
        last_orders = filter_orders_within_last_7_days(orders)
        ranked_orders = orders_ranking(last_orders)
        return ranked_orders


def orders_ranking(orders: List[order_schema.OrderDisplay]) -> List[Tuple[str, int]]:
    # Dictionary to store the total quantity per orderedItemName
    quantity_by_item_name = defaultdict(int)

    for order in orders:
        if order.orderedItemName:  # Ensure that the orderedItemName is not None
            quantity_by_item_name[order.orderedItemName] += order.quantity

    # Create a list of tuples (orderedItemName, total quantity) sorted by quantity in descending order
    ranked_items = sorted(
        quantity_by_item_name.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return ranked_items


def filter_orders_within_last_7_days(orders: List[order_schema.OrderDisplay]) -> List[order_schema.OrderDisplay]:
    # Define the current time in UTC+1
    now_utc1 = datetime.now(timezone.utc) + timedelta(hours=1)

    # Define the time threshold (7 days ago from now)
    seven_days_ago = now_utc1 - timedelta(days=7)

    # Filter orders where orderTime is within the last 7 days
    recent_orders = [
        order for order in orders
        if order.orderTime and order.orderTime >= seven_days_ago
    ]

    return recent_orders


async def get_last_sessions(restautant_id: str) -> list[table_session_schema.TableSessionDisplay]:
    not_billed = asyncio.create_task(get_all_open_sessions(restautant_id))
    billed = asyncio.create_task(get_tables_last_billed_session(restautant_id))

    open_sessions = await not_billed
    billed_sessions = await billed
    sessions = []

    if open_sessions:
        sessions += open_sessions
    if billed_sessions:
        sessions += billed_sessions

    return sessions


async def get_all_open_sessions(restaurant_id: str) -> list[table_session_schema.TableSessionDisplay] or None:
    restaurant_ref = await restaurant_crud.getRestaurant(restaurant_id)
    if restaurant_ref:
        restaurant_data = restaurant_ref.get().to_dict()
        if "tables" in restaurant_data:
            tables: list[DocumentReference] = restaurant_data["tables"]
            open_sessions: list[table_session_schema.TableSessionDisplay] = []
            for table in tables:
                current_session = table.get().to_dict()["currentSessionID"]
                json_data = table_session_utils.json(current_session)
                open_sessions.append(table_session_schema.TableSessionDisplay(**json_data))
            return open_sessions


async def get_tables_last_billed_session(restaurant_id: str) -> list[table_session_schema.TableSessionDisplay] or None:
    billed_sessions = await get_all_billed_sessions(restaurant_id)
    #print("TUDO QUE CHEGOU DA PRIMEIRA FUNCÇÃO:", billed_sessions)
    table_number_by_session = {}

    for session in billed_sessions:
        table_number = session.tableNumber
        if table_number not in table_number_by_session:
            table_number_by_session[table_number] = session
        else:
            table_number_by_session[table_number] = session if session.created_time > table_number_by_session[table_number].created_time else table_number_by_session[table_number]

    table_numbers = list(table_number_by_session.keys())
    sessions = [table_number_by_session[table_number] for table_number in table_numbers]
    print(sessions)
    return sessions


async def get_all_billed_sessions(restaurant_id: str) -> list[table_session_schema.TableSessionDisplay] or None:
    restaurant_ref = await restaurant_crud.getRestaurant(restaurant_id)
    if restaurant_ref:
        restaurant_data = restaurant_ref.get().to_dict()
        if "sessions" in restaurant_data:
            sessions_ref = restaurant_data["sessions"]
            sessions = []
            for session_ref in sessions_ref:
                session_data = session_ref.get().to_dict()
                if session_data["status"] == "Billed":
                    sessions.append(table_session_schema.TableSessionDisplay(**table_session_utils.json(session_ref)))

            return sessions

