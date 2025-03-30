from fastapi import status
from app_exceptions.app_exception import AppException


class UserAlreadyExists(AppException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = "User with email already exists"


class UserNotFound(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    message = "User Not found"
