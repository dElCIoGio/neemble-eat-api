import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.client import Client
from google.cloud.firestore import AsyncClient
import os


path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "./credentials/credentials.json")


# Use a service account_
cred = credentials.Certificate(path)
firebase_admin.initialize_app(cred)

# Initialize Firestore
db: Client = firestore.client()
