from fastapi import status
from app_exceptions.app_exception import AppException


class RoleAlreadyExists(AppException):
    status_code = status.HTTP_403_FORBIDDEN
    message = "Role with name already exists"


class RoleNotFound(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    message = "Role Not found"


class RoleAlreadyAssigned(AppException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = "The user already has this role"
