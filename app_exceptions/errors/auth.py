from fastapi import status
from app_exceptions.app_exception import AppException


class InvalidTokenError(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = "Token is invalid"
    headers = ({"WWW-Authenticate": "Bearer"},)


class TokenValidationError(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = "Could not validate token"
    headers = ({"WWW-Authenticate": "Bearer"},)


class ExpiredTokenError(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = "Token has expired"
    headers = ({"WWW-Authenticate": "Bearer"},)


class InvalidCredentials(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = "Invalid email or password"


class AccountNotApproved(AppException):
    status_code = status.HTTP_403_FORBIDDEN
    message = "Change password instead!"


class InsufficientPermission(AppException):
    status_code = status.HTTP_403_FORBIDDEN
    message = "You do not have enough permissions to perform this action"
