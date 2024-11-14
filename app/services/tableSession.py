from typing import Optional
from app.crud import tableSession as table_session_crud
from app.crud import order as order_crud
from app.crud import invoice as invoice_crud
from app.schemas import order as order_schema
from app.schemas import invoice as invoice_schema
from app.schemas import tableSession as table_session_schema
from app.services import restaurant as restaurant_service
from datetime import timedelta
from google.cloud.firestore_v1.document import DocumentReference
from datetime import datetime, timezone
from schemas.tableSession import TableSessionBase


async def add_order(session_id: str, order: order_schema.OrderCreate) -> tuple[DocumentReference, str] or None:
    session_ref = await table_session_crud.getTableSession(session_id)
    if session_ref:
        session_data = session_ref.get().to_dict()
        order_ref = await order_crud.createOrder(order)
        if order_ref:
            order_data = order_ref.get().to_dict()
            if "orders" in session_data:
                orders: list[DocumentReference] = session_data["orders"]
            else:
                orders: list[DocumentReference] = []

            if "total" in session_data:
                total = session_data["total"]
            else:
                total = 0
            total += order_data["total"]

            orders.append(order_ref)
            session_ref.update({
                "orders": orders,
                "total": total
            })

            restaurant_id = session_data["restaurantID"].id
            await restaurant_service.save_order(restaurant_id=restaurant_id, order=order_ref)

            return order_ref, restaurant_id
    return None


async def close_session(session_id: str, status: str) -> Optional[tuple[DocumentReference, str, DocumentReference]]:
    session_ref = await table_session_crud.getTableSession(session_id)
    if session_ref:
        session_data = session_ref.get().to_dict()
        if "orders" in session_data:
            if session_data["status"] == "Open" and len(session_data["orders"]) != 0:
                invoice = invoice_schema.InvoiceCreate(
                    sessionID=session_ref.id,
                    total=None,
                    generatedTime=None,
                    orders=None
                )
                invoice_ref = await invoice_crud.createInvoice(invoice)
                session_ref.update({
                    "invoiceID": invoice_ref,
                    "status": status,
                    "endTime": datetime.now()
                })

                # new session
                session_data = session_ref.get().to_dict()
                table_ref: DocumentReference = session_data["tableID"]
                restaurant_ref: DocumentReference = session_data["restaurantID"]
                new_session = table_session_schema.TableSessionCreate(
                    invoiceID=None,
                    startTime=None,
                    endTime=None,
                    tableID=table_ref.id,
                    tableNumber=None,
                    restaurantID=restaurant_ref.id,
                    orders=None,
                    status=None,
                    total=None
                )
                new_session_ref = await table_session_crud.createTableSession(new_session)
                table_ref.update({
                    "currentSessionID": new_session_ref,
                    "sessionStatus": "Open",
                    "sessionOrders": []
                })

                restaurant_data = restaurant_ref.get().to_dict()
                if "sessions" in restaurant_data:
                    restaurant_sessions = restaurant_data["sessions"]
                else:
                    restaurant_sessions = []

                restaurant_sessions.append(new_session_ref)
                restaurant_ref.update({
                    "sessions": restaurant_sessions
                })

                return invoice_ref, restaurant_ref.id, new_session_ref


async def get_orders(table_session_id: str) -> list[DocumentReference] or None:
    table_session_ref = await table_session_crud.getTableSession(table_session_id)
    if table_session_ref:
        table_session_data = table_session_ref.get().to_dict()
        if "orders" in table_session_data:
            return table_session_data["orders"]
        return []


def has_minutes_passed(table_session_json: dict, minutes: int) -> bool:
    try:
        # Parse the JSON to a TableSessionBase object
        table_session = TableSessionBase(**table_session_json)

        # Check if startTime is provided
        if table_session.startTime is None:
            return False
        # Calculate the difference between now and the start time
        time_difference = datetime.now(timezone.utc) - table_session.startTime
        # Check if the time difference is greater than or equal to the specified minutes
        return time_difference >= timedelta(minutes=minutes)
    except Exception as e:
        print(e)
        # If any error occurs, return False
        return False


print(has_minutes_passed({
    "invoiceID": None,
    "startTime": "2024-09-26T12:18:12.156283Z",
    "endTime": None,
    "tableID": "yGWqbx21CeGFNshYY4kw",
    "tableNumber": 1,
    "restaurantID": "FUHT4zQL5Umz99BN7dUI",
    "orders": None,
    "status": "Open",
    "total": 0.0,
    "id": "1cqGZBbSPr0GAAlW46C4",
    "created_time": "2024-11-13T12:18:12.171921Z"
},
60))