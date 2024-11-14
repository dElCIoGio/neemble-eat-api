from app.utils import order as order_utils
from google.cloud.firestore_v1.document import DocumentReference


async def get_orders(orders: list[DocumentReference]):
    for index, order in enumerate(orders):
        order = order_utils.json(order)
        order["orderTime"] = order["orderTime"].isoformat()
        orders[index] = order
    return orders
