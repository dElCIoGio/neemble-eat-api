from google.cloud import firestore
from google.cloud.firestore_v1 import DocumentReference
import asyncio

from app.schemas import tableSession as table_session_schema
from app.crud import restaurant as restaurant_crud
from app.crud import order as order_crud
from app.crud import tableSession as session_crud



def reset_orders_and_sessions():

    # Get all restaurant documents
    restaurants = restaurant_crud.get_all_restaurants()

    for restaurant in restaurants:
        restaurant_ref = restaurant.reference
        restaurant_ref.update({
            "orders": [],
            "sessions": []
        })
        print(f"Updated restaurant: {restaurant.id}")


def delete_orders():
    orders = order_crud.get_orders()
    for order in orders:
        order_ref = order.reference
        order_ref.delete()
        print(f"Deleted order: {order.id}")


def delete_table_sessions():
    table_sessions = session_crud.get_table_sessions()
    for table_session in table_sessions:
        table_session_ref = table_session.reference
        table_session_ref.delete()
        print(f"Deleted table session: {table_session.id}")



async def assign():
    restaurants = restaurant_crud.get_all_restaurants()
    for restaurant in restaurants:
        restaurant_ref: DocumentReference = restaurant.reference
        restaurant_id = restaurant_ref.id
        if restaurant_id == "FUHT4zQL5Umz99BN7dUI":
            restaurant_data = restaurant_ref.get().to_dict()
            tables_refs: list[DocumentReference] = restaurant_data["tables"]

            table_sessions = []

            for table_ref in tables_refs:
                table_data = table_ref.get().to_dict()
                table_session = table_session_schema.TableSessionCreate(
                    tableID=table_ref.id,
                    tableNumber=table_data["number"],
                    restaurantID=restaurant_id,
                    orders=[],
                )
                table_session_ref = await session_crud.create_table_session(table_session)
                table_sessions.append(table_session_ref)

                table_ref.update({
                    "currentSessionID": table_session_ref,
                })

                print(table_session)

            restaurant_ref.update({
                "sessions": table_sessions,
            })