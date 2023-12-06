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

    @pytest.mark.negative
    def test_failed_to_create_post_missing_field(self, mock_posts_api):
        """Test that post cannot be created with missing data fields"""
        post_data = {
            "title": "Incomplete Post",
            # Missing 'content'
            "user_id": 1,
        }
        result = mock_posts_api.create_post(
            post_data=post_data, expected_status_code=400
        )
        assert result == {
            "error": "Post not created"
        }, f"Expected '{'error': 'Post not created'}', but got '{result}'"


@pytest.mark.posts
class TestGetPosts:
    """Tests on retrieving posts."""

    @pytest.mark.smoke
    def test_get_all_posts(self, mock_posts_api):
        """Test that all posts can be retrieved."""
        posts_api = mock_posts_api  # TODO: Remove after API is implemented
        posts = posts_api.get_posts(expected_status_code=200)
        for post in posts:
            validate_data_against_model(
                response_data=post,
                expected_model=Post,
                expected_response_data_type="dict",
            )
            assert post["id"], f"Expected non-empty post id, but got '{post['id']}'"
            assert post[
                "title"
            ], f"Expected non-empty post title, but got '{post['title']}'"
            assert post[
                "content"
            ], f"Expected non-empty post content, but got '{post['content']}'"

    @pytest.mark.parametrize(
        "post_id",
        [
            pytest.param(1, marks=pytest.mark.smoke),
            *range(2, 11),
        ],  # 1 is for smoke test
    )
    def test_get_post_by_id(self, mock_posts_api, post_id):
        """Test that post can be retrieved by id."""
        posts_api = mock_posts_api  # TODO: Remove after API is implemented
        post = posts_api.get_post(post_id=post_id, expected_status_code=200)
        validate_data_against_model(
            response_data=post, expected_model=Post, expected_response_data_type="dict"
        )
        assert (
            post["id"] == post_id
        ), f"Expected post id = '{post_id}', but got '{post['id']}'"
        assert post[
            "title"
        ], f"Expected non-empty post title, but got '{post['title']}'"
        assert post[
            "content"
        ], f"Expected non-empty post content, but got '{post['content']}'"

    @pytest.mark.negative
    def test_get_non_existing_post(self, mock_posts_api):
        """Test that non existing post returns 404."""
        posts_api = mock_posts_api  # TODO: Remove after API is implemented
        post_id = TEST_ID_NON_EXISTING  # Non existing post id
        result = posts_api.get_post(post_id=post_id, expected_status_code=404)
        assert result == {
            "error": "Post not found"
        }, f"Expected '{'error': 'Post not found'}', but got '{result}'"


@pytest.mark.posts
class TestCreatePost:
    """Tests on creating posts."""

    @pytest.mark.smoke
    def test_create_post(self, mock_posts_api):
        """Test that post can be created."""
        posts_api = mock_posts_api  # TODO: Remove after API is implemented
        new_post_data = {
            "title": "New Post",
            "content": "New post content",
            "user_id": 1,
        }
        created_post = posts_api.create_post(
            post_data=new_post_data, expected_status_code=201,
        )
        validate_data_against_model(
            response_data=created_post,
            expected_model=Post,
            expected_response_data_type="dict",
        )
        assert (
            created_post["title"] == new_post_data["title"]
        ), f"Expected post title = '{new_post_data['title']}', but got '{created_post['title']}'"
        assert (
            created_post["content"] == new_post_data["content"]
        ), f"Expected post content = '{new_post_data['content']}', but got '{created_post['content']}'"

    @pytest.mark.negative
    def test_failed_to_create_post_without_title(self, mock_posts_api):
        """Test that post cannot be created without title."""
        posts_api = mock_posts_api  # TODO: Remove after API is implemented
        result = posts_api.create_post(
            post_data={"content": "Post content", "user_id": 1},
            expected_status_code=400,
        )
        assert result == {
            "error": "Post not created"
        }, f"Expected '{'error': 'Post not created'}', but got '{result}'"


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
