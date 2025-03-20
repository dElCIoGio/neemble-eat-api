from beanie import Document
from bson import ObjectId
from pydantic import BaseModel, EmailStr, constr, validator, conint, HttpUrl, confloat
from datetime import datetime
from typing import Optional

from app.utils.utils import partial_model


class TableBase(BaseModel):
    number: int
    currentSessionID: Optional[str] = None
    sessionStatus: Optional[str] = None
    sessionOrders: Optional[list[str]] = None
    restaurantID: str
    link: Optional[str] = None



class TableCreate(TableBase):
    pass


@partial_model
class TableUpdate(TableBase):
    pass


class TableDisplay(TableBase):
    id: str
    created_time: Optional[datetime]

class TableDocument(TableBase, Document):

    class Settings:
        name = "tables"
        bson_encoders = {ObjectId: str}
        indexes = [
            {"keys": [("restaurantID", 1)], "name": "restaurant_id_index"},
            {"keys": [("number", 1)], "name": "table_number_index"},
            {"keys": [("sessionStatus", 1)], "name": "session_status_index"},
        ]