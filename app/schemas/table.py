from pydantic import BaseModel, EmailStr, constr, validator, conint, HttpUrl, confloat
from datetime import datetime
from typing import Optional
from google.cloud.firestore_v1.document import DocumentReference


class TableBase(BaseModel):
    number: int
    currentSessionID: Optional[str] = None
    sessionStatus: Optional[str] = None
    sessionOrders: Optional[list[str]] = None
    restaurantID: str
    link: Optional[str] = None

    class Config:
        orm_mode = True


class TableCreate(TableBase):
    pass


class TableDisplay(TableBase):
    id: str
    created_time: Optional[datetime]

