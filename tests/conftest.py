import pytest

from tests.base import SocialMediaAPI, Users


def pytest_addoption(parser):
    parser.addoption(
        "--base_url",
        action="store",
        default="https://pitch.me",
        help="Base URL of the application under test",
    )


@pytest.fixture(autouse=True, scope="session")
def base_url(request):
    return request.config.getoption("--base_url")


@pytest.fixture
def social_media_api(base_url):
    return SocialMediaAPI(base_url)


@pytest.fixture
def users_api(social_media_api):
    return Users(social_media_api)
