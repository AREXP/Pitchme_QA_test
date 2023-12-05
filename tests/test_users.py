import uuid
import pytest

from helpers import validate_response_data
from schemas import User


class TestGetUsers:
    """Tests on retrieving users"""

    @pytest.mark.parametrize("user_id", range(1, 11))
    def test_get_user_by_id(self, mock_users_api, user_id):
        """Test that user can be retrieved by id"""
        users_api = mock_users_api  # TODO: Remove after API is implemented
        user = users_api.get_user(user_id=user_id, expected_status_code=200)
        validate_response_data(
            response_data=user, expected_model=User, expected_response_data_type="dict"
        )
        assert (
            user["id"] == user_id
        ), f"Expected user id = '{user_id}', but got '{user['id']}'"
        assert user["name"], f"Expected non-empty user name, but got '{user['name']}'"
        assert user[
            "email"
        ], f"Expected non-empty user email, but got '{user['email']}'"

    def test_get_non_existing_user(self, mock_users_api):
        """Test that non existing user returns 404"""
        users_api = mock_users_api  # TODO: Remove after API is implemented
        non_existing_user_id = uuid.uuid4().int
        result = users_api.get_user(
            user_id=non_existing_user_id, expected_status_code=404
        )
        assert result == {
            "error": "User not found"
        }, f"Expected '{'error': 'User not found'}', but got '{result}'"

    def test_get_all_users(self, mock_users_api):
        """Test that all users can be retrieved"""
        users_api = mock_users_api  # TODO: Remove after API is implemented
        users = users_api.get_users(expected_status_code=200)
        for user in users:
            validate_response_data(
                response_data=user,
                expected_model=User,
                expected_response_data_type="dict",
            )
            assert user["id"], f"Expected non-empty user id, but got '{user['id']}'"
            assert user[
                "name"
            ], f"Expected non-empty user name, but got '{user['name']}'"
            assert user[
                "email"
            ], f"Expected non-empty user email, but got '{user['email']}'"
