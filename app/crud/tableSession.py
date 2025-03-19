from app.schemas.tableSession import TableSessionCreate
from google.cloud.firestore_v1.document import DocumentReference
from app.crud.table import get_table
from app.crud.restaurant import get_restaurant
from app.db import table_sessions_collection_ref
from datetime import datetime


async def create_table_session(session: TableSessionCreate) -> DocumentReference or None:
    table_ref = await get_table(session.tableID)
    table_data = table_ref.get().to_dict()
    restaurant_ref = await get_restaurant(session.restaurantID)
    if table_ref and restaurant_ref:
        session_data = {
            "startTime": session.startTime or datetime.now(),
            "tableID": table_ref,
            "tableNumber": table_data["number"],
            "restaurantID": restaurant_ref,
            "status": session.status or "Open",
            "total": 0.0
        }
        ref = table_sessions_collection_ref.add(session_data)
        return ref[1]


async def get_table_session(session_id: str) -> DocumentReference or None:
    session = table_sessions_collection_ref.document(session_id)
    doc = session.get()
    return session if doc.exists else None


def get_table_sessions():
    return table_sessions_collection_ref.get()


async def update_table_session(session_id: str, update_data: dict):
    session = await get_table_session(session_id)
    if session:
        session.update(update_data)
    return session


async def delete_table_session(session_id: str):
    session = await get_table_session(session_id)
    if session:
        session.delete()
    return session
