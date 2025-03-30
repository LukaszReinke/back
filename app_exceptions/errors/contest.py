from fastapi import status
from app_exceptions.app_exception import AppException


class ContestAlreadyExists(AppException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = "Contest with name already exists"


class ContestNotFound(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    message = "Contest Not found"


class ContestArleadyApproved(AppException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = "Contest is arleady approved"
