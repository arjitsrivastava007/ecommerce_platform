import time
import traceback
from pathlib import Path
from fastapi import APIRouter, FastAPI, Request
import uvicorn
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse
from app.api.api import api_router
from app.core.config import setup_logging, log_entry_point, settings
from app.core.exception import CustomHTTPException, custom_http_exception_handler
from fastapi.middleware.cors import CORSMiddleware
from http import HTTPStatus


BASE_PATH = Path(__file__).resolve().parent

router = APIRouter()
app = FastAPI(title="Ecommerce Platform", version="1.0")

logger = setup_logging(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.add_exception_handler(CustomHTTPException, custom_http_exception_handler)


@router.get("/", status_code=HTTPStatus.OK)
async def root(req: Request) -> dict:
    try:
        await log_entry_point(req)
    except Exception as error:
        traceback.print_exc()
        raise CustomHTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Unhandled Exception - {error}"
        ) from error

    return {
        "app": "Ecommerce Platform",
        "version": "1.0",
        "status": "Ok"
    }


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add the request processing time to the header."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.debug(f"X-Process-Time: {str(process_time)}")
    return response


@app.exception_handler(TypeError)
async def type_error_handler(request: Request, exc: TypeError):
    """Returns Type error Exception Handler."""
    logger.error(request)
    logger.error(exc)
    traceback.print_exc()
    return JSONResponse(
        content={"message": "Internal server error", "detail": str(exc)},
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Returns Generic Exception Handler."""
    logger.error(str(request))
    logger.error(str(exc))
    traceback.print_exc()
    return JSONResponse(
        content={"message": "Internal server error", "detail": str(exc)},
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
    )


@app.exception_handler(RequestValidationError)
async def custom_exception_handler(request: Request, exc: RequestValidationError):
    """Returns Custom Exception Handler."""
    error_response = {
        "message": "Bad request",
        "details": "Validation error in the request data",
        "data": [],
    }
    try:
        logger.error("Custom exception handler")
        logger.error(f"Request Failed | {request} | {exc}")
        payload = await request.json()
        error_messages = []
        for error in exc.errors():
            location = ".".join(map(str, error["loc"])) if error["loc"] else "body"
            error_messages.append(f'Field "{location}" - {error["msg"]}')

        error_detail = ", ".join(error_messages)
        error_response = {
            "error_code": HTTPStatus.BAD_REQUEST,
            "message": error_detail,
            "request_payload": payload,
            "success": False,
        }
        logger.error(error_response)
        traceback.print_exc()
        return JSONResponse(content=error_response, status_code=HTTPStatus.BAD_REQUEST)
    except Exception as error:
        # Handle any unexpected exceptions here
        logger.error(str(error))
        traceback.print_exc()
        return JSONResponse(
            content=error_response, status_code=HTTPStatus.INTERNAL_SERVER_ERROR
        )


app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(router)


if __name__ == "__main__":
    # pass
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
