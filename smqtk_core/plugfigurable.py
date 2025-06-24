from __future__ import annotations

import abc
from collections.abc import Mapping
from typing import Any

from .configuration import Configurable, from_config_dict
from .plugin import Pluggable

try:
    import pydantic
    from pydantic_core import core_schema

    PYDANTIC_2_AVAILABLE = tuple(map(int, pydantic.__version__.split(".")[:3])) >= (2,)
except (ImportError, AttributeError):
    PYDANTIC_2_AVAILABLE = False


class Plugfigurable(Pluggable, Configurable, metaclass=abc.ABCMeta):
    """
    When you don't want to have to constantly inherit from two mixin classes
    all the time, we provide this as a convenience that descends from both
    mixin classes: Pluggable and Configurable.
    """

    if PYDANTIC_2_AVAILABLE:
        @classmethod
        def __get_pydantic_core_schema__(
            cls, _source_type: Any, _handler: pydantic.GetCoreSchemaHandler
        ) -> core_schema.CoreSchema:
            def from_config(value: Mapping[str, Any]) -> Plugfigurable:
                return from_config_dict(dict(value), cls.get_impls())

            def to_config(value: Plugfigurable) -> dict[str, Any]:
                t = f"{type(value).__module__}.{type(value).__name__}"
                return {"type": t, t: value.get_config()}

            from_config_dict_schema = core_schema.chain_schema(
                [
                    core_schema.dict_schema(
                        keys_schema=core_schema.str_schema(),
                        values_schema=core_schema.any_schema(),
                    ),
                    core_schema.no_info_plain_validator_function(from_config),
                ]
            )

            return core_schema.json_or_python_schema(
                json_schema=from_config_dict_schema,
                python_schema=core_schema.union_schema(
                    [
                        core_schema.is_instance_schema(cls),
                        from_config_dict_schema,
                    ]
                ),
                serialization=core_schema.plain_serializer_function_ser_schema(to_config),
            )