from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class ModificationBase(BaseModel):
	name: str
	order: str
	options: List[str]


class ModificationCreate(ModificationBase):
	name: str = Field(..., min_length=1, max_length=100)
	options: List[str] = Field(..., min_length=1, max_length=10)


class ModificationDisplay(ModificationBase):
	id: str
	created_time: Optional[datetime]


class ModificationOptionBase(BaseModel):
	name: str
	additionalPrice: float = 0.0
	selectCount: int


class ModificationOptionCreate(ModificationOptionBase):
	name = Field(..., min_length=1, max_length=100)
	additionalPrice = Field(..., ge=0.0)
	selectCount = Field(..., ge=0)


class ModificationOptionDisplay(ModificationOptionBase):
	id: str
	created_time: Optional[datetime]
