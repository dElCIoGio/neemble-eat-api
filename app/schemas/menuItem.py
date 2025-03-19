from beanie import Document
from bson import ObjectId
from fastapi import UploadFile
from pydantic import BaseModel, constr, confloat
from datetime import datetime
from typing import Optional

from app.schemas.document_id import DocumentId
from app.utils.utils import partial_model


class MenuItemBase(BaseModel):
    name: str
    description: Optional[str] = ""
    categoryID: str
    availability: Optional[bool] = True
    price: float
    imageURL: str


class MenuItemCreate(MenuItemBase):
    name: constr(min_length=1)
    price: confloat(gt=0)


@partial_model
class MenuItemUpdate(MenuItemBase):
    pass


class MenuItem(MenuItemBase, DocumentId):
    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }


class MenuItemDocument(MenuItemBase, Document):

    class Settings:
        name = "menu_items"
        bson_encoders = {ObjectId: str}
        indexes = [
            {"keys": [("categoryID", 1)], "name": "category_index"},
            {"keys": [("price", 1)], "name": "price_index"},
            {"keys": [("availability", 1)], "name": "availability_index"},
        ]


class MenuItemDisplay(MenuItemBase):
    id: str
    created_time: Optional[datetime]


class MenuItemNew(MenuItemBase):
    imageURL: UploadFile
    categoryID: None