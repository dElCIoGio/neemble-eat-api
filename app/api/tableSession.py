from fastapi import APIRouter, HTTPException, Response
from app.crud import tableSession as table_session_crud
from app.schemas import tableSession as table_session_schema
from app.schemas import order as order_schema
from app.utils import tableSession as table_session_utils
from app.services import tableSession as session_service
from app.utils import order as order_utils
from app.services import invoice as invoice_service
from google.cloud.firestore_v1.document import DocumentReference

from app.websocket.manager import manager

import json


router = APIRouter()


@router.post("/", response_model=table_session_schema.TableSessionDisplay)
async def create_table_session(session: table_session_schema.TableSessionCreate):
    table_session_ref: DocumentReference = await table_session_crud.create_table_session(session=session)
    if table_session_ref is None:
        raise HTTPException(status_code=400, detail="There was an error creating the Session")
    table_session_data = table_session_utils.json(table_session_ref)
    return table_session_schema.TableSessionDisplay(**table_session_data)


@router.get("/{session_id}", response_model=table_session_schema.TableSessionDisplay)
async def read_table_session(session_id: str):
    table_session_ref = await table_session_crud.get_table_session(session_id=session_id)
    if table_session_ref is None:
        raise HTTPException(status_code=404, detail="Table session not found")
    table_session_data = table_session_utils.json(table_session_ref)
    return table_session_schema.TableSessionDisplay(**table_session_data)


@router.put("/{session_id}", response_model=table_session_schema.TableSessionDisplay)
async def update_table_session(session_id: str, table_session: table_session_schema.TableSessionBase):
    table_session_ref = await table_session_crud.update_table_session(session_id, table_session.model_dump(exclude_unset=True))
    if table_session_ref is None:
        raise HTTPException(status_code=404, detail="Table Session not found")
    table_session_data = table_session_utils.json(table_session_ref)
    return table_session_schema.TableSessionDisplay(**table_session_data)


@router.delete("/{session_id}", status_code=204)
async def delete_table_session(session_id: str):
    table_session_ref = await table_session_crud.delete_table_session(session_id)
    if table_session_ref is None:
        raise HTTPException(status_code=404, detail="Table Session not found")
    return Response(status_code=204)


# Service


@router.put("/{session_id}/orders", response_model=order_schema.OrderDisplay)
async def add_order(session_id: str, order: order_schema.OrderCreate):
    try:
        result = await session_service.add_order(session_id, order)
    except Exception as error:
        print(error)
    else:
        if result is None:
            raise HTTPException(status_code=404, detail="Table session not found")

        order_ref, restaurant_id = result

        order_data = order_utils.json(order_ref)

        copy_data = order_data.copy()
        copy_data["orderTime"] = copy_data["orderTime"].isoformat()
        json_data = json.dumps(copy_data)

        print(order_data)

        try:
            await manager.broadcast(json_data, f'{restaurant_id}/order')
            await manager.broadcast(json_data, f"{restaurant_id}/session_order")
        except Exception as error:
            print(error)

        return order_schema.OrderDisplay(**order_data)


@router.post("/{session_id}/{status}/orders", response_model=table_session_schema.TableSessionDisplay)
async def close_session(session_id: str, status: str):
    result = await session_service.close_session(session_id, status)
    if result is None:
        raise HTTPException(status_code=404, detail="Table session not found")

    invoice_ref, restaurant_id, new_session_ref = result

    new_session_data = table_session_utils.json(new_session_ref)

    try:
        orders_ref = invoice_ref.get().to_dict()["orders"]
        orders = await invoice_service.get_orders(orders_ref)
        json_data = json.dumps(orders)
        await manager.broadcast(json_data, f"{restaurant_id}/billed")
    except Exception as error:
        print(error)

    try:
        new_session = await table_session_crud.get_table_session(new_session_ref.id)
        session_data = table_session_utils.serialize(new_session)
        json_data = json.dumps(session_data)
        await manager.broadcast(json_data, f"{restaurant_id}/closed_session")
    except Exception as error:
        print(error)

    return table_session_schema.TableSessionDisplay(**new_session_data)


@router.get("/{session_id}/orders", response_model=list[order_schema.OrderDisplay])
async def get_orders(session_id: str):
    orders = await session_service.get_orders(session_id)
    if orders is None:
        raise HTTPException(status_code=404, detail="Table session not found")
    orders = list(map(lambda order: order_schema.OrderDisplay(**order_utils.json(order)), orders))
    return orders
