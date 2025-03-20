import json
from functools import lru_cache

from app.core.config import Settings


@lru_cache()
def get_settings():
    return Settings()


def get_google_cloud_credentials():
    settings = get_settings()

    credentials = json.loads(settings.GOOGLE_CLOUD_CREDENTIALS)

    credentials["private_key"] = credentials["private_key"].replace("\\n", "\n")

    return credentials


