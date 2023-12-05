from typing import Optional, Union

import requests


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


class Users(SocialMediaAPI):

    USERS = "/users"
    GET_USER_BY_ID = "/user/{user_id}"

    def __init__(self, social_media_api: SocialMediaAPI):
        super().__init__(base_url=social_media_api.base_url)

    def get_user(
        self, user_id: int, expected_status_code: Optional[int] = None
    ) -> dict:
        return self.get(
            self.GET_USER_BY_ID.format(user_id=user_id),
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
