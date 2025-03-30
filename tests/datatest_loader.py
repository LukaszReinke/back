import json
from typing import Any


def _json_data_loader(path: str):
    with open(rf"{path}", "r", encoding="utf-8") as file:
        return json.load(file)


def seed_data() -> dict[str, Any]:
    return _json_data_loader("tests//data//seed_data.json")


def get_users_data() -> dict[str, Any]:
    return _json_data_loader("tests//data//test_users.json")


def get_events_data() -> dict[str, Any]:
    return _json_data_loader("tests//data//test_events.json")
