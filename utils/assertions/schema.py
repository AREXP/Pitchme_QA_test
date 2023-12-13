from pydantic import json


def validate_schema(instance: dict, schema: dict) -> None:
    json.validate(instance=instance, schema=schema)
