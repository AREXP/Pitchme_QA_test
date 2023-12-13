from requests import Response

from models.posts import Post, PostCreate, PostUpdate, PostList
from utils.clients.http.client import APIClient
from utils.constants.routes import APIRoutes


class PostsClient(APIClient):

    def get_posts_api(self) -> Response:
        return self.client.get(APIRoutes.POSTS)

    def get_post_api(self, post_id: int) -> Response:
        return self.client.get(f'{APIRoutes.POSTS}/{post_id}')

    def create_post_api(self, payload: PostCreate) -> Response:
        return self.client.post(APIRoutes.POSTS, json=payload.model_dump(by_alias=True))

    def update_post_api(self, post_id: int, payload: PostUpdate) -> Response:
        return self.client.put(
            f'{APIRoutes.POSTS}/{post_id}',
            json=payload.model_dump(by_alias=True)
        )

    def delete_post_api(self, post_id: int) -> Response:
        return self.client.delete(f'{APIRoutes.POSTS}/{post_id}')

    def create_post(self) -> Post:
        payload = PostCreate()

        response = self.create_post_api(payload)
        return Post(**response.json())
