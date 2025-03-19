import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import CollectionReference
from google.cloud.firestore_v1.client import Client
from app.core.dependencies import get_settings, get_google_cloud_credentials


settings = get_settings()
gc_cred = get_google_cloud_credentials()

# Use a service account_
cred = credentials.Certificate(gc_cred)
firebase_admin.initialize_app(cred)

# Initialize Firestore
db: Client = firestore.client()

categories_collection_ref: CollectionReference = db.collection(settings.CATEGORIES)
invitation_tokens_collection_ref: CollectionReference = db.collection(settings.INVITATION_TOKENS)
invoices_collection_ref: CollectionReference = db.collection(settings.INVOICES)
menus_collection_ref: CollectionReference = db.collection(settings.MENUS)
menu_items_collection_ref: CollectionReference = db.collection(settings.MENU_ITEMS)
modifications_collection_ref: CollectionReference = db.collection(settings.MODIFICATIONS)
modification_options_collection_ref: CollectionReference = db.collection(settings.MODIFICATION_OPTIONS)
modifiers_collection_ref: CollectionReference = db.collection(settings.MODIFIERS)
modifier_options_collection_ref: CollectionReference = db.collection(settings.MODIFIER_OPTIONS)
orders_collection_ref: CollectionReference = db.collection(settings.ORDERS)
restaurants_collection_ref: CollectionReference = db.collection(settings.RESTAURANTS)
tables_collection_ref: CollectionReference = db.collection(settings.TABLES)
table_sessions_collection_ref: CollectionReference = db.collection(settings.TABLE_SESSIONS)
users_collection_ref: CollectionReference = db.collection(settings.USERS)
representants_collection_ref: CollectionReference = db.collection("representants")



# Run the function to start the role update process

__all__ = [
    "categories_collection_ref",
    "invitation_tokens_collection_ref",
    "invoices_collection_ref",
    "menus_collection_ref",
    "menu_items_collection_ref",
    "modifications_collection_ref",
    "modification_options_collection_ref",
    "modifiers_collection_ref",
    "modifier_options_collection_ref",
    "orders_collection_ref",
    "restaurants_collection_ref",
    "tables_collection_ref",
    "table_sessions_collection_ref",
    "users_collection_ref",
]