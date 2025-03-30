from enum import Enum
from typing import Any


class UserRole(str, Enum):
    SUPERADMIN = "super_admin"
    ADMIN = "admin"
    USER_MODERATOR = "user_moderator"
    EVENT_MODERATOR = "event_moderator"


class Permission(str, Enum):
    GET_USERS = "get_users"
    ADD_USER = "add_user"
    DELETE_USER = "delete_user"
    UPDATE_USER = "update_user"
    APPROVE_USER = "approve_user"
    ADD_ROLE = "add_role"
    GET_ROLES = "get_roles"
    DELETE_ROLE = "delete_role"
    UPDATE_ROLE = "update_role"
    GET_CONTESTS = "get_contests"
    ADD_CONTEST = "add_contest"
    DELETE_CONTEST = "delete_contest"
    UPDATE_CONTEST = "update_contest"
    APPROVE_CONTEST = "approve_contest"
    GET_WORKSHOPS = "get_workshops"
    ADD_WORKSHOP = "add_workshop"
    DELETE_WORKSHOP = "delete_workshop"
    UPDATE_WORKSHOP = "update_workshop"
    APPROVE_WORKSHOP = "approve_workshop"
    ADD_ORGANIZER = "add_organizer"
    GET_ORGANIZERS = "get_organizers"
    DELETE_ORGANIZER = "delete_organizer"
    UPDATE_ORGANIZER = "update_organizer"
    GET_EVENTS = "get_events"
    ADD_EVENT = "add_event"
    DELETE_EVENT = "delete_event"
    UPDATE_EVENT = "update_event"
    APPROVE_EVENT = "approve_event"


class EventCategory(str, Enum):
    WORKSHOP = "workshop"
    CONTEST = "contest"


class Role:
    def __init__(self, level: int, permissions: list[str]):
        self.level = level
        self.permissions = permissions

    def has_permissions(self, permission: list[Permission]) -> bool:
        return all([True for perm in permission if perm in self.permissions])

    def has_permission(self, permission: Permission) -> bool:
        return permission in self.permissions


class RolePermissions:
    _ROLE_PERMISSIONS: dict[str, Role] = {
        UserRole.SUPERADMIN.value: Role(
            level=0, permissions=[permission.value for permission in Permission]
        ),
        UserRole.ADMIN.value: Role(
            level=2, permissions=[permission.value for permission in Permission]
        ),
        UserRole.USER_MODERATOR.value: Role(
            level=4,
            permissions=[
                Permission.GET_EVENTS.value,
                Permission.GET_USERS.value,
                Permission.ADD_USER.value,
                Permission.DELETE_USER.value,
                Permission.UPDATE_USER.value,
                Permission.APPROVE_USER.value,
            ],
        ),
        UserRole.EVENT_MODERATOR.value: Role(
            level=6,
            permissions=[
                Permission.GET_EVENTS.value,
                Permission.GET_USERS.value,
                Permission.ADD_EVENT.value,
                Permission.DELETE_EVENT.value,
                Permission.UPDATE_EVENT.value,
                Permission.APPROVE_EVENT.value,
                Permission.ADD_ORGANIZER.value,
                Permission.GET_ORGANIZERS.value,
                Permission.DELETE_ORGANIZER.value,
                Permission.UPDATE_ORGANIZER.value,
            ],
        ),
    }

    @classmethod
    def get_role(cls, _role: str) -> Role | Any:
        role = cls._ROLE_PERMISSIONS.get(_role, None)
        return role
