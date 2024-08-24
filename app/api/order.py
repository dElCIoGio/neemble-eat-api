from fastapi import APIRouter, Depends, HTTPException, Response
from app.crud import order as order_crud
from app.schemas import order as order_schema
from app.utils import order as order_utils


router = APIRouter()


@router.post("/", response_model=order_schema.OrderDisplay)
def create_order(order: order_schema.OrderCreate):
    order_ref = order_crud.createOrder(order=order)
    order_data = order_utils.json(order_ref)
    return order_schema.OrderDisplay(**order_data)


@router.get("/{order_id}", response_model=order_schema.OrderDisplay)
def read_order(order_id: str):
    order_ref = order_crud.getOrder(order_id=order_id)
    if order_ref is None:
        raise HTTPException(status_code=404, detail="Order not found")
    order_data = order_utils.json(order_ref)
    return order_schema.OrderDisplay(**order_data)


@router.put("/{order_id}", response_model=order_schema.OrderDisplay)
def update_order(order_id: str, order: order_schema.OrderBase):
    order_ref = order_crud.updateOrder(order_id, order.dict(exclude_unset=True))
    if order_ref is None:
        raise HTTPException(status_code=404, detail="Order Session not found")
    order_data = order_utils.json(order_ref)
    return order_schema.OrderDisplay(**order_data)


@router.delete("/{order_id}", status_code=204)
def delete_order(order_id: str):
    order_ref = order_crud.deleteOrder(order_id)
    if order_ref is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return Response(status_code=204)
