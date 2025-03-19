from datetime import datetime

from beanie import Document

from app.crud import restaurant as restaurant_crud
from google.cloud.firestore_v1 import DocumentReference
from pydantic import BaseModel, confloat, Field
from typing import Optional

from schemas.document_id import DocumentId
from utils.utils import partial_model


class InvitationTokenBase(BaseModel):
    restaurant_id: str
    expire: Optional[datetime]

    @staticmethod
    def from_doc(doc: DocumentReference) -> "InvitationTokenDisplay":
        doc_data = doc.get().to_dict()
        restaurant_ref: DocumentReference = doc_data["restaurant_id"]
        restaurant_id = restaurant_ref.id
        _id = doc.id
        return InvitationTokenDisplay(
            id=_id,
            expire=doc_data["expire"],
            restaurant_id=restaurant_id,
            created_time=doc.get().create_time.isoformat()
        )


class InvitationTokenCreate(InvitationTokenBase):
    pass

@partial_model
class InvitationTokenUpdate(InvitationTokenBase):
    pass


class InvitationToken(InvitationTokenBase, DocumentId):

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }


class InvitationTokenDocument(InvitationTokenBase, Document):

    class Settings:
        name = "invitation tokens"


class InvitationTokenDisplay(InvitationTokenBase):
    id: str
    created_time: Optional[datetime]
