from beanie import Document
from bson import ObjectId
from google.cloud.firestore_v1 import DocumentReference
from pydantic import BaseModel, constr
from typing import Optional, List
from datetime import datetime
from enum import Enum

from app.schemas.document_id import DocumentId
from app.utils.utils import partial_model


class MemberRoleNames(str, Enum):
    Administrator="Administrator"
    Manager="Manager"
    Chef="Chef"
    Waitstaff="Waitstaff"
    Bartender="Bartender"
    Accountant="Accountant"

class Permissions(str, Enum):
    View="view"
    Delete="delete"
    Update="update"
    Create="create"

class SectionPermission(BaseModel):
    section: str
    permissions: List[Permissions]

class Role(BaseModel):
    name: MemberRoleNames
    description: str
    permissions: List[SectionPermission]

class UserBase(BaseModel):
    UUID: str
    firstName: str
    lastName: str
    email: str
    role: Role
    phoneNumber: str
    restaurantID: Optional[str] = None


    @staticmethod
    def from_doc(doc: DocumentReference) -> "UserDisplay":
        doc_data = doc.get().to_dict()
        restaurant_ref: DocumentReference = doc_data["restaurantID"]
        restaurant_id = restaurant_ref.id
        _id = doc.id
        return UserDisplay(
            id=_id,
            phoneNumber=doc_data["phoneNumber"],
            UUID=doc_data["UUID"],
            firstName=doc_data["firstName"],
            lastName=doc_data["lastName"],
            email=doc_data["email"],
            restaurantID=restaurant_id,
            role=doc_data["role"],
            created_time=doc.get().create_time.isoformat()
        )


class UserCreate(UserBase):
    firstName: constr(min_length=1, max_length=40)
    lastName: constr(min_length=1, max_length=40)
    phoneNumber: constr(min_length=9)


@partial_model
class UserUpdate(UserBase):
    pass


class User(UserBase, DocumentId):
    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }


class UserDisplay(UserBase):
    id: str
    created_time: Optional[datetime]


class UserDocument(UserBase, Document):

    class Settings:
        name = "users"
        bson_encoders = {ObjectId: str}
        indexes = [
            {"keys": [("email", 1)], "name": "user_email_index", "unique": True},
            {"keys": [("UUID", 1)], "name": "user_uuid_index", "unique": True},
            {"keys": [("restaurantID", 1)], "name": "restaurant_id_index"},
            {"keys": [("role.name", 1)], "name": "role_name_index"},
        ]