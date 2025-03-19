from app.crud import restaurant as restaurant_crud
from app.crud import user as user_crud
from app.crud import table as table_crud
from app.crud import menu as menu_crud
from app.crud import tableSession as table_session_crud
from app.schemas import table as table_schema
from app.schemas import menu as menu_shema
from app.schemas import tableSession as table_session_schema
from app.schemas import restaurant as restaurant_schema
from app.schemas import order as order_schema
from app.googleCloudStorage import uploadFile
from app.utils import order as order_utils
from app.utils import tableSession as table_session_utils
from app.utils import utils

from google.cloud.firestore_v1.document import DocumentReference
from datetime import datetime, timedelta, timezone
from typing import List, Tuple
from collections import defaultdict
import asyncio

from app.utils.filter import filter_recent_documents


async def create_restaurant(restaurant: restaurant_schema.RestaurantCreate) -> DocumentReference or None:
    restaurant_ref = await restaurant_crud.create_restaurant(restaurant)
    if restaurant_ref:
        banner_url = uploadFile(
            file_path=restaurant.banner_url,
            filename="banner.jpg",
            folder_path=f"{restaurant_ref.id}",
        )
        if banner_url:
            restaurant_ref.update({"banner": banner_url})
            return restaurant_ref
        else:
            restaurant_ref.delete()
    return None


async def add_user(restaurant_id: str, user_id: str):
    restaurant_ref = await restaurant_crud.get_restaurant(restaurant_id)
    user_ref = await user_crud.get_user(user_id)
    if restaurant_ref and user_ref:
        restaurant_data = restaurant_ref.get().to_dict()
        users: list[DocumentReference] = restaurant_data["users"] if "users" in restaurant_data else []
        users.append(user_ref)
        restaurant_ref.update({
            "users": users
        })
        user_ref.update({
            "restaurantID": restaurant_ref
        })
        return restaurant_ref


async def add_session(table_id: str, restaurant_id: str) -> DocumentReference or None:
    restaurant_ref = await restaurant_crud.get_restaurant(restaurant_id)
    table_ref = await table_crud.get_table(table_id)
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
        session_ref = await table_session_crud.create_table_session(session)
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
    restaurant_ref = await restaurant_crud.get_restaurant(restaurant_id)
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
        table_ref = await table_crud.create_table(table)
        tables.append(table_ref)
        await add_session(table_ref.id, restaurant_id)
        restaurant_ref.update({
            "tables": tables
        })
        return table_ref


async def remove_table(table_id: str, restaurant_id: str) -> bool:
    table_ref = await table_crud.get_table(table_id)
    if table_ref:
        table_data = table_ref.get().to_dict()
        if "currentSessionID" in table_data:
            current_session_ref: DocumentReference = table_data["currentSessionID"]
            current_session_ref.delete()
        if "restaurantID" in table_data:
            restaurant_ref = table_data["restaurantID"]
            restaurant_ref.update({
                "tables": [ref for ref in restaurant_ref.get().to_dict()["tables"] if ref.id != table_id]
            })
        table_ref.delete()
        return True
    return False


async def add_menu(restaurant_id: str, menu: menu_shema.MenuCreate) -> DocumentReference or None:
    restaurant_ref = await restaurant_crud.get_restaurant(restaurant_id)
    if restaurant_ref:
        restaurant_data = restaurant_ref.get().to_dict()
        if "menus" in restaurant_data:
            menus: list[DocumentReference] = restaurant_data["menus"]
        else:
            menus: list[DocumentReference] = []
        menu_ref = await menu_crud.create_menu(menu)
        menus.append(menu_ref)
        restaurant_ref.update({
            "menus": menus
        })
        return menu_ref


async def get_orders(restaurant_id: str) -> list[DocumentReference] or None:
    restaurant_ref = await restaurant_crud.get_restaurant(restaurant_id)
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


