from http import HTTPStatus
from fastapi import Depends, Request, Header
from app.core.config import settings
from app.core.exception import CustomHTTPException


# Check for the request if X-API-KEY is present in the headers
def get_api_key(request: Request):
    api_key = request.headers.get("X_API_KEY", None)
    if api_key is None:
        raise CustomHTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Missing API Key")
    return api_key


# Validate the X-API-KEY with the value in the .env
def validate_api_key(api_key: str = Depends(get_api_key)):
    if api_key != settings.API_KEY:
        raise CustomHTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid API Key"
        )


# pass auth middleware to include routes
def auth_middleware(
    X_API_KEY: str = Header(..., description="Your X_API_KEY header for authentication")
):
    validate_api_key(X_API_KEY)
