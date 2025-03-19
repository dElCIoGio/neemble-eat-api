from pydantic import BaseModel, Field
from datetime import datetime

from app.db.object_id import PyObjectId

class DocumentId(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)