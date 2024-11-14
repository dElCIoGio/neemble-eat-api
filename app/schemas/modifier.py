from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from datetime import datetime


class LimitType(str, Enum):
	UP_TO = "UP_TO"
	EXACTLY = "EXACTLY"
	AT_LEAST = "AT_LEAST"
	ALL = "ALL"


class OptionLimitType(str, Enum):
	UP_TO = "UP_TO"
	UNLIMITED = "UNLIMITED"


class ModifierBase(BaseModel):
	"""
	Represents the base class for modifiers used in a menu item.

	Attributes:
		name and description: Strings that describe the modifier.
		isRequired: A boolean that indicates whether this modifier must be selected.
		limitType: An instance of LimitType enum that specifies how selection limits should be enforced.
		limit: An integer that works together with limitType to define the limits of selection.
		optionLimitType: An instance of OptionLimitType that determines how many times a single option can be chosen.
		optionLimit: An integer that specifies the maximum number of times an option can be selected.
		options: A list of ModifierOption instances available for this modifier.
	"""
	name: str
	description: Optional[str] = ""
	isRequired: bool
	limitType: LimitType
	limit: int
	optionLimitType: OptionLimitType
	optionLimit: int
	options: List[str]


class ModifierCreate(ModifierBase):
	name: str = Field(..., min_length=1, max_length=100)
	description: str = Field(..., min_length=1, max_length=300)
	limit: int = Field(..., ge=0)
	optionLimit: int = Field(..., ge=0)
	options: List[str] = Field(..., min_length=1, max_length=10)


class ModifierDisplay(ModifierBase):
	id: str
	created_time: Optional[datetime]


class ModifierOptionBase(BaseModel):
	"""
	Represents a base model for a modifier option for a modifier.

	Attributes:
		name (str): The name of the modifier option.
		additionalPrice (Optional[float]): The additional price of the modifier option, default is 0.0.
	"""
	name: str
	additionalPrice: Optional[float] = 0.0


class ModifierOptionCreate(ModifierOptionBase):
	name = Field(..., min_length=1, max_length=100)
	additionalPrice = Field(..., ge=0.0)


class ModifierOptionDisplay(ModifierOptionBase):
	id: str
	created_time: Optional[datetime]
