from datetime import datetime, timedelta, timezone
from typing import List

from google.cloud.firestore_v1 import DocumentReference

from app.utils.utils import get_time_now


def filter_recent_documents(hours: int, documents: List[DocumentReference]):
    """
    Filters documents that were created within the last given amount of hours.

    :param hours: Number of hours to look back from current time
    :param documents: List of DocumentReference objects
    :return: List of DocumentReference objects created in the last given amount of hours
    """
    # Ensure current_time is offset-aware, using UTC
    current_time = get_time_now()
    cutoff_time = current_time - timedelta(hours=hours)

    recent_documents = [
        doc for doc in documents
        if doc.get().create_time > cutoff_time
    ]

    return recent_documents
