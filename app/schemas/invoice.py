from datetime import datetime
from pydantic import BaseModel, confloat, Field
from typing import Optional


class InvoiceBase(BaseModel):
    total: Optional[float] = None
    generatedTime: Optional[datetime] = None
    sessionID: str
    orders: Optional[list[str]] = None

    class Config:
        orm_mode = True


class InvoiceCreate(InvoiceBase):
    total: Optional[confloat(gt=0)] = Field(None)


class InvoiceDisplay(InvoiceBase):
    id: str
    created_time: Optional[datetime]