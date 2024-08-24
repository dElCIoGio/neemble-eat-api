from pydantic import BaseModel, EmailStr, constr, validator, conint, HttpUrl, confloat
from datetime import datetime
from typing import Optional


class MenuItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    categoryID: str
    availability: Optional[bool] = None
    price: float
    imageURL: str

    class Config:
        orm_mode = True


class MenuItemCreate(MenuItemBase):
    name: constr(min_length=1)
    price: confloat(gt=0)


class MenuItemDisplay(MenuItemBase):
    id: str
    created_time: Optional[datetime]

