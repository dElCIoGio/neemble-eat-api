from pydantic import BaseModel, EmailStr, constr, validator, conint, HttpUrl, confloat
from typing import Optional
from datetime import datetime


class MenuBase(BaseModel):
    restaurantID: str
    name: str
    description: Optional[str] = None
    categories: Optional[list[str]] = None

    class Config:
        orm_mode = True


class MenuCreate(MenuBase):
    pass


class MenuDisplay(MenuBase):
    id: str
    created_time: Optional[datetime]
