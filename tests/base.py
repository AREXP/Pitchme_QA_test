from typing import Optional, Union

import requests

TEST_ID_FOR_DELETE_OR_UPDATE = "1" * 32  # to use in tests to avoid changing real data
TEST_ID_NON_EXISTING = "2" * 32  # to use in tests to avoid changing real data
MAX_NAME_LENGTH = 50


class SocialMediaAPI:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.default_headers = {"Content-type": "application/json; charset=UTF-8"}

    def get(
        self, endpoint: str, expected_status_code: Optional[int] = None
    ) -> Union[dict, list]:
        if not endpoint.startswith("/"):
            endpoint = "/" + endpoint
        url = self.base_url + endpoint

        response = requests.get(url=url, headers=self.default_headers)

        if expected_status_code:
            assert (
                response.status_code == expected_status_code
            ), f"Expected status code ='{expected_status_code}', but request to '{url}' returned '{response.status_code}', response body: \n'{response.text}'"

        result_json = response.json()
        return result_json

    def post(
        self, endpoint: str, data: dict, expected_status_code: Optional[int] = None
    ) -> Union[dict, list]:
        if not endpoint.startswith("/"):
            endpoint = "/" + endpoint
        url = self.base_url + endpoint

        response = requests.post(url=url, headers=self.default_headers, json=data)

        if expected_status_code:
            assert (
                response.status_code == expected_status_code
            ), f"Expected status code ='{expected_status_code}', but request to '{url}' returned '{response.status_code}', response body: \n'{response.text}'"

        result_json = response.json()
        return result_json

    def put(
        self, endpoint: str, data: dict, expected_status_code: Optional[int] = None
    ) -> Union[dict, list]:
        if not endpoint.startswith("/"):
            endpoint = "/" + endpoint
        url = self.base_url + endpoint

        response = requests.put(url=url, headers=self.default_headers, json=data)

        if expected_status_code:
            assert (
                response.status_code == expected_status_code
            ), f"Expected status code ='{expected_status_code}', but request to '{url}' returned '{response.status_code}', response body: \n'{response.text}'"

        result_json = response.json()
        return result_json

    def delete(
        self, endpoint: str, expected_status_code: Optional[int] = None
    ) -> Union[dict, list]:
        if not endpoint.startswith("/"):
            endpoint = "/" + endpoint
        url = self.base_url + endpoint

        response = requests.delete(url=url, headers=self.default_headers)

        if expected_status_code:
            assert (
                response.status_code == expected_status_code
            ), f"Expected status code ='{expected_status_code}', but request to '{url}' returned '{response.status_code}', response body: \n'{response.text}'"

        result_json = response.json()
        return result_json


class Users(SocialMediaAPI):

    USERS = "/users"
    USER_BY_ID = "/user/{user_id}"

    def __init__(self, social_media_api: SocialMediaAPI):
        super().__init__(base_url=social_media_api.base_url)

    def get_user(
        self, user_id: int, expected_status_code: Optional[int] = None
    ) -> dict:
        return self.get(
            self.USER_BY_ID.format(user_id=user_id),
            expected_status_code=expected_status_code,
        )

    def get_users(self, expected_status_code: Optional[int] = None) -> list[dict]:
        return self.get(self.USERS, expected_status_code=expected_status_code)

    def create_user(
        self, user_data: dict, expected_status_code: Optional[int] = None
    ) -> dict:
        return self.post(
            self.USERS, data=user_data, expected_status_code=expected_status_code
        )

    def update_user(
        self, user_id: int, user_data: dict, expected_status_code: Optional[int] = None
    ) -> dict:
        endpoint = self.USER_BY_ID.format(user_id=user_id)
        return self.put(
            endpoint, data=user_data, expected_status_code=expected_status_code
        )

    def delete_user(
        self, user_id: int, expected_status_code: Optional[int] = None
    ) -> dict:
        endpoint = self.USER_BY_ID.format(user_id=user_id)
        return self.delete(endpoint, expected_status_code=expected_status_code)


class Posts(SocialMediaAPI):

    POSTS = "/posts"
    POST_BY_ID = "/posts/{post_id}"

    def get_post(
        self, post_id: int, expected_status_code: Optional[int] = None
    ) -> dict:
        return self.get(
            self.POST_BY_ID.format(post_id=post_id),
            expected_status_code=expected_status_code,
        )

    def get_posts(self, expected_status_code: Optional[int] = None) -> list[dict]:
        return self.get(self.POSTS, expected_status_code=expected_status_code)

    def create_post(
        self, post_data: dict, expected_status_code: Optional[int] = None
    ) -> dict:
        return self.post(
            self.POSTS, data=post_data, expected_status_code=expected_status_code
        )

    def update_post(
        self, post_id: int, post_data: dict, expected_status_code: Optional[int] = None
    ) -> dict:
        endpoint = self.POST_BY_ID.format(post_id=post_id)
        return self.put(
            endpoint, data=post_data, expected_status_code=expected_status_code
        )

    def delete_post(
        self, post_id: int, expected_status_code: Optional[int] = None
    ) -> dict:
        endpoint = self.POST_BY_ID.format(post_id=post_id)
        return self.delete(endpoint, expected_status_code=expected_status_code)
