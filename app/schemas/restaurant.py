from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import datetime


class RestaurantBase(BaseModel):
    name: str
    address: str
    phoneNumber: str
    orders: Optional[list[str]] = None
    representants: Optional[list[str]] = None
    bannerURL: str
    description: str
    sessions: Optional[list[str]] = None
    menus: Optional[list[str]] = None
    tables: Optional[list[str]] = None

    class Config:
        orm_mode = True


class RestaurantCreate(RestaurantBase):
    pass


class RestaurantDisplay(RestaurantBase):
    id: str
    created_time: Optional[datetime]
