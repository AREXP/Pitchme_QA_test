from typing import Optional

import pytest

from schemas import UserCreate
from tests.base import SocialMediaAPI, Users
from tests.helpers import validate_data_against_model


def pytest_addoption(parser):
    parser.addoption(
        "--base_url",
        action="store",
        default="https://pitch.me",
        help="Base URL of the application under test",
    )


@pytest.fixture(autouse=True, scope="session")
def base_url(request):
    return request.config.getoption("--base_url")


@pytest.fixture
def social_media_api(base_url):
    return SocialMediaAPI(base_url)


@pytest.fixture
def users_api(social_media_api):
    return Users(social_media_api)


@pytest.fixture
def mock_users_api(monkeypatch, social_media_api):
    def mock_get_user(
        self, user_id: int, expected_status_code: Optional[int] = None
    ) -> dict:
        if user_id in range(1, 11):
            return {
                "id": user_id,
                "name": f"mock_user_no_{user_id}",
                "email": f"user_{user_id}@example.com",
            }
        else:
            return {"error": "User not found"}

    def mock_get_users(self, expected_status_code: Optional[int] = None) -> list[dict]:
        return [
            {
                "id": user_id,
                "name": f"mock_user_no_{user_id}",
                "email": f"user_{user_id}@example.com",
            }
            for user_id in range(1, 11)
        ]

    def mock_create_user(
        self, user_data: dict, expected_status_code: Optional[int] = None
    ) -> dict:
        try:
            validate_data_against_model(
                response_data=user_data,
                expected_model=UserCreate,
                expected_response_data_type="dict",
            )
            return {
                "id": 11,
                "name": user_data["name"],
                "email": user_data["email"],
            }
        except:
            return {"error": "User not created"}

    monkeypatch.setattr(Users, "get_user", mock_get_user)
    monkeypatch.setattr(Users, "get_users", mock_get_users)
    monkeypatch.setattr(Users, "create_user", mock_create_user)

    return Users(social_media_api)
