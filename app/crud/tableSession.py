from app.schemas.tableSession import TableSessionCreate
from google.cloud.firestore_v1.document import DocumentReference
from app.crud.table import getTable
from app.crud.restaurant import getRestaurant
from app import database
from datetime import datetime


collection_ref = database.db.collection('sessions')


async def createTableSession(session: TableSessionCreate) -> DocumentReference or None:
    tableRef = await getTable(session.tableID)
    tableData = tableRef.get().to_dict()
    restaurantRef = await getRestaurant(session.restaurantID)
    if tableRef and restaurantRef:
        session_data = {
            "startTime": session.startTime or datetime.now(),
            "tableID": tableRef,
            "tableNumber": tableData["number"],
            "restaurantID": restaurantRef,
            "status": session.status or "Open",
            "total": 0.0
        }
        ref = collection_ref.add(session_data)
        return ref[1]


async def getTableSession(session_id: str) -> DocumentReference or None:
    session = collection_ref.document(session_id)
    doc = session.get()
    return session if doc.exists else None


async def asyncGetTableSession(session_id: str) -> DocumentReference or None:
    session = collection_ref.document(session_id)
    doc = session.get()
    return session if doc.exists else None


async def updateTableSession(session_id: str, update_data: dict):
    session = await getTableSession(session_id)
    if session:
        session.update(update_data)
    return session


async def deleteTableSession(session_id: str):
    session = await getTableSession(session_id)
    if session:
        session.delete()
    return session
