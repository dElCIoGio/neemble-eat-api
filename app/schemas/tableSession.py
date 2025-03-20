from beanie import Document
from bson import ObjectId
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from app.utils.utils import partial_model


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


@partial_model
class TableSessionUpdate(TableSessionBase):
    pass




class TableSessionDisplay(TableSessionBase):
    id: str
    created_time: Optional[datetime]


class TableSessionDocument(TableSessionBase, Document):

    class Settings:
        name = "table_sessions"
        bson_encoders = {ObjectId: str}
        indexes = [
            {"keys": [("tableID", 1)], "name": "table_id_index"},
            {"keys": [("restaurantID", 1)], "name": "restaurant_id_index"},
            {"keys": [("status", 1)], "name": "session_status_index"},
            {"keys": [("startTime", -1)], "name": "session_start_time_index"},
        ]
