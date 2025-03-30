from fastapi import status
from app_exceptions.app_exception import AppException


class PageOutOfRange(AppException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = "Page number exceeds total pages"
