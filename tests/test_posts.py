from helpers import validate_data_against_model
from schemas import Post


class TestGetPosts:
    """Tests on retrieving posts"""

    def test_get_all_posts(self, mock_posts_api):
        """Test that all posts can be retrieved"""
        posts = mock_posts_api.get_posts(expected_status_code=200)
        for post in posts:
            validate_data_against_model(
                response_data=post,
                expected_model=Post,
                expected_response_data_type="dict",
            )

    def test_get_post_by_id(self, mock_posts_api):
        """Test that post can be retrieved by id"""
        post_id = 1
        post = mock_posts_api.get_post(post_id=post_id, expected_status_code=200)
        validate_data_against_model(
            response_data=post, expected_model=Post, expected_response_data_type="dict",
        )
        assert post["id"] == post_id

    def test_get_non_existing_post(self, mock_posts_api):
        """Test that non existing post returns 404"""
        post_id = 999
        result = mock_posts_api.get_post(post_id=post_id, expected_status_code=404)
        assert result == {"error": "Post not found"}


class TestCreatePosts:
    """Tests on creating posts"""

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
        assert result == {"error": "Post not created"}, f"Expected '{'error': 'Post not created'}', but got '{result}'"
