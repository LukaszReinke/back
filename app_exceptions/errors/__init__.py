from .auth import (
    AccountNotApproved,
    ExpiredTokenError,
    InsufficientPermission,
    InvalidCredentials,
    InvalidTokenError,
    TokenValidationError,
)
from .contest import ContestAlreadyExists, ContestArleadyApproved, ContestNotFound
from .event import EventAlreadyExists, EventNotFound, EventArleadyApproved
from .meta import PageOutOfRange
from .organizer import OrganizerAlreadyExists, OrganizerNotFound
from .role import RoleAlreadyExists, RoleNotFound, RoleAlreadyAssigned
from .user import UserAlreadyExists, UserNotFound
from .workshop import WorkshopAlreadyExists, WorkshopArleadyApproved, WorkshopNotFound
from .email import EmailAuthenticationError, EmailSendingError, SMTPConnectionError, EmailTemplateError

__all__ = [
    "EventAlreadyExists",
    "EventNotFound",
    "EventArleadyApproved",
    "ContestAlreadyExists",
    "ContestArleadyApproved",
    "ContestNotFound",
    "OrganizerAlreadyExists",
    "OrganizerNotFound",
    "RoleAlreadyExists",
    "AccountNotApproved",
    "ExpiredTokenError",
    "PageOutOfRange",
    "InsufficientPermission",
    "InvalidCredentials",
    "InvalidTokenError",
    "TokenValidationError",
    "RoleNotFound",
    "UserAlreadyExists",
    "UserNotFound",
    "WorkshopAlreadyExists",
    "WorkshopArleadyApproved",
    "WorkshopNotFound",
    "EmailAuthenticationError",
    "EmailSendingError",
    "SMTPConnectionError",
    "EmailTemplateError"
    "RoleAlreadyAssigned",
]
