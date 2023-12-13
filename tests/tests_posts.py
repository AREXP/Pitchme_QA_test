from http import HTTPStatus
from typing import cast

import pytest

from base.api.posts_api import PostsClient
from models.posts import (Post, PostList,
                          PostCreate, PostUpdate)
from utils.assertions.api.posts import assert_post
from utils.assertions.base.solutions import assert_status_code
from utils.assertions.schema import validate_schema


@pytest.mark.posts
class TestPosts:

    def test_get_posts(self, class_posts_client: PostsClient):
        response = class_posts_client.get_posts_api()
        json_response: list[PostList] = response.json()

        assert_status_code(response.status_code, HTTPStatus.OK)

        validate_schema(
            cast(json_response, list[PostList]), PostList.model_json_schema())

    def test_create_post(self, class_posts_client: PostsClient):
        payload = PostCreate()
        response = class_posts_client.create_post_api(payload)
        json_response: PostCreate = response.json()

        assert_status_code(response.status_code, HTTPStatus.CREATED)
        assert_post(
            expected_post=cast(json_response, PostCreate),
            actual_post=cast(payload, PostCreate)
        )

        validate_schema(cast(json_response, Post), Post.model_json_schema())

    def test_get_user(
            self,
            function_post: Post,
            class_posts_client: PostsClient
    ):
        response = class_posts_client.get_post_api(
            function_post.id
        )

        json_response: Post = response.json()

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_post(
            expected_post=json_response,
            actual_post=function_post
        )

        validate_schema(cast(json_response, Post), Post.model_json_schema())

    def test_update_post(
            self,
            function_post: Post,
            class_posts_client: PostsClient
    ):
        payload = PostUpdate()

        response = class_posts_client.update_post_api(
            function_post.id, payload
        )

        json_response: Post = response.json()

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_post(
            expected_post=json_response,
            actual_post=payload
        )

        validate_schema(cast(json_response, PostUpdate), Post.model_json_schema())

    def test_delete_user(
            self,
            function_post: Post,
            class_posts_client: PostsClient
    ):
        delete_post_response = class_posts_client.delete_post_api(
            function_post.id
        )
        get_user_response = class_posts_client.get_post_api(
            function_post.id
        )

        assert_status_code(delete_post_response.status_code, HTTPStatus.OK)
        assert_status_code(
            get_user_response.status_code, HTTPStatus.NOT_FOUND
        )
