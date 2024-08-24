from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import datetime


class RestaurantBase(BaseModel):
    name: str
    address: str = None
    phoneNumber: str
    representants: Optional[list[str]]
    bannerURL: str
    description: str
    sessions: Optional[list[str]]
    menus: Optional[list[str]]
    tables: Optional[list[str]]

    class Config:
        orm_mode = True


class RestaurantCreate(RestaurantBase):
    name: constr(min_length=5, max_length=50)
    phoneNumber: constr(min_length=9)


class RestaurantDisplay(RestaurantBase):
    id: str
    created_time: Optional[datetime]
