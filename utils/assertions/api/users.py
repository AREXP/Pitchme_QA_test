from __future__ import annotations

from operator import length_hint

from models.users import User, UserList, UserUpdate
from utils.assertions.base.expect import expect


def assert_user(
        expected_user: User,
        actual_user: User | UserUpdate
):
    if isinstance(actual_user, User):
        expect(expected_user['id']) \
            .to_be_equal(actual_user.id)

    expect(expected_user['name']) \
        .to_be_equal(actual_user.name)

    expect(expected_user['email']) \
        .to_be_equal(actual_user.email)


def assert_users(
        expected_users: UserList,
        actual_users: UserList
):
    assert length_hint(actual_users) == length_hint(expected_users)
    assert all([a == b for a, b in zip(actual_users, expected_users)])
