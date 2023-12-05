import uuid
import pytest

from helpers import validate_response_data
from schemas import User


class TestGetUsers:
    """Tests on retrieving users"""

    @pytest.mark.parametrize("user_id", range(1, 11))
    def test_get_user_by_id(self, users_api, user_id):
        """Test that user can be retrieved by id"""
        user = users_api.get_user(user_id=user_id, expected_status_code=200)
        validate_response_data(
            response_data=user, expected_model=User, expected_response_data_type="dict"
        )

    def test_get_non_existing_user(self, users_api):
        """Test that non existing user returns 404"""
        non_existing_user_id = uuid.uuid4().int
        users_api.get_user(user_id=non_existing_user_id, expected_status_code=404)

    def test_get_all_users(self, users_api):
        """Test that all users can be retrieved"""
        users = users_api.get_users(expected_status_code=200)
        for user in users:
            validate_response_data(
                response_data=user,
                expected_model=User,
                expected_response_data_type="dict",
            )
