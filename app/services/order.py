from app.crud import order as order_crud
from google.cloud.firestore_v1.document import DocumentReference
from app.services import tableSession as table_session_service

from fastapi import BackgroundTasks
from asyncio import Event


event = Event()


async def set_order_as_in_preparation(order_id: str) -> DocumentReference or None:
    order_ref = await order_crud.updateOrder(order_id, {"prepStatus": "In Progress"})
    return order_ref


async def close_session(session_id: str):
    await event.wait()
    await table_session_service.close_session(session_id, "Cancelled")
    event.clear()


async def cancel_order(order_id: str, background_tasks: BackgroundTasks) -> DocumentReference or None:
    order_ref = await order_crud.updateOrder(order_id, {"prepStatus": "Cancelled"})
    order_data = order_ref.get().to_dict()
    session_ref: DocumentReference = order_data["sessionID"]

    background_tasks.add_task(close_session, session_ref.id)

    session_data = session_ref.get().to_dict()
    if "total" in session_data:
        total: float = session_data["total"]
        total -= order_data["total"]
        if total <= 0:
            event.set()
        session_ref.update({"total": total})
    return order_ref


async def set_order_as_done(order_id: str) -> DocumentReference or None:
    order_ref = await order_crud.updateOrder(order_id, {"prepStatus": "Done"})
    return order_ref

