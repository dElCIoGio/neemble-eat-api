import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.client import Client
import os


path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "./credentials/neemble-eat-db-c49af78976aa.json")


# Use a service account_
cred = credentials.Certificate(path)
firebase_admin.initialize_app(cred)

# Initialize Firestore
db: Client = firestore.client()
