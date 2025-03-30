from fastapi import status
from app_exceptions.app_exception import AppException


class OrganizerAlreadyExists(AppException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = "Organizer with email already exists"


class OrganizerNotFound(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    message = "Organizer Not found"
