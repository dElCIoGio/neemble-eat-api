from pydantic import BaseModel, constr
from typing import Optional
from datetime import datetime


class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    menuID: str
    items: Optional[list[str]] = None

    class Config:
        orm_mode = True


class CategoryCreate(CategoryBase):
    name: constr(strip_whitespace=True, min_length=1)  # Ensure the name is not empty and whitespace is handled


class CategoryDisplay(CategoryBase):
    id: str
    created_time: Optional[datetime]
