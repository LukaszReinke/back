from fastapi import status
from app_exceptions.app_exception import AppException


class EmailAuthenticationError(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = "SMTP authentication failed. Please check your credentials."


class SMTPConnectionError(AppException):
    status_code = status.HTTP_502_BAD_GATEWAY
    message = "SMTP connection error."


class EmailSendingError(AppException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = "Unexpected error occurred while sending the email."


class EmailTemplateError(AppException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = "Error occurred while loading or formatting the email template."