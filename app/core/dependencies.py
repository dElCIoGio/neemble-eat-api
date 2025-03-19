from functools import lru_cache

from app.core.config import Settings


@lru_cache()
def get_settings():
    return Settings()


def get_google_cloud_credentials():

    settings = get_settings()
    return {
  "type": settings.GOOGLE_CLOUD_TYPE,
  "project_id": settings.GOOGLE_CLOUD_PROJECT_ID,
  "private_key_id": settings.GOOGLE_CLOUD_PRIVATE_KEY_ID,
  "private_key": settings.GOOGLE_CLOUD_PRIVATE_KEY,
  "client_email": settings.GOOGLE_CLOUD_CLIENT_EMAIL,
  "client_id": settings.GOOGLE_CLOUD_CLIENT_ID,
  "auth_uri": settings.GOOGLE_CLOUD_AUTH_URI,
  "token_uri": settings.GOOGLE_CLOUD_TOKEN_URI,
  "auth_provider_x509_cert_url": settings.GOOGLE_CLOUD_AUTH_PROVIDER_X509_CERT_URL,
  "client_x509_cert_url": settings.GOOGLE_CLOUD_CLIENT_X509_CERT_URL,
  "universe_domain": settings.GOOGLE_CLOUD_UNIVERSI_DOMAIN
}


