from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TableSessionBase(BaseModel):
    invoiceID: Optional[str] = None
    startTime: Optional[datetime] = None
    endTime: Optional[datetime] = None
    tableID: str
    tableNumber: Optional[int] = None
    restaurantID: str
    orders: Optional[list[str]] = None
    status: Optional[str] = None
    total: Optional[float] = None

    class Config:
        orm_mode = True 


class TableSessionCreate(TableSessionBase):
    pass


class TableSessionDisplay(TableSessionBase):
    id: str
    created_time: Optional[datetime]


