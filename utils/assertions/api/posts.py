from __future__ import annotations

from operator import length_hint

from models.posts import Post, PostList, PostUpdate
from utils.assertions.base.expect import expect


def assert_post(
        expected_post: Post,
        actual_post: Post | PostUpdate
):
    if isinstance(actual_post, Post):
        expect(expected_post['id']) \
            .to_be_equal(actual_post.id)

    expect(expected_post['title']) \
        .to_be_equal(actual_post.title)

    expect(expected_post['content']) \
        .to_be_equal(actual_post.content)

    expect(expected_post['user_id']) \
        .to_be_equal(actual_post.user_id)


def assert_users(
        expected_users: PostList,
        actual_users: PostList
):
    assert length_hint(actual_users) == length_hint(expected_users)
    assert all([a == b for a, b in zip(actual_users, expected_users)])
