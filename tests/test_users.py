import uuid

import pytest


class TestGetUsers:
    """Tests on retrieving users"""

    @pytest.mark.parametrize("user_id", range(1, 11))
    def test_get_user_by_id(self, users_api, user_id):
        """Test that user can be retrieved by id"""
        user = users_api.get_user(user_id=user_id, expected_status_code=200)
        assert isinstance(
            user, dict
        ), f"Expected type 'dict', but got '{type(user)}' for user '{user}'"
        for (field, field_type) in [
            ("id", int),
            ("name", str),
            ("email", str),
        ]:
            assert isinstance(
                user[field], field_type
            ), f"Expected type '{field_type}', but got '{type(user[field])}' for user '{user}'"

    def test_get_non_existing_user(self, users_api):
        """Test that non existing user returns 404"""
        non_existing_user_id = uuid.uuid4().int
        users_api.get_user(user_id=non_existing_user_id, expected_status_code=404)

    def test_get_all_users(self, users_api):
        """Test that all users can be retrieved"""
        users = users_api.get_users(expected_status_code=200)
        assert isinstance(
            users, list
        ), f"Expected type 'list', but got '{type(users)}' for users '{users}'"
        for user in users:
            assert isinstance(
                user, dict
            ), f"Expected type 'dict', but got '{type(user)}' for user '{user}'"
            for (field, field_type) in [
                ("id", int),
                ("name", str),
                ("email", str),
            ]:
                assert isinstance(
                    user[field], field_type
                ), f"Expected type '{field_type}', but got '{type(user[field])}' for user '{user}'"
