from beanie import Document
from bson import ObjectId
from pydantic import BaseModel, constr
from typing import Optional, List
from datetime import datetime
from app.schemas import menuItem as menu_item_schema
from schemas.document_id import DocumentId
from utils.utils import partial_model


class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = ""
    menuID: str
    items: Optional[list[str]] = []


class CategoryCreate(CategoryBase):
    pass


@partial_model
class CategoryUpdate(CategoryBase):
    pass


class Category(CategoryBase, DocumentId):
    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }


class CategoryDisplay(CategoryBase):
    id: str
    created_time: Optional[datetime]


class CategoryNew(CategoryBase):
    items: List[menu_item_schema.MenuItemNew] = []
    menuID: None


class CategoryDocument(CategoryBase, Document):

    class Settings:
        name = "categories"
        bson_encoders = {ObjectId: str}
        indexes = []