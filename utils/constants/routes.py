from enum import Enum


class APIRoutes(str, Enum):
    USERS = '/users'
    POSTS = '/posts'
    AUTH = '/auth'

    def __str__(self) -> str:
        return self.value
