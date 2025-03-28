from datetime import datetime

from beanie import Document
from bson import ObjectId
from pydantic import BaseModel, confloat, Field
from typing import Optional

from app.utils.utils import partial_model


class InvoiceBase(BaseModel):
    total: Optional[float] = 0
    generatedTime: Optional[datetime] = datetime.now().isoformat()
    sessionID: str
    orders: Optional[list[str]] = []


class InvoiceCreate(InvoiceBase):
    total: Optional[confloat(gt=0)] = Field(None)

@partial_model
class InvoiceUpdate(InvoiceBase):
    pass



class InvoiceDocument(InvoiceBase, Document):

    class Settings:
        name = "invoices"
        bson_encoders = {ObjectId: str}
        indexes = []


class InvoiceDisplay(InvoiceBase):
    id: str
    created_time: Optional[datetime]

