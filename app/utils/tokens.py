from jwt import encode, decode, PyJWTError
from datetime import datetime, timedelta
from app.core.dependencies import get_settings

settings = get_settings()


def create_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = encode(to_encode, settings.TOKENS_SECRET_KEY, algorithm="HS256")
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = decode(token, settings.TOKENS_SECRET_KEY, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return user_id
    except PyJWTError:
        raise credentials_exception