async def get_all_orders(restaurant_id: str, hours: int=24) -> list[DocumentReference] or None:
    restaurant_ref = await restaurant_crud.get_restaurant(restaurant_id)
    if restaurant_ref:
        restaurant_data = restaurant_ref.get().to_dict()
        if "orders" in restaurant_data:
            orders: list[DocumentReference] = restaurant_data["orders"]

            orders_in_last_24h = filter_recent_documents(
                documents=orders,
                hours=hours
            )

            return orders_in_last_24h
        return []


async def get_restaurant_table_open(restaurant_id: str, table_number: int) -> DocumentReference or None:
    restaurant_ref = await restaurant_crud.get_restaurant(restaurant_id)
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
    restaurant_ref = await restaurant_crud.get_restaurant(restaurant_id)
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
        orders = list(map(lambda order: order_schema.OrderDisplay(**order_utils.json(order)), orders))
        last_orders = filter_orders_within_last_7_days(orders)
        ranked_orders = orders_ranking(last_orders)
        return ranked_orders
    return []


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


async def get_last_sessions(restaurant_id: str) -> list[table_session_schema.TableSessionDisplay]:
    try:
        not_billed = asyncio.create_task(get_all_open_sessions(restaurant_id))
        billed = asyncio.create_task(get_tables_last_billed_session(restaurant_id))

        open_sessions = await not_billed
        billed_sessions = await billed
    except Exception as e:
        print(e)
    else:
        print(open_sessions)
        print(billed_sessions)


        sessions = []



        if open_sessions:
            sessions += open_sessions
        if billed_sessions:
            sessions += billed_sessions

        return sessions


async def get_all_open_sessions(restaurant_id: str) -> list[table_session_schema.TableSessionDisplay] or None:
    restaurant_ref = await restaurant_crud.get_restaurant(restaurant_id)
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
    table_number_by_session = {}

    for session in billed_sessions:
        table_number = session.tableNumber
        if table_number not in table_number_by_session:
            table_number_by_session[table_number] = session
        else:
            table_number_by_session[table_number] = session if session.created_time > table_number_by_session[table_number].created_time else table_number_by_session[table_number]

    table_numbers = list(table_number_by_session.keys())
    sessions = [table_number_by_session[table_number] for table_number in table_numbers]
    return sessions


async def get_all_billed_sessions(restaurant_id: str) -> list[table_session_schema.TableSessionDisplay] or None:
    restaurant_ref = await restaurant_crud.get_restaurant(restaurant_id)
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


async def get_all_tables(restaurant_id: str) -> list[DocumentReference] or None:
    restaurant_ref: DocumentReference or None = await restaurant_crud.get_restaurant(restaurant_id)
    if restaurant_ref:
        restaurant_data = restaurant_ref.get().to_dict()
        if "tables" in restaurant_data:
            return restaurant_data["tables"]
        else:
            restaurant_crud.update_restaurant(
                restaurant_id,
                {
                    "tables": []
                })
            return []
    return None


async def get_all_users(restaurant_id: str) -> List[DocumentReference]:
    restaurant_ref: DocumentReference or None = await restaurant_crud.get_restaurant(restaurant_id)
    if restaurant_ref:
        restaurant_data = restaurant_ref.get().to_dict()
        users: List[DocumentReference] = restaurant_data["users"] if "users" in restaurant_data else []
        return users
    return []


async def reset_month_orders(restaurant_id: str):
    restaurant_ref: DocumentReference or None = await restaurant_crud.get_restaurant(restaurant_id)
    if restaurant_ref:
        restaurant_data = restaurant_ref.get().to_dict()
        combined_orders = []
        if "orders" in restaurant_data:
            orders: list[DocumentReference] = restaurant_data["orders"]
            current_month_orders: List[DocumentReference] = utils.get_documents_created_this_month(orders)
            last_month_orders: List[DocumentReference] = utils.get_documents_created_last_month(orders)
            combined_orders = current_month_orders + last_month_orders
            
        restaurant_ref.update({
            "orders": list(map(lambda order: order_utils.json(order), combined_orders)),
        })
        return True
    return False


