from fastapi import HTTPException
from fastapi.responses import JSONResponse


class CustomHTTPException(HTTPException):

    def __init__(self, status_code, detail, payload=None, errors=None):
        super().__init__(status_code, detail)
        self.payload = payload
        self.errors = errors


def custom_http_exception_handler(request, exc: HTTPException):

    error_response = {
        "status_code": exc.status_code,
        "message": exc.detail,
        "request_payload": exc.payload,
        "errors": exc.errors
    }

    return JSONResponse(content=error_response, status_code=exc.status_code)
