from fastapi import status
from app_exceptions.app_exception import AppException


class WorkshopAlreadyExists(AppException):
    status_code = status.HTTP_403_FORBIDDEN
    message = "Workshop with name already exists"


class WorkshopNotFound(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    message = "Workshop Not found"


class WorkshopArleadyApproved(AppException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = "Workshop is arleady approved"
