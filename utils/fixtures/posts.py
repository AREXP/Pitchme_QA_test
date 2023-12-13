import pytest

from base.api.posts_api import PostsClient
from models.authentication import Authentication
from models.posts import Post
from utils.clients.http.builder import get_http_client


@pytest.fixture(scope="class")
def class_posts_client() -> PostsClient:
    client = get_http_client(auth=Authentication())

    return PostsClient(client=client)


@pytest.fixture(scope='function')
def function_post(class_posts_client: PostsClient) -> Post:
    post = class_posts_client.create_post()
    yield post

    class_posts_client.delete_post_api(post.id)
