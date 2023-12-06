import uuid

import pytest
from helpers import validate_data_against_model
from base import TEST_ID_FOR_DELETE_OR_UPDATE, TEST_ID_NON_EXISTING, MAX_NAME_LENGTH

from schemas import User


@pytest.mark.users
class TestGetUsers:
    """Tests on retrieving users"""

    @pytest.mark.parametrize(
        "user_id",
        [
            pytest.param(1, marks=pytest.mark.smoke),
            *range(2, 11),
        ],  # 1 is for smoke test
    )
    def test_get_user_by_id(self, mock_users_api, user_id):
        """Test that user can be retrieved by id"""
        users_api = mock_users_api  # TODO: Remove after API is implemented
        user = users_api.get_user(user_id=user_id, expected_status_code=200)
        validate_data_against_model(
            response_data=user, expected_model=User, expected_response_data_type="dict"
        )
        assert (
            user["id"] == user_id
        ), f"Expected user id = '{user_id}', but got '{user['id']}'"
        assert user["name"], f"Expected non-empty user name, but got '{user['name']}'"
        assert user[
            "email"
        ], f"Expected non-empty user email, but got '{user['email']}'"

    @pytest.mark.negative
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

    @pytest.mark.smoke
    def test_get_all_users(self, mock_users_api):
        """Test that all users can be retrieved"""
        users_api = mock_users_api  # TODO: Remove after API is implemented
        users = users_api.get_users(expected_status_code=200)
        for user in users:
            validate_data_against_model(
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


@pytest.mark.users
class TestCreateUser:
    """Tests on creating users"""

    @pytest.mark.smoke
    def test_create_user(self, mock_users_api):
        """Test that user can be created"""
        users_api = mock_users_api  # TODO: Remove after API is implemented
        postfix = uuid.uuid4().int
        user_name = f"user_{postfix}"
        user_email = f"user_{postfix}@example.com"
        created_user = users_api.create_user(
            user_data={"name": user_name, "email": user_email},
            expected_status_code=201,
        )
        validate_data_against_model(
            response_data=created_user,
            expected_model=User,
            expected_response_data_type="dict",
        )
        assert created_user[
            "id"
        ], f"Expected non-empty user id, but got '{created_user['id']}'"
        assert (
            created_user["name"] == user_name
        ), f"Expected user name = '{user_name}', but got '{created_user['name']}'"
        assert (
            created_user["email"] == user_email
        ), f"Expected user email = '{user_email}', but got '{created_user['email']}'"

    @pytest.mark.negative
    def test_failed_to_create_user_without_name(self, mock_users_api):
        """Test that user cannot be created without name"""
        users_api = mock_users_api  # TODO: Remove after API is implemented
        result = users_api.create_user(
            user_data={"email": "john@example.com"}, expected_status_code=400,
        )
        assert result == {
            "error": "User not created"
        }, f"Expected '{'error': 'User not created'}', but got '{result}'"

    @pytest.mark.negative
    def test_failed_to_create_user_without_email(self, mock_users_api):
        """Test that user cannot be created without email"""
        users_api = mock_users_api  # TODO: Remove after API is implemented
        result = users_api.create_user(
            user_data={"name": "John Doe"}, expected_status_code=400,
        )
        assert result == {
            "error": "User not created"
        }, f"Expected '{'error': 'User not created'}', but got '{result}'"

    # Positive regression scenarios with expected success
    positive_user_test_data = [
        pytest.param(f"JohnDoe", f"john.doe@example.com", 201, id="Regular User"),
        pytest.param(
            "a" * MAX_NAME_LENGTH, f"long.name@example.com", 201, id="Max Length Name"
        ),
        pytest.param(
            "Jane.Doe-O'Riley",
            f"jane.doe.o'riley@example.com",
            201,
            id="Special Characters In Name",
        ),
        pytest.param(
            "Tim", f"tim@subdomain.example.com", 201, id="Email With Subdomains"
        ),
        pytest.param("Eve", f"eve@example.co.uk", 201, id="Email Different TLD"),
    ]

    @pytest.mark.users
    @pytest.mark.regression
    @pytest.mark.parametrize(
        "user_name, user_email, expected_status", positive_user_test_data
    )
    def test_create_user_positive(
        self, mock_users_api, user_name, user_email, expected_status
    ):
        user_data = {"name": user_name, "email": user_email}
        created_user = mock_users_api.create_user(
            user_data=user_data, expected_status_code=expected_status
        )

        # Validate the response against the user schema.
        validate_data_against_model(
            response_data=created_user,
            expected_model=User,
            expected_response_data_type="dict",
        )

        assert (
            created_user["name"] == user_name
        ), f"Expected user name to be '{user_name}'"
        assert (
            created_user["email"] == user_email
        ), f"Expected user email to be '{user_email}'"

    # Negative regression scenarios with expected failures
    negative_user_test_data = [
        pytest.param("JohnDoe", f"copycat@example.com", 400, id="Email Already Taken"),
        pytest.param(None, f"no.name@example.com", 400, id="Empty Name"),
        pytest.param(
            "Jane Doe", f"invalid_email_format", 400, id="Invalid Email Format"
        ),
        pytest.param(
            "a" * (MAX_NAME_LENGTH + 1),
            f"too.long.name@example.com",
            400,
            id="Name Too Long",
        ),
        pytest.param("JohnNoEmail", None, 400, id="Missing Email"),
    ]

    @pytest.mark.users
    @pytest.mark.negative
    @pytest.mark.regression
    @pytest.mark.parametrize(
        "user_name, user_email, expected_status", negative_user_test_data
    )
    def test_create_user_negative(
        self, mock_users_api, user_name, user_email, expected_status
    ):
        user_data = {"name": user_name, "email": user_email}

        user = mock_users_api.create_user(
            user_data=user_data, expected_status_code=expected_status
        )
        assert user == {
            "error": "User not created"
        }, f"Expected '{'error': 'User not created'}', but got '{user}'"


@pytest.mark.users
class TestUpdateUser:
    """Tests on updating users"""

    @pytest.mark.smoke
    def test_update_existing_user(self, mock_users_api):
        user_id = TEST_ID_FOR_DELETE_OR_UPDATE  # TODO: Remove after API is implemented
        updated_data = {"name": "Updated Name", "email": "updated@example.com"}
        result = mock_users_api.update_user(
            user_id=user_id, user_data=updated_data, expected_status_code=200
        )
        assert result["id"] == user_id
        assert result["name"] == updated_data["name"]
        assert result["email"] == updated_data["email"]

    @pytest.mark.negative
    def test_update_non_existing_user(self, mock_users_api):
        user_id = TEST_ID_NON_EXISTING  # TODO: Remove after API is implemented
        updated_data = {"name": "Nonexistent Name", "email": "nonexistent@example.com"}
        result = mock_users_api.update_user(
            user_id=user_id, user_data=updated_data, expected_status_code=404
        )
        assert result == {"error": "User not found"}


@pytest.mark.users
class TestDeleteUser:
    """Tests on deleting users"""

    @pytest.mark.smoke
    def test_delete_existing_user(self, mock_users_api):
        # create user to delete
        user = mock_users_api.create_user(
            user_data={"name": "User to delete", "email": "delete@me.com"},
        )
        user[
            "id"
        ] = TEST_ID_FOR_DELETE_OR_UPDATE  # TODO: Remove after API is implemented
        # delete user
        result = mock_users_api.delete_user(
            user_id=user["id"], expected_status_code=200
        )
        assert result == {"message": "User deleted"}
        # check that user does not exist after deleting
        user["id"] = TEST_ID_NON_EXISTING  # TODO: Remove after API is implemented
        result = mock_users_api.get_user(
            user_id=user["id"], expected_status_code=404
        )  # TODO: Uncomment after API is implemented

    @pytest.mark.negative
    def test_delete_non_existing_user(self, mock_users_api):
        user_id = TEST_ID_NON_EXISTING  # TODO: Remove after API is implemented
        result = mock_users_api.delete_user(user_id=user_id, expected_status_code=404)
        assert result == {"error": "User not found"}
