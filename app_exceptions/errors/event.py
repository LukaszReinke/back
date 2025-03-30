from fastapi import status
from app_exceptions.app_exception import AppException


class EventAlreadyExists(AppException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = "Event with name already exists"


class EventNotFound(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    message = "Event Not found"


class EventArleadyApproved(AppException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = "Event is arleady approved"
