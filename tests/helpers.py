from typing import Type, Union

import pytest
from pydantic import BaseModel, ValidationError


def validate_data_against_model(
    *,
    expected_model: Type[BaseModel],
    response_data: Union[dict, list, str],
    expected_response_data_type: str = "dict",
):
    """
    Validate response data against a given Pydantic model.

    :param expected_model: The Pydantic model to validate against.
    :param response_data: The response dict to validate.
    :param expected_response_data_type: The type of response data. Can be 'dict', 'list' or 'str'.
    :raises ValidationError: If response data does not conform to given model.
    :return: True if validation passes.
    """
    if expected_response_data_type == "dict":
        assert isinstance(
            response_data, dict
        ), f"Expected type 'dict', but got '{type(response_data)}' for response data '{response_data}'"
    elif expected_response_data_type == "list":
        assert isinstance(
            response_data, list
        ), f"Expected type 'list', but got '{type(response_data)}' for response data '{response_data}'"
    elif expected_response_data_type == "str":
        assert isinstance(
            response_data, str
        ), f"Expected type 'str', but got '{type(response_data)}' for response data '{response_data}'"
    try:
        expected_model.model_validate(response_data)
    except ValidationError as e:
        pytest.fail(f"API response validation failed with error: {e}")

    return True
