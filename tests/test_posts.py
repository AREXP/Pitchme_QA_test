import uuid

import pytest

from helpers import validate_data_against_model
from schemas import Post
from base import TEST_ID_FOR_DELETE_OR_UPDATE, TEST_ID_NON_EXISTING


@pytest.mark.posts
class TestGetPosts:
    """Tests on retrieving posts"""

    @pytest.mark.parametrize(
        "post_id",
        [
            pytest.param(1, marks=pytest.mark.smoke),
            *range(2, 11),
        ],  # 1 is for smoke test
    )
    def test_get_post_by_id(self, mock_posts_api, post_id):
        """Test that post can be retrieved by id"""
        post = mock_posts_api.get_post(post_id=post_id, expected_status_code=200)
        validate_data_against_model(
            response_data=post, expected_model=Post, expected_response_data_type="dict",
        )
        assert post["id"] == post_id

    @pytest.mark.negative
    def test_get_non_existing_post(self, mock_posts_api):
        """Test that non existing post returns 404"""
        post_id = uuid.uuid4().int  # Non existing post id
        result = mock_posts_api.get_post(post_id=post_id, expected_status_code=404)
        assert result == {"error": "Post not found"}

    def test_get_all_posts(self, mock_posts_api):
        """Test that all posts can be retrieved"""
        posts = mock_posts_api.get_posts(expected_status_code=200)
        for post in posts:
            validate_data_against_model(
                response_data=post,
                expected_model=Post,
                expected_response_data_type="dict",
            )


@pytest.mark.posts
class TestCreatePosts:
    """Tests on creating posts"""

    @pytest.mark.smoke
    def test_create_post(self, mock_posts_api):
        """Test that post can be created"""
        post_data = {"title": "New Post", "content": "New post content", "user_id": 1}
        created_post = mock_posts_api.create_post(
            post_data=post_data, expected_status_code=201
        )
        validate_data_against_model(
            response_data=created_post,
            expected_model=Post,
            expected_response_data_type="dict",
        )
        assert created_post["title"] == post_data["title"]

    # Positive regression scenarios with expected success
    positive_post_test_data = [
        pytest.param("Valid Title", "Valid content.", 1, 201, id="Valid Post"),
        pytest.param("Max Length Title", "a" * 255, 1, 201, id="Max Title Length"),
        pytest.param(
            "Title With Emoji 🔥", "Content with emoji 🚀", 1, 201, id="Title With Emoji"
        ),
        pytest.param(
            "Valid Title", "<strong>Bold Content</strong>", 1, 201, id="HTML Content"
        ),
        pytest.param(
            "Title Only, Content is empty string", "", 1, 201, id="Title Only"
        ),
    ]

    @pytest.mark.regression
    @pytest.mark.parametrize(
        "title, content, user_id, expected_status", positive_post_test_data
    )
    def test_create_post_positive(
        self, mock_posts_api, title, content, user_id, expected_status
    ):
        post_data = {"title": title, "content": content, "user_id": user_id}

        created_post = mock_posts_api.create_post(
            post_data=post_data, expected_status_code=expected_status
        )
        # Validate the response against the post schema.
        validate_data_against_model(
            response_data=created_post,
            expected_model=Post,
            expected_response_data_type="dict",
        )

        assert (
            created_post["title"] == title
        ), f"Expected title to be '{title}' but found '{created_post['title']}'"
        assert (
            created_post["content"] == content
        ), f"Expected content to be '{content}' but found '{created_post['content']}'"

    # Negative regression scenarios with expected failures
    negative_post_test_data = [
        pytest.param(None, "Content with no title", 1, 400, id="None in Title"),
        pytest.param("Valid Title", None, 1, 400, id="None in Content"),
        pytest.param(
            "Valid Title", "Content", TEST_ID_NON_EXISTING, 404, id="Non-existing User"
        ),
        pytest.param("Valid Title", "Content", 0, 400, id="Invalid User Zero"),
    ]

    @pytest.mark.regression
    @pytest.mark.negative
    @pytest.mark.parametrize(
        "title, content, user_id, expected_status", negative_post_test_data
    )
    def test_create_post_negative(
        self, mock_posts_api, title, content, user_id, expected_status
    ):
        post_data = {"title": title, "content": content, "user_id": user_id}
        post = mock_posts_api.create_post(
            post_data=post_data, expected_status_code=expected_status
        )
        assert post == {
            "error": "Post not created"
        }, f"Expected '{'error': 'Post not created'}', but got '{post}'"


@pytest.mark.posts
class TestUpdatePost:
    """Tests on updating posts."""

    def test_update_existing_post(self, mock_posts_api):
        """Test updating an existing post."""
        posts_api = mock_posts_api  # TODO: Remove after API is implemented
        post_id_for_update_delete = TEST_ID_FOR_DELETE_OR_UPDATE
        updated_post_data = {
            "title": "Updated Post",
            "content": "Updated post content",
            "user_id": 1,
        }
        result = posts_api.update_post(
            post_id=post_id_for_update_delete,
            post_data=updated_post_data,
            expected_status_code=200,
        )
        assert (
            result["id"] == post_id_for_update_delete
        ), f"Expected post id = '{post_id_for_update_delete}', but got '{result['id']}'"
        assert (
            result["title"] == updated_post_data["title"]
        ), f"Expected post title = '{updated_post_data['title']}', but got '{result['title']}'"
        assert (
            result["content"] == updated_post_data["content"]
        ), f"Expected post content = '{updated_post_data['content']}', but got '{result['content']}'"

    @pytest.mark.negative
    def test_update_non_existing_post(self, mock_posts_api):
        """Test that updating a non-existing post returns a 404."""
        posts_api = mock_posts_api  # TODO: Remove after API is implemented
        non_existing_post_id = TEST_ID_NON_EXISTING
        updated_post_data = {
            "title": "Updated Post",
            "content": "Updated post content",
            "user_id": 1,
        }
        result = posts_api.update_post(
            post_id=non_existing_post_id,
            post_data=updated_post_data,
            expected_status_code=404,
        )
        assert result == {
            "error": "Post not found"
        }, f"Expected '{'error': 'Post not found'}', but got '{result}'"


@pytest.mark.posts
class TestDeletePost:
    """Tests on deleting posts."""

    @pytest.mark.smoke
    def test_delete_existing_post(self, mock_posts_api):
        """Test that an existing post can be deleted."""
        posts_api = mock_posts_api  # TODO: Remove after API is implemented
        post_id_for_update_delete = TEST_ID_FOR_DELETE_OR_UPDATE
        result = posts_api.delete_post(
            post_id=post_id_for_update_delete, expected_status_code=200
        )
        assert result == {
            "message": "Post deleted"
        }, f"Expected '{'message': 'Post deleted'}', but got '{result}'"

    @pytest.mark.negative
    def test_delete_non_existing_post(self, mock_posts_api):
        """Test that an attempt to delete a non-existing post returns a 404."""
        posts_api = mock_posts_api  # TODO: Remove after API is implemented
        non_existing_post_id = TEST_ID_NON_EXISTING
        result = posts_api.delete_post(
            post_id=non_existing_post_id, expected_status_code=404
        )
        assert result == {
            "error": "Post not found"
        }, f"Expected '{'error': 'Post not found'}', but got '{result}'"
