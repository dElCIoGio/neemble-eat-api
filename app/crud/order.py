from app.schemas.order import OrderCreate
from google.cloud.firestore_v1.document import DocumentReference
from app.db import orders_collection_ref, menu_items_collection_ref, table_sessions_collection_ref
from datetime import datetime


async def create_order(order: OrderCreate) -> DocumentReference:
    item_ref = menu_items_collection_ref.document(order.itemID)
    item_exists = item_ref.get().exists
    session_ref = table_sessions_collection_ref.document(order.sessionID)
    session_exists = session_ref.get().exists
    if item_exists and session_exists:
        order_data = {
            "sessionID": session_ref,
            "orderTime": order.orderTime or datetime.now(),
            "itemID": item_ref,
            "orderedItemName": item_ref.get().to_dict()["name"],
            "unitPrice": item_ref.get().to_dict()["price"],
            "quantity": order.quantity,
            "total": float(item_ref.get().to_dict()["price"] * order.quantity),
            "delivered": False,
            "prepStatus": order.prepStatus or "New",
            "tableNumber": session_ref.get().to_dict()["tableNumber"],
            "sessionStatus": session_ref.get().to_dict()["status"],
            "additionalNote": order.additionalNote or ""
        }
        ref = orders_collection_ref.add(order_data)
        return ref[1]


async def get_order(order_id: str) -> DocumentReference or None:
    order = orders_collection_ref.document(order_id)
    doc = order.get()
    return order if doc.exists else None

def get_orders():
    return orders_collection_ref.get()


async def update_order(order_id: str, update_data: dict):
    order = await get_order(order_id)
    if order:
        order.update(update_data)
    return order


async def delete_order(order_id: str):
    order = await get_order(order_id)
    if order:
        order.delete()
    return order
