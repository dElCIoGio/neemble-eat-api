from app.crud import tableSession as table_session_crud
from app.crud import order as order_crud
from app.crud import invoice as invoice_crud
from app.schemas import order as order_schema
from app.schemas import invoice as invoice_schema
from app.schemas import tableSession as table_session_schema
from google.cloud.firestore_v1.document import DocumentReference
from datetime import datetime


def add_order(session_id: str, order: order_schema.OrderCreate) -> DocumentReference or None:
    session_ref = table_session_crud.getTableSession(session_id)
    if session_ref:
        session_data = session_ref.get().to_dict()
        order_ref = order_crud.createOrder(order)
        if order_ref:
            if "orders" in session_data:
                orders: list[DocumentReference] = session_data["orders"]
            else:
                orders: list[DocumentReference] = []
            orders.append(order_ref)
            session_ref.update({
                "orders": orders
            })
            return session_ref


def close_session(session_id: str) -> DocumentReference:
    session_ref = table_session_crud.getTableSession(session_id)
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
                invoice_ref = invoice_crud.createInvoice(invoice)
                session_ref.update({
                    "invoiceID": invoice_ref,
                    "status": "Billed",
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
                )
                new_session_ref = table_session_crud.createTableSession(new_session)
                table_ref.update({
                    "currentSessionID": new_session_ref,
                    "sessionStatus": "Open",
                    "sessionOrders": []
                })
                return invoice_ref


def get_orders(table_session_id: str) -> list[DocumentReference] or None:
    table_session_ref = table_session_crud.getTableSession(table_session_id)
    if table_session_ref:
        table_session_data = table_session_ref.get().to_dict()
        if "orders" in table_session_data:
            return table_session_data["orders"]
        return []