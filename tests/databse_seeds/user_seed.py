import repositories as rp
from models import UserBase
from authentication import PasswordManager
from tests.datatest_loader import seed_data, get_users_data
from authentication import jwt_manager


password_manager = PasswordManager()


async def get_user_id(test_user: dict[str, str]):
    user_id = test_user.get("user_id")
    if user_id:
        return user_id

    if test_user.get("email"):
        user = await rp.UserRepository.get_user_by_email(str(test_user["email"]))
        return user.user_id if user else None

    else:
        return None


def get_clients_tokens_dict() -> dict[str, str]:
    seed: dict[str, dict[str, dict[str, str]]] = seed_data()

    tokens = {
        user["email"]: jwt_manager.create_access_token(user["email"], user["role"])
        for user in seed["users"].values()
    }

    return tokens


async def _add_users(users: list[dict[str, str]]):
    for test_user in users:
        _user = UserBase(
            **{
                **test_user,
                "hashed_password": password_manager.hash_password("password"),
            }
        )
        await rp.UserRepository.add_user(_user)


async def add_test_users():
    users: list[dict[str, str]] = get_users_data().get("users", {})
    await _add_users(users)


async def add_seed_users():
    users: dict[str, dict[str, str]] = seed_data().get("users", {})
    await _add_users(list(users.values()))
