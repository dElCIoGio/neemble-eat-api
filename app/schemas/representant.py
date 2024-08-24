from pydantic import BaseModel, EmailStr, constr, field_validator
from phonenumbers import geocoder
import phonenumbers
from typing import Optional
from datetime import datetime


class RepresentantBase(BaseModel):
    UUID: str
    firstName: str
    lastName: str
    email: str
    role: str
    phoneNumber: str
    restaurantID: Optional[str] = None

    #@field_validator("phoneNumber")
    #def validate_phone_number(cls, value: str):
    #    try:
    #        phone_number_obj = phonenumbers.parse(value, None)
    #    except phonenumbers.NumberParseException:
    #        raise ValueError("Invalid phone number format")
#
    #    if not phonenumbers.is_valid_number(phone_number_obj):
    #        raise ValueError("Invalid phone number")
#
    #    for country_code in ["AO", "PT", "UK"]:
    #        country = geocoder.description_for_number(
    #            phonenumbers.parse(value, country_code), "en")
    #        if country not in ["United Kingdom", "Angola", "Portugal"]:
    #            raise ValueError(f"{value} is not from a supported region (UK, AO, PT)")
#
    #    return value

    class Config:
        orm_mode = True


class RepresentantCreate(RepresentantBase):
    firstName: constr(min_length=1, max_length=50)
    lastName: constr(min_length=1, max_length=50)
    phoneNumber: constr(min_length=9)


class RepresentantDisplay(RepresentantBase):
    id: str
    created_time: Optional[datetime]
