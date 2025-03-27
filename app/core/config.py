from dotenv import load_dotenv, find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
import os
import sys

# DOTENV = os.path.join(os.path.dirname(__file__), ".env")
from pathlib import Path
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname('app'), '..')))


class Settings(BaseSettings):
    # App Config
    TITLE: str = "Neemble Eat API"
    DESCRIPTION: str = "API - Neemble Eat"
    VERSION: str = "1.0.0"
    FRONTEND_URL: str = "https://neemble-eat.ao"
    TIMEZONE: str = "Africa/Luanda"

    # Firestore Collections
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

    # Goggle Cloud Config
    GOOGLE_CLOUD_CREDENTIALS: str = os.getenv("GOOGLE_CLOUD_CREDENTIALS")


    # Additional Config
    TOKENS_SECRET_KEY: str = "0wxK3rMDpk"

    model_config = SettingsConfigDict(case_sensitive=True, env_file_encoding='utf-8')
