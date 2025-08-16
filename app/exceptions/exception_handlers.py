from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging

logger = logging.getLogger(__name__)

def register_exception_handlers(app):
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        logger.warning(f"HTTP error: {exc.detail} - Path: {request.url}")
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    @app.exception_handler(HTTPException)
    async def fastapi_http_exception_handler(request: Request, exc: HTTPException):
        logger.warning(f"FastAPI HTTP error: {exc.detail} - Path: {request.url}")
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.warning(f"Validation error: {exc.errors()} - Path: {request.url}")
        errors = exc.errors()
        for error in errors:
            if "ctx" in error:
                error.pop("ctx")
        return JSONResponse(status_code=422, content={"detail": errors})

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled error: {str(exc)} - Path: {request.url}")
        return JSONResponse(status_code=500, content={"detail": "Erro interno do servidor"})
