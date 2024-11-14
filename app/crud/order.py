from app.schemas.order import OrderCreate
from google.cloud.firestore_v1.document import DocumentReference
from app import database
from datetime import datetime

collection_ref = database.db.collection('orders')


async def createOrder(order: OrderCreate) -> DocumentReference:
    itemRef = database.db.collection("menu items").document(order.itemID)
    itemExists = itemRef.get().exists
    sessionRef = database.db.collection("sessions").document(order.sessionID)
    sessionExists = sessionRef.get().exists
    if itemExists and sessionExists:
        order_data = {
            "sessionID": sessionRef,
            "orderTime": order.orderTime or datetime.now(),
            "itemID": itemRef,
            "orderedItemName": itemRef.get().to_dict()["name"],
            "unitPrice": itemRef.get().to_dict()["price"],
            "quantity": order.quantity,
            "total": float(itemRef.get().to_dict()["price"] * order.quantity),
            "delivered": False,
            "prepStatus": order.prepStatus or "New",
            "tableNumber": sessionRef.get().to_dict()["tableNumber"],
            "sessionStatus": sessionRef.get().to_dict()["status"],
            "additionalNote": order.additionalNote or ""
        }
        ref = collection_ref.add(order_data)
        return ref[1]


async def getOrder(order_id: str) -> DocumentReference or None:
    order = collection_ref.document(order_id)
    doc = order.get()
    return order if doc.exists else None


async def updateOrder(order_id: str, update_data: dict):
    order = await getOrder(order_id)
    if order:
        order.update(update_data)
    return order


async def deleteOrder(order_id: str):
    order = await getOrder(order_id)
    if order:
        order.delete()
    return order
