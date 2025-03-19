from beanie import Document
from bson import ObjectId
from pydantic import BaseModel, EmailStr, constr, validator, conint, HttpUrl, confloat
from typing import Optional
from datetime import datetime

from app.schemas.document_id import DocumentId
from utils.utils import partial_model


class OrderBase(BaseModel):
    sessionID: str
    orderTime: Optional[datetime] = None
    itemID: str
    unitPrice: Optional[float] = 0.0
    total: Optional[float] = 0.0
    orderedItemName: Optional[str] = None
    quantity: int
    delivered: Optional[bool] = False
    prepStatus: Optional[str] = None
    tableNumber: Optional[int] = None
    sessionStatus: Optional[str] = None
    additionalNote: Optional[str] = None


class OrderCreate(OrderBase):
    pass

@partial_model
class OrderUpdate(OrderBase):
    pass


class Order(OrderBase, DocumentId):
    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }


class OrderDisplay(OrderBase):
    id: str
    created_time: Optional[datetime]


class OrderDocument(OrderBase, Document):

    class Settings:
        name = "orders"
        bson_encoders = {ObjectId: str}
        indexes = [
            {"keys": [("sessionID", 1)], "name": "session_index"},
            {"keys": [("orderTime", -1)], "name": "order_time_index"},
            {"keys": [("prepStatus", 1)], "name": "prep_status_index"},
            {"keys": [("delivered", 1)], "name": "delivered_index"},
            {"keys": [("tableNumber", 1)], "name": "table_number_index"},
        ]