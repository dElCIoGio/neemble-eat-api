from dotenv import load_dotenv

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname('app'), '..')))

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load .env file automatically
load_dotenv()

class Metadata(BaseSettings):
    TITLE: str = "Neemble Eat API"
    DESCRIPTION: str = "API for Neemble Eat"
    VERSION: str = "1.0.0"
    FRONTEND_URL: str = "https://neemble-eat.ao"
    TIMEZONE: str = "Africa/Luanda"

class Collections(BaseSettings):
    CATEGORIES: str = "categories"
    INVITATION_TOKENS: str = "invitation tokens"
    INVOICES: str = "invoices"
    MENUS: str = "menus"
    MENU_ITEMS: str = "menu items"
    MODIFICATIONS: str = "modifications"
    MODIFICATION_OPTIONS: str = "modification options"
    MODIFIERS: str = "modifiers"
    MODIFIER_OPTIONS: str = "modifier options"
    ORDERS: str = "orders"
    RESTAURANTS: str = "restaurants"
    TABLES: str = "tables"
    TABLE_SESSIONS: str = "sessions"
    USERS: str = "users"

class TokensSettings(BaseSettings):
    TOKENS_SECRET_KEY: str = "0wxK3rMDpk"

class GoogleCloudSettings(BaseSettings):
    GOOGLE_CLOUD_TYPE: str
    GOOGLE_CLOUD_PROJECT_ID: str
    GOOGLE_CLOUD_PRIVATE_KEY_ID: str
    GOOGLE_CLOUD_PRIVATE_KEY: str
    GOOGLE_CLOUD_CLIENT_EMAIL: str
    GOOGLE_CLOUD_CLIENT_ID: str
    GOOGLE_CLOUD_AUTH_URI: str
    GOOGLE_CLOUD_TOKEN_URI: str
    GOOGLE_CLOUD_AUTH_PROVIDER_X509_CERT_URL: str
    GOOGLE_CLOUD_CLIENT_X509_CERT_URL: str
    GOOGLE_CLOUD_UNIVERSI_DOMAIN: str = "googleapis.com"

    class Config:
        case_sensitive = True
        env_file = ".env"


class Settings(Metadata, TokensSettings, Collections, GoogleCloudSettings):
    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"
