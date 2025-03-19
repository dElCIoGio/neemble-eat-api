from fastapi import APIRouter, Depends, HTTPException, Response
from app.crud import order as order_crud
from app.schemas import order as order_schema
from app.utils import order as order_utils
from app.services import order as order_service

from fastapi import BackgroundTasks


router = APIRouter()


@router.post("/", response_model=order_schema.OrderDisplay)
async def create_order(order: order_schema.OrderCreate):
    order_ref = await order_crud.create_order(order=order)
    if order_ref is None:
        raise HTTPException(status_code=404, detail="Order not created")
    order_data = order_utils.json(order_ref)
    return order_schema.OrderDisplay(**order_data)


@router.get("/{order_id}", response_model=order_schema.OrderDisplay)
async def read_order(order_id: str):
    order_ref = await order_crud.get_order(order_id=order_id)
    if order_ref is None:
        raise HTTPException(status_code=404, detail="Order not found")
    order_data = order_utils.json(order_ref)
    return order_schema.OrderDisplay(**order_data)


@router.put("/{order_id}", response_model=order_schema.OrderDisplay)
async def update_order(order_id: str, order: order_schema.OrderBase):
    order_ref = await order_crud.update_order(order_id, order.model_dump(exclude_unset=True))
    if order_ref is None:
        raise HTTPException(status_code=404, detail="Order Session not found")
    order_data = order_utils.json(order_ref)
    return order_schema.OrderDisplay(**order_data)


@router.delete("/{order_id}", status_code=204)
async def delete_order(order_id: str):
    order_ref = await order_crud.delete_order(order_id)
    if order_ref is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return Response(status_code=204)


# Service


@router.put("/{order_id}/in-progress", response_model=order_schema.OrderDisplay)
async def set_order_as_in_preparation(order_id: str):
    order_ref = await order_service.set_order_as_in_preparation(order_id)
    if order_ref is None:
        raise HTTPException(status_code=404, detail="Order not found")
    order_data = order_utils.json(order_ref)
    return order_schema.OrderDisplay(**order_data)


@router.put("/{order_id}/cancel", response_model=order_schema.OrderDisplay)
async def cancel_order(order_id: str, background_tasks: BackgroundTasks):
    order_ref = await order_service.cancel_order(order_id, background_tasks)
    if order_ref is None:
        raise HTTPException(status_code=404, detail="Order not found")
    order_data = order_utils.json(order_ref)
    return order_schema.OrderDisplay(**order_data)


@router.put("/{order_id}/done", response_model=order_schema.OrderDisplay)
async def set_order_as_done(order_id: str):
    order_ref = await order_service.set_order_as_done(order_id)
    if order_ref is None:
        raise HTTPException(status_code=404, detail="Order not found")
    order_data = order_utils.json(order_ref)
    return order_schema.OrderDisplay(**order_data)

