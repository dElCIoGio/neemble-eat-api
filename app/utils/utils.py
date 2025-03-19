from copy import deepcopy
from typing import List, Type, Tuple, Any, Optional

import pytz
from google.api_core.datetime_helpers import DatetimeWithNanoseconds
from google.cloud.firestore_v1 import DocumentReference
from pydantic import BaseModel, create_model
from pydantic.fields import FieldInfo

from datetime import timedelta, datetime




def get_time_now() -> datetime:
    tz = pytz.timezone("Africa/Luanda")
    now = datetime.now(tz)
    return now

def get_time_plus_hs(hours: int = 24):
    current_time = get_time_now()
    time_plus_24h = current_time + timedelta(hours=hours)
    return time_plus_24h


def get_documents_created_this_month(doc_refs: List[DocumentReference]):
    """Returns Firestore DocumentReferences created in the current month."""
    now = get_time_now()
    start_of_month = datetime(now.year, now.month, 1)

    return [doc for doc in doc_refs if convert_datetime_with_ns_to_datetime(doc.get().create_time) >= start_of_month]


def get_documents_created_last_month(doc_refs: List[DocumentReference]):
    """Returns Firestore DocumentReferences created in the previous month."""
    now = get_time_now()
    first_day_this_month = datetime(now.year, now.month, 1)
    last_day_last_month = first_day_this_month - timedelta(days=1)
    start_of_last_month = datetime(last_day_last_month.year, last_day_last_month.month, 1)

    return [doc for doc in doc_refs if
            start_of_last_month <= convert_datetime_with_ns_to_datetime(doc.get().create_time) < first_day_this_month]


def get_documents_created_today(doc_refs: List[DocumentReference]) -> List[DocumentReference]:
    """Returns Firestore DocumentReferences created today."""
    now = get_time_now()
    start_of_today = datetime(now.year, now.month, now.day)

    # Filter documents that were created today
    today_docs = [
        doc for doc in doc_refs if convert_datetime_with_ns_to_datetime(doc.get().create_time) >= start_of_today
    ]
    return today_docs


def get_documents_created_yesterday(doc_refs: List[DocumentReference]) -> List[DocumentReference]:
    """Returns Firestore DocumentReferences created yesterday."""
    now = get_time_now()
    start_of_today = datetime(now.year, now.month, now.day)
    start_of_yesterday = start_of_today - timedelta(days=1)

    # Filter documents that were created yesterday
    yesterday_docs = [
        doc for doc in doc_refs if start_of_yesterday <= convert_datetime_with_ns_to_datetime(doc.get().create_time) < start_of_today
    ]
    return yesterday_docs


def convert_datetime_with_ns_to_datetime(dt_ns: DatetimeWithNanoseconds) -> datetime:
    """Converts a Firestore DatetimeWithNanoseconds object to a Python datetime object."""
    # Convert to a string and then back to a datetime, truncating to microseconds
    dt_str = dt_ns.isoformat()
    # The Firestore DatetimeWithNanoseconds typically has more than 6 decimal places, trim to microseconds
    dt_micro_str = dt_str[:dt_str.rfind('.')+7]  # Include 6 decimal places for microseconds
    # Convert the string back to a datetime object
    dt = datetime.fromisoformat(dt_micro_str)
    return dt


def partial_model(model: Type[BaseModel]):
    def make_field_optional(field: FieldInfo, default: Any = None) -> Tuple[Any, FieldInfo]:
        new = deepcopy(field)
        new.default = default
        new.annotation = Optional[field.annotation]  # type: ignore
        return new.annotation, new
    return create_model(
        f'Partial{model.__name__}',
        __base__=model,
        __module__=model.__module__,
        **{
            field_name: make_field_optional(field_info)
            for field_name, field_info in model.__fields__.items()
        }
    )