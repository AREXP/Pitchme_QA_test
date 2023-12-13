from requests import Response

from models.users import User, UserCreate, UserUpdate, UserList
from utils.clients.http.client import APIClient
from utils.constants.routes import APIRoutes


class UsersClient(APIClient):

    def get_users_api(self) -> Response:
        return self.client.get(APIRoutes.USERS)

    def get_user_api(self, user_id: int) -> Response:
        return self.client.get(f'{APIRoutes.USERS}/{user_id}')

    def create_user_api(self, payload: UserCreate) -> Response:
        return self.client.post(APIRoutes.USERS, json=payload.model_dump(by_alias=True))

    def update_user_api(self, user_id: int, payload: UserUpdate) -> Response:
        return self.client.put(
            f'{APIRoutes.USERS}/{user_id}',
            json=payload.model_dump(by_alias=True)
        )

    def delete_user_api(self, user_id: int) -> Response:
        return self.client.delete(f'{APIRoutes.USERS}/{user_id}')

    def create_user(self) -> User:
        payload = UserCreate()

        response = self.create_user_api(payload)
        return User(**response.json())
