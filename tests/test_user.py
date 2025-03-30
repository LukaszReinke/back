import pytest
from fastapi.testclient import TestClient
from tests.datatest_loader import get_users_data
from tests.databse_seeds.user_seed import get_user_id, get_clients_tokens_dict

DATA: dict[str, dict[str, dict[str, str]]] = get_users_data()
TOKENS = get_clients_tokens_dict()


class TestUser:

    @pytest.fixture(params=list(DATA["get_all_users"]))
    def get_all_users(self, request: pytest.FixtureRequest) -> dict[str, str]:
        return request.param

    @pytest.fixture(params=list(DATA["get_user"]))
    def get_user(self, request: pytest.FixtureRequest) -> dict[str, str]:
        return request.param

    @pytest.fixture(params=list(DATA["add"]))
    def add_users(self, request: pytest.FixtureRequest) -> dict[str, str]:
        return request.param

    @pytest.fixture(params=list(DATA["change_role"]))
    def change_user_role(self, request: pytest.FixtureRequest) -> dict[str, str]:
        return request.param

    @pytest.fixture(params=list(DATA["delete"]))
    def delete_user(self, request: pytest.FixtureRequest) -> dict[str, str]:
        return request.param

    def test_get_all_users(self, client: TestClient, get_all_users: dict[str, str]):
        response = client.get(
            "/users/",
            headers={"Authorization": f"Bearer {TOKENS[get_all_users['client']]}"},
        )

        assert response.status_code == get_all_users.get("expected_status")

    @pytest.mark.asyncio
    async def test_get_user(self, client: TestClient, get_user: dict[str, str]):
        user_id = await get_user_id(get_user)

        response = client.get(
            f"/users/{user_id}",
            headers={"Authorization": f"Bearer {TOKENS[get_user['client']]}"},
        )

        assert response.status_code == get_user.get("expected_status")

    def test_add_user(self, client: TestClient, add_users: dict[str, str]):
        response = client.post(
            "/users/",
            json=add_users.get("user"),
            headers={"Authorization": f"Bearer {TOKENS[add_users['client']]}"},
        )

        print(response)
        assert response.status_code == add_users.get("expected_status")

    @pytest.mark.asyncio
    async def test_change_user_role(
        self, client: TestClient, change_user_role: dict[str, str]
    ):
        user_id = await get_user_id(change_user_role)

        response = client.put(
            f"/users/{user_id}/update",
            headers={"Authorization": f"Bearer {TOKENS[change_user_role['client']]}"},
            json={
                "role": change_user_role.get("role"),
            },
        )

        assert response.status_code == change_user_role.get("expected_status")

    @pytest.mark.asyncio
    async def test_delete_user(self, client: TestClient, delete_user: dict[str, str]):
        user_id = await get_user_id(delete_user)

        response = client.delete(
            f"/users/{user_id}",
            headers={"Authorization": f"Bearer {TOKENS[delete_user['client']]}"},
        )

        assert response.status_code == delete_user.get("expected_status")
