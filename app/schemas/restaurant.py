from beanie import Document
from bson import ObjectId
from fastapi import UploadFile
from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import datetime
from app.schemas import menu as menu_schema
from app.schemas.document_id import DocumentId
from app.utils.utils import partial_model


class RestaurantBase(BaseModel):
    name: str
    address: str
    phoneNumber: str
    orders: Optional[list[str]] = []
    users: Optional[list[str]] = []
    bannerURL: str
    description: str
    sessions: Optional[list[str]] = []
    menus: Optional[list[str]] = []
    tables: Optional[list[str]] = []


class RestaurantCreate(RestaurantBase):
    pass


@partial_model
class RestaurantUpdate(RestaurantBase):
    pass


class Restaurant(RestaurantBase, DocumentId):
    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }


class RestaurantDocument(RestaurantBase, Document):

    class Settings:
        name = "restaurants"
        bson_encoders = {ObjectId: str}
        indexes = [
            {"keys": [("name", 1)], "name": "restaurant_name_index"},
            {"keys": [("address", 1)], "name": "restaurant_address_index"},
            {"keys": [("phoneNumber", 1)], "name": "restaurant_phone_index"},
        ]


class RestaurantDisplay(RestaurantBase):
    id: str
    created_time: Optional[datetime]


class RestaurantNew(RestaurantBase):
    bannerURL: UploadFile
    menus: Optional[list[menu_schema.MenuNew]] = []