from beanie import Document
from bson import ObjectId
from pydantic import BaseModel, EmailStr, constr, validator, conint, HttpUrl, confloat
from typing import Optional
from datetime import datetime
from app.schemas import category as category_schema
from app.schemas.document_id import DocumentId
from app.utils.utils import partial_model


class MenuBase(BaseModel):
    restaurantID: str
    name: str
    description: Optional[str] = ""
    categories: Optional[list[str]] = []


class MenuCreate(MenuBase):
    pass


@partial_model
class MenuUpdate(MenuBase):
    pass


class Menu(MenuBase, DocumentId):
    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }

class MenuDocument(MenuBase, Document):

    class Settings:
        name = "menus"
        bson_encoders = {ObjectId: str}
        indexes = []

class MenuDisplay(MenuBase):
    id: str
    created_time: Optional[datetime]


class MenuNew(MenuBase):
    categories: Optional[list[category_schema.CategoryNew]] = []
    restaurantID: None
