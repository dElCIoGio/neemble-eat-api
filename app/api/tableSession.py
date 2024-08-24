from fastapi import APIRouter, Depends, HTTPException, Response
from app.crud import tableSession as table_session_crud
from app.schemas import tableSession as table_session_schema
from app.schemas import order as order_schema
from app.schemas import invoice as invoice_schema
from app.utils import tableSession as table_session_utils
from app.utils import invoice as invoice_utils
from app.services import tableSession as session_service
from app.utils import order as order_utils
from google.cloud.firestore_v1.document import DocumentReference

router = APIRouter()


@router.post("/", response_model=table_session_schema.TableSessionDisplay)
def create_table_session(session: table_session_schema.TableSessionCreate):
    table_session_ref: DocumentReference = table_session_crud.createTableSession(session=session)
    if table_session_ref is None:
        raise HTTPException(status_code=400, detail="There was an error creating the Session")
    table_session_data = table_session_utils.json(table_session_ref)
    return table_session_schema.TableSessionDisplay(**table_session_data)


@router.get("/{session_id}", response_model=table_session_schema.TableSessionDisplay)
def read_table_session(session_id: str):
    table_session_ref = table_session_crud.getTableSession(session_id=session_id)
    if table_session_ref is None:
        raise HTTPException(status_code=404, detail="Table session not found")
    table_session_data = table_session_utils.json(table_session_ref)
    return table_session_schema.TableSessionDisplay(**table_session_data)


@router.put("/{session_id}", response_model=table_session_schema.TableSessionDisplay)
def update_table_session(session_id: str, table_session: table_session_schema.TableSessionBase):
    table_session_ref = table_session_crud.updateTableSession(session_id, table_session.dict(exclude_unset=True))
    if table_session_ref is None:
        raise HTTPException(status_code=404, detail="Table Session not found")
    table_session_data = table_session_utils.json(table_session_ref)
    return table_session_schema.TableSessionDisplay(**table_session_data)


@router.delete("/{session_id}", status_code=204)
def delete_table_session(session_id: str):
    table_session_ref = table_session_crud.deleteTableSession(session_id)
    if table_session_ref is None:
        raise HTTPException(status_code=404, detail="Table Session not found")
    return Response(status_code=204)


# Service

@router.put("/{session_id}/orders", response_model=table_session_schema.TableSessionDisplay)
def add_order(session_id: str, order: order_schema.OrderCreate):
    print(order)
    table_session_ref = session_service.add_order(session_id, order)
    if table_session_ref is None:
        raise HTTPException(status_code=404, detail="Table session not found")
    table_session_data = table_session_utils.json(table_session_ref)
    return table_session_schema.TableSessionDisplay(**table_session_data)


@router.post("/{session_id}/orders", response_model=invoice_schema.InvoiceDisplay)
def close_session(session_id: str):
    invoice_ref = session_service.close_session(session_id)
    if invoice_ref is None:
        raise HTTPException(status_code=404, detail="Table session not found")
    invoice_data = invoice_utils.json(invoice_ref)
    return invoice_schema.InvoiceDisplay(**invoice_data)


@router.get("/{session_id}/orders", response_model=list[order_schema.OrderDisplay])
def get_orders(session_id: str):
    orders = session_service.get_orders(session_id)
    if orders is None:
        raise HTTPException(status_code=404, detail="Table session not found")
    orders = list(map(lambda order: order_schema.OrderDisplay(**order_utils.json(order)), orders))
    return orders

