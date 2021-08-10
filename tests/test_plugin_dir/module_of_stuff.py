"""
Test module defining various things for testing type value extraction.
"""
import abc
import os  # noqa: F401
from pathlib import Path  # noqa: F401

a = 1  # an instance
b = str  # exporting an alias to the type!


class ClassDefinition(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def cool_thing(self) -> str: ...


class Derived(ClassDefinition):

    def cool_thing(self) -> str:
        """ Some implementation, content doesn't matter. """


class StillAbstract(ClassDefinition):
    ...


class_instance = Derived()
