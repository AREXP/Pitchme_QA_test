from typing import Optional

import pytest

from schemas import UserCreate, UserUpdate, PostUpdate, PostCreate
from tests.base import SocialMediaAPI, Users, Posts
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

    def mock_update_user(
        self, user_id: int, user_data: dict, expected_status_code: Optional[int] = None
    ) -> dict:
        if user_id in range(1, 11):
            validate_data_against_model(
                response_data=user_data,
                expected_model=UserUpdate,
                expected_response_data_type="dict",
            )
            return {
                "id": user_id,
                "name": user_data["name"],
                "email": user_data["email"],
            }
        else:
            return {"error": "User not found"}

    def mock_delete_user(
        self, user_id: int, expected_status_code: Optional[int] = None
    ) -> dict:
        if user_id in range(1, 11):
            return {"message": "User deleted"}
        else:
            return {"error": "User not found"}

    monkeypatch.setattr(Users, "get_user", mock_get_user)
    monkeypatch.setattr(Users, "get_users", mock_get_users)
    monkeypatch.setattr(Users, "create_user", mock_create_user)
    monkeypatch.setattr(Users, "update_user", mock_update_user)
    monkeypatch.setattr(Users, "delete_user", mock_delete_user)

    return Users(social_media_api)


@pytest.fixture
def posts_api(social_media_api):
    return Posts(social_media_api)


@pytest.fixture
def mock_posts_api(monkeypatch, social_media_api):
    def mock_get_post(
        self, post_id: int, expected_status_code: Optional[int] = None
    ) -> dict:
        if post_id in range(1, 11):
            return {
                "id": post_id,
                "title": f"Post Title {post_id}",
                "content": "Post content",
                "user_id": 1,
            }
        else:
            return {"error": "Post not found"}

    def mock_get_posts(self, expected_status_code: Optional[int] = None) -> list[dict]:
        return [
            {
                "id": post_id,
                "title": f"Post Title {post_id}",
                "content": "Post content",
                "user_id": 1,
            }
            for post_id in range(1, 11)
        ]

    def mock_create_post(
        self, post_data: dict, expected_status_code: Optional[int] = None
    ) -> dict:
        try:
            validate_data_against_model(
                response_data=post_data,
                expected_model=PostCreate,
                expected_response_data_type="dict",
            )
            return {
                "id": 11,
                "title": post_data["title"],
                "content": post_data["content"],
                "user_id": post_data["user_id"],
            }
        except:
            return {"error": "Post not created"}

    def mock_update_post(
        self, post_id: int, post_data: dict, expected_status_code: Optional[int] = None
    ) -> dict:
        if post_id in range(1, 11):
            validate_data_against_model(
                response_data=post_data,
                expected_model=PostUpdate,
                expected_response_data_type="dict",
            )
            return {
                "id": post_id,
                "title": post_data["title"],
                "content": post_data["content"],
                "user_id": post_data["user_id"],
            }
        else:
            return {"error": "Post not found"}

    def mock_delete_post(
        self, post_id: int, expected_status_code: Optional[int] = None
    ) -> dict:
        if post_id in range(1, 11):
            return {"message": "Post deleted"}
        else:
            return {"error": "Post not found"}

    monkeypatch.setattr(Posts, "get_post", mock_get_post)
    monkeypatch.setattr(Posts, "get_posts", mock_get_posts)
    monkeypatch.setattr(Posts, "create_post", mock_create_post)
    monkeypatch.setattr(Posts, "update_post", mock_update_post)
    monkeypatch.setattr(Posts, "delete_post", mock_delete_post)

    return Posts(social_media_api)
