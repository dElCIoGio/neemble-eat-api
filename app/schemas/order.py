from pydantic import BaseModel, EmailStr, constr, validator, conint, HttpUrl, confloat
from typing import Optional
from datetime import datetime


class OrderBase(BaseModel):
    sessionID: str
    orderTime: Optional[datetime] = None
    itemID: str
    unitPrice: Optional[float] = None
    total: Optional[float] = None
    orderedItemName: Optional[str] = None
    quantity: int
    delivered: Optional[bool] = None
    prepStatus: Optional[str] = None
    tableNumber: Optional[int] = None
    sessionStatus: Optional[str] = None
    additionalNote: Optional[str] = None

    class Config:
        orm_mode = True


class OrderCreate(OrderBase):
    pass


class OrderDisplay(OrderBase):
    id: str
    created_time: Optional[datetime]
