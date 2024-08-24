from app.schemas.tableSession import TableSessionCreate
from google.cloud.firestore_v1.document import DocumentReference
from app.crud.order import getOrder
from app.crud.table import getTable
from app.crud.restaurant import getRestaurant
from app import database
from datetime import datetime


collection_ref = database.db.collection('sessions')


def createTableSession(session: TableSessionCreate) -> DocumentReference or None:
    tableRef = getTable(session.tableID)
    tableData = tableRef.get().to_dict()
    restaurantRef = getRestaurant(session.restaurantID)
    if tableRef and restaurantRef:
        session_data = {
            "startTime": session.startTime or datetime.now(),
            "tableID": tableRef,
            "tableNumber": tableData["number"],
            "restaurantID": restaurantRef,
            "status": session.status or "Open",
        }
        ref = collection_ref.add(session_data)
        return ref[1]


def getTableSession(session_id: str) -> DocumentReference or None:
    session = collection_ref.document(session_id)
    doc = session.get()
    return session if doc.exists else None


def updateTableSession(session_id: str, update_data: dict):
    session = getTableSession(session_id)
    if session:
        session.update(update_data)
    return session


def deleteTableSession(session_id: str):
    session = getTableSession(session_id)
    if session:
        session.delete()
    return session
