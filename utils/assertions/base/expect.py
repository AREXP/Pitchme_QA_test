from typing import TypeVar

from utils.assertions.base.assertion_mixin import AssertionMixin

T = TypeVar('T')


def expect(expected: T) -> AssertionMixin:
    assertion = AssertionMixin(expected=expected)

    return assertion
