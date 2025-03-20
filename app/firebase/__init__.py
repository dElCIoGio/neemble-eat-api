import os
import sys

from app.core.dependencies import get_google_cloud_credentials

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname('app'), '..')))

import firebase_admin
from firebase_admin import auth, credentials
import os


certi = get_google_cloud_credentials()


gc_cred = get_google_cloud_credentials()

cred = credentials.Certificate(certi)
firebase_admin.initialize_app(cred)

__all__ = [
    "auth"
]