from typing import Any, Dict

import pydantic

from smqtk_core import Plugfigurable, Pluggable, Configurable


def test_inheritance():
    assert issubclass(Plugfigurable, Pluggable)
    assert issubclass(Plugfigurable, Configurable)

class MyBaseClass(Plugfigurable):
    def __init__(self, foo: str) -> None:
        self.foo = foo

    def get_config(self) -> Dict[str, Any]:
        return {"foo": self.foo}


class MyObject(MyBaseClass):
    def __init__(self, foo: str, *, bar: int):
        super().__init__(foo)
        self.bar = bar

    def get_config(self) -> Dict[str, Any]:
        cfg = super().get_config()
        cfg["bar"] = self.bar
        return cfg

class MyModel(pydantic.BaseModel):
    any_object: MyBaseClass

def test_pydantic_e2e():
    config = {"foo": "foofoo", "bar": 42}
    obj = {
        "any_object": {
            "type": (t := f"{MyObject.__module__}.{MyObject.__name__}"),
            t: config,
        }
    }
    my_model = MyModel.model_validate(obj)

    assert isinstance(my_model.any_object, MyObject)
    assert my_model.any_object.get_config() == config
    assert my_model.model_dump(mode="json") == obj
