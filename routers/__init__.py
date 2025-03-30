from .contest import router as contest_router
from .event import router as events_router
from .user import router as users_router
from .profile import router as profile_router
from .organizer import router as organizer_router
from .workshop import router as workshop_router

__all__ = [
    "contest_router",
    "events_router",
    "users_router",
    "profile_router",
    "organizer_router",
    "workshop_router",
]
