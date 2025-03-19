import os
import sys

from app.core.dependencies import get_google_cloud_credentials

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname('app'), '..')))

import firebase_admin
from firebase_admin import auth, credentials
import os

path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "credentials/credentials.json")
gc_cred = get_google_cloud_credentials()

cred = credentials.Certificate.from_dict(gc_cred)
firebase_admin.initialize_app(cred)

__all__ = [
    "auth"
]