from http import HTTPStatus
from typing import cast

import pytest

from base.api.users_api import UsersClient
from models.users import (User, UserList,
                          UserCreate, UserUpdate)
from utils.assertions.api.users import assert_user
from utils.assertions.base.solutions import assert_status_code
from utils.assertions.schema import validate_schema


@pytest.mark.users
class TestUsers:

    def test_get_users(self, class_users_client: UsersClient):
        response = class_users_client.get_users_api()
        json_response: list[UserList] = response.json()

        assert_status_code(response.status_code, HTTPStatus.OK)

        validate_schema(
            cast(json_response, list[UserList]), UserList.model_json_schema())

    def test_create_user(self, class_users_client: UsersClient):
        payload = UserCreate()
        response = class_users_client.create_user_api(payload)
        json_response: UserCreate = response.json()

        assert_status_code(response.status_code, HTTPStatus.CREATED)
        assert_user(
            expected_user=cast(json_response, UserCreate),
            actual_user=cast(payload, UserCreate)
        )

        validate_schema(cast(json_response, UserCreate), UserCreate.model_json_schema())

    def test_get_user(
            self,
            function_user: User,
            class_users_client: UsersClient
    ):
        response = class_users_client.get_user_api(
            function_user.id
        )

        json_response: User = response.json()

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_user(
            expected_user=json_response,
            actual_user=function_user
        )

        validate_schema(cast(json_response, User), User.model_json_schema())

    def test_update_user(
            self,
            function_user: User,
            class_users_client: UsersClient
    ):
        payload = UserUpdate()

        response = class_users_client.update_user_api(
            function_user.id, payload
        )

        json_response: User = response.json()

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_user(
            expected_user=json_response,
            actual_user=payload
        )

        validate_schema(cast(json_response, UserUpdate), UserUpdate.model_json_schema())

    def test_delete_user(
            self,
            function_user: User,
            class_users_client: UsersClient
    ):
        delete_user_response = class_users_client.delete_user_api(
            function_user.id
        )
        get_user_response = class_users_client.get_user_api(
            function_user.id
        )

        assert_status_code(delete_user_response.status_code, HTTPStatus.OK)
        assert_status_code(
            get_user_response.status_code, HTTPStatus.NOT_FOUND
        )
