import asyncio
import pytest

from fastapi.testclient import TestClient
from main import app

from models.base import reset_db, create_engine

from tests.databse_seeds.user_seed import add_seed_users, add_test_users

from authentication import PasswordManager


password_manager = PasswordManager()


DATABASE_URL = "sqlite+aiosqlite:///tests/test.db"
engine = create_engine(DATABASE_URL)


async def main():
    await reset_db()
    await add_seed_users()
    await add_test_users()


asyncio.run(main())


@pytest.fixture
def client():
    return TestClient(app)
