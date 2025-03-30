import inspect
from collections import defaultdict
from typing import Any

import fastapi.exceptions as fexc
from app_exceptions.app_exception import AppException
from app_exceptions import errors
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

EXCEPTIONS_CLASSES: list[type[AppException]] = [
    obj
    for _, obj in inspect.getmembers(errors, inspect.isclass)
    if issubclass(obj, AppException)
]


class RequestValidationError(AppException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    message = "Validation error message"
    detail: Any = [{"loc": ["string", 0], "msg": "string", "type": "string"}]


def generate_error_responses(
    *exceptions: type[AppException],
) -> dict[int | str, dict[str, Any]]:
    error_responses: Any = defaultdict(
        lambda: {"description": "", "content": {"application/json": {"examples": {}}}}
    )

    default_exceptions: list[type[AppException]] = [
        errors.InvalidTokenError,
        errors.ExpiredTokenError,
        errors.TokenValidationError,
        errors.AccountNotApproved,
        errors.InsufficientPermission,
    ]

    all_exceptions = list(exceptions) + default_exceptions
    for exc in all_exceptions:
        error_responses[exc.status_code]["content"]["application/json"]["examples"][
            exc.__name__
        ] = {
            "summary": exc.message,
            "value": {
                "message": exc.message,
            },
        }

    error_responses[422]["content"]["application/json"]["examples"][
        RequestValidationError.__name__
    ] = {
        "summary": RequestValidationError.message,
        "value": {
            "message": RequestValidationError.message,
            "detail": RequestValidationError.detail,
        },
    }

    return dict(error_responses)


def app_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, AppException):
        return exc.response()

    return JSONResponse(content={"message": "Unhandled exception"}, status_code=500)


def register_all_errors(app: FastAPI):
    for exception in EXCEPTIONS_CLASSES:
        app.add_exception_handler(exception, app_exception_handler)

    @app.exception_handler(fexc.RequestValidationError)
    async def validation_exception_handler(  # type: ignore
        request: Request, exc: fexc.RequestValidationError
    ):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"message": "Validation error message", "errors": exc.errors()},
        )

    @app.exception_handler(500)
    async def internal_server_error(request: Request, exc: Exception):  # type: ignore
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "Oops! Something went wrong",
                "error_type": type(exc).__name__,
                "details": str(exc),
            },
        )

    @app.exception_handler(SQLAlchemyError)
    async def database_error(request: Request, exc: SQLAlchemyError):  # type: ignore
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "Database error occurred",
                "error_type": type(exc).__name__,
                "details": str(exc),
            },
        )
