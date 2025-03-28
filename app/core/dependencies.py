import json
from functools import lru_cache

from app.core.config import Settings


@lru_cache()
def get_settings():
    return Settings()


def get_google_cloud_credentials():
    settings = get_settings()

    return settings.GOOGLE_CLOUD_CREDENTIALS


