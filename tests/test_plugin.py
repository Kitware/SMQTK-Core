"""Unit tests for the plugin utility sub-module."""
import abc
import os
import types
from typing import cast
from unittest import mock

import pytest

# noinspection PyProtectedMember
from smqtk_core.plugin import (
    metadata,
    OS_ENV_PATH_SEP,
    is_valid_plugin,
    _collect_types_in_module,
    discover_via_env_var,
    NotAModuleError,
    discover_via_entrypoint_extensions,
    discover_via_subclasses,
    filter_plugin_types,
    Pluggable,
)

from tests.test_plugin_dir import module_of_stuff
from tests.test_plugin_dir import module_of_more_stuff


TYPES_IN_STUFF_MODULE = {
    module_of_stuff.Path,
    str,
    module_of_stuff.ClassDefinition,
    module_of_stuff.Derived,
    module_of_stuff.StillAbstract,
}
TYPES_IN_MORE_STUFF_MODULE = {
    module_of_more_stuff.Path,
    module_of_more_stuff.NewCustomType,
    module_of_more_stuff.AnotherDerived,
    type,
}


###############################################################################
# Tests

class TestIsValidPlugin:
    def test_not_different_type(self) -> None:
        """
        Test that a type is NOT considered a plugin when it's literally the
        interface type.
        """

        class InterfaceType:
            ...

        assert not is_valid_plugin(InterfaceType, InterfaceType)

    def test_not_subclass(self) -> None:
        """
        Test that the return is False when the type is not a direct subclass.
        """

        class InterfaceType:
            ...

        class TestType:
            ...

        assert not is_valid_plugin(TestType, InterfaceType)

    def test_has_abstract_methods(self) -> None:
        """
        Test that False is returned when the test type *is* a sub-class, but
        does not implement all abstract methods.
        """

        class InterfaceType(metaclass=abc.ABCMeta):
            @abc.abstractmethod
            def abs_method(self) -> None:
                """ An abstract method. """

            @property
            @abc.abstractmethod
            def abs_prop(self) -> int:
                """ An abstract property. """

        # noinspection PyAbstractClass
        class ImplementsMethodOnly(InterfaceType):
            # Lingering abstract property
            def abs_method(self) -> None: ...

        # noinspection PyAbstractClass
        class ImplementsPropOnly(InterfaceType):
            # Lingering abstract method
            @property
            def abs_prop(self) -> int: ...

        assert not is_valid_plugin(ImplementsMethodOnly, InterfaceType)
        assert not is_valid_plugin(ImplementsPropOnly, InterfaceType)

    def test_pluggable_usable(self) -> None:
        """
        Test that if input type descends from Pluggable that the is_usable()
        function returning false invalidates it's plugin validity.
        """

        class InterfaceType(Pluggable):
            ...

        class ImplementingTypeFalse(InterfaceType):
            @classmethod
            def is_usable(cls) -> bool:
                return False

        assert not is_valid_plugin(ImplementingTypeFalse, InterfaceType)

        class ImplementingTypeTrue(InterfaceType):
            @classmethod
            def is_usable(cls) -> bool:
                return True

        assert is_valid_plugin(ImplementingTypeTrue, InterfaceType)

    def test_success(self) -> None:
        """
        Test successfully validating a subclass type relative to a parent
        "interface" type.
        """

        class InterfaceType(metaclass=abc.ABCMeta):
            @abc.abstractmethod
            def feature(self) -> int: ...

        class ImplementingType(InterfaceType):
            # is_usable default is True
            def feature(self) -> int: ...

        assert is_valid_plugin(ImplementingType, InterfaceType)


def test_collect_types_in_module() -> None:
    """
    Test that the proper values are returned from the test module.
    """
    assert _collect_types_in_module(cast(types.ModuleType, module_of_stuff)) == TYPES_IN_STUFF_MODULE


class TestDiscoveryViaEnvVar:
    """
    Unit tests for environment variable based discovery of types.
    """

    VAR_NAME = "SOME_SILLY_NAME"

    @mock.patch.dict(os.environ)
    def test_not_set(self) -> None:
        """
        Test when variable of the given name is not set in the environment.
        Nothing should be returned from the discovery.
        """
        # Clear any values in the environ for the test name in if it for some
        #   reason really existed...
        # We're in a mock.patch.dict so it's OK to do this with out affecting
        #   parent scope.
        os.environ[TestDiscoveryViaEnvVar.VAR_NAME] = ""

        type_set = discover_via_env_var(TestDiscoveryViaEnvVar.VAR_NAME)
        assert len(type_set) == 0

    @mock.patch.dict(
        os.environ, {VAR_NAME: "tests.test_plugin_dir.module_of_stuff"}
    )
    def test_module_in_path(self) -> None:
        """
        Test that when a module path exist in the environment variable, it's
        searched for types.
        """
        assert TestDiscoveryViaEnvVar.VAR_NAME in os.environ
        type_set = discover_via_env_var(TestDiscoveryViaEnvVar.VAR_NAME)
        assert type_set == TYPES_IN_STUFF_MODULE

    @mock.patch.dict(os.environ, {
        VAR_NAME: OS_ENV_PATH_SEP.join([
            "tests.test_plugin_dir.module_of_stuff",
            "tests.test_plugin_dir.module_of_more_stuff",
        ])
    })
    def test_multiple_in_path(self) -> None:
        """
        Test that multiple modules resolve in environment variable.
        """
        test_set = discover_via_env_var(TestDiscoveryViaEnvVar.VAR_NAME)
        assert test_set == (TYPES_IN_STUFF_MODULE | TYPES_IN_MORE_STUFF_MODULE)

    @mock.patch.dict(
        os.environ, {VAR_NAME: "probably.not.a.valid.path"}
    )
    def test_invalid_in_path(self) -> None:
        """
        Test when there is an invalid module in the path.
        """
        with pytest.raises(ModuleNotFoundError):
            discover_via_env_var(TestDiscoveryViaEnvVar.VAR_NAME)

    @mock.patch.dict(os.environ, {
        VAR_NAME: OS_ENV_PATH_SEP.join([
            "tests.test_plugin_dir.module_of_stuff",
            "tests.test_plugin_dir.module_of_more_stuff",
            # The exception causing module.
            "tests.test_plugin_dir.module_with_exception"
        ])
    })
    def test_module_exception(self) -> None:
        """
        Test when there is a module in the path that raises an exception.
        """
        with pytest.raises(RuntimeError, match=r"^Expected error on import$"):
            discover_via_env_var(TestDiscoveryViaEnvVar.VAR_NAME)


class TestDiscoveryViaEntrypointExtensions:
    """
    Unit tests for entry-point extension based discovery of types.
    """

    @mock.patch("smqtk_core.plugin.get_ns_entrypoints")
    def test_no_extensions_for_entrypoint(self, m_get_ep: mock.Mock) -> None:
        """
        Test that no types are returned when there are no extensions for the
        given test entry-point namespace.
        """
        # Mock an empty number of entrypoint returns.
        m_get_ep.return_value = ()
        type_set = discover_via_entrypoint_extensions('my_namespace')
        assert len(type_set) == 0

    @mock.patch("smqtk_core.plugin.get_ns_entrypoints")
    def test_valid_extension_for_ns(self, get_ep: mock.Mock) -> None:
        """
        Test that a module's types are successfully returned when there is an
        EntryPoint referring to that module (NOT attribute).
        """
        my_namespace = "my_namespace"
        get_ep.return_value = (
            metadata.EntryPoint(
                name="module_via_extension_one",
                value="tests.test_plugin_dir.module_of_stuff",
                group=my_namespace,
            ),
            metadata.EntryPoint(
                name="module_via_extension_two",
                value="tests.test_plugin_dir.module_of_more_stuff",
                group=my_namespace
            ),
        )
        type_set = discover_via_entrypoint_extensions(my_namespace)
        get_ep.assert_called_once_with(my_namespace)
        assert type_set == (TYPES_IN_STUFF_MODULE | TYPES_IN_MORE_STUFF_MODULE)

    @mock.patch("smqtk_core.plugin.get_ns_entrypoints")
    def test_invalid_ep_warning(self, m_get_ep: mock.Mock) -> None:
        """
        Test that a warning is emitted when an entry-point is specified but is
        NOT a module.
        """
        my_namespace = "my_namespace"
        # An entrypoint referring to an attribute specification. This should
        # cause this EP to be skipped.
        test_ep = metadata.EntryPoint(
            name="module_via_extension_bad",
            value="tests.test_plugin_dir.module_of_more_stuff:argparse.ArgumentParser",
            group=my_namespace,
        )
        # Mock the entrypoints getter to return our test scenario, assuming
        # it is called with a group selector (turning iterable).
        m_get_ep.return_value = (test_ep,)

        with pytest.raises(
            NotAModuleError,
            match=r"An entrypoint with key 'module_via_extension_bad' and "
                  r"value 'tests.test_plugin_dir.module_of_more_stuff:"
                  r"argparse.ArgumentParser' did not specify a module "
                  r"\(got an object of type `type` instead\): "
        ):
            discover_via_entrypoint_extensions("my_namespace")

    @mock.patch("smqtk_core.plugin.get_ns_entrypoints")
    def test_module_with_error(self, m_get_ep: mock.Mock) -> None:
        """
        Test when there is an entry-point specifying a module with an error.
        """
        my_namespace = "my_namespace"
        m_get_ep.return_value = (
            metadata.EntryPoint(
                name="module_via_extension_one",
                value="tests.test_plugin_dir.module_of_stuff",
                group=my_namespace,
            ),
            metadata.EntryPoint(
                name="module_via_extension_two",
                value="tests.test_plugin_dir.module_of_more_stuff",
                group=my_namespace,
            ),
            # Error causing entrypoint
            metadata.EntryPoint(
                name="module_via_extension_two",
                value="tests.test_plugin_dir.module_with_exception",
                group=my_namespace,
            ),
        )
        with pytest.raises(RuntimeError, match=r"^Expected error on import$"):
            discover_via_entrypoint_extensions("my_namespace")


class TestDiscoverViaSubclasses:
    """
    Unit tests for local sub-class definition based discovery of types.
    """

    def test_no_subclasses(self) -> None:
        """
        Test when a type has no locally defined sub-classes.
        """
        class SomeClass(Pluggable):
            ...

        type_set = discover_via_subclasses(SomeClass)
        assert len(type_set) == 0

    def test_has_local_subclasses(self) -> None:
        """
        Test that a locally defines class structure is expectedly discoverable.
        """
        # Hypothetical parent class. Should not be included.
        class ParentClass(abc.ABC):
            @abc.abstractmethod
            def some_method(self) -> None: ...

        # Test finding descendents of this.
        # noinspection PyAbstractClass
        class SomeClass(ParentClass):
            ...

        # A sibling is not a descendent. Should not be included.
        # noinspection PyAbstractClass, PyUnusedLocal
        class SiblingClass(ParentClass):
            ...

        # Immediate subclasses of the parent type should be discoverable
        class DerivedClassOne(SomeClass):
            def some_method(self) -> None: ...

        class DerivedClassTwo(SomeClass):
            def some_method(self) -> None: ...

        # Nested Children classes should also be discovered.
        class DerivedClassTwoSubOne(DerivedClassTwo):
            def some_method(self) -> None: ...

        class DerivedClassTwoSubOneMore(DerivedClassTwoSubOne):
            def some_method(self) -> None: ...

        type_set = discover_via_subclasses(SomeClass)
        assert type_set == {
            DerivedClassOne,
            DerivedClassTwo,
            DerivedClassTwoSubOne,
            DerivedClassTwoSubOneMore
        }


class TestFilterPluginTypes:
    """
    Unit tests for the `filter_plugin_types` function.

    The meat of the functionality in this function is based on
    `is_valid_plugin`, so those unit tests above are where the bulk of the
    validity unit tests live.

    The only novel behavior of this function is the looping and unique
    aggregation of types deemed valid.
    """

    def test_no_candidates(self) -> None:
        """
        Test that nothing is returned when an empty list is provided.
        """
        type_set = filter_plugin_types(module_of_stuff.ClassDefinition, [])
        assert len(type_set) == 0

    def test_no_subclasses(self) -> None:
        """
        Test that an empty list is returned when the given candidates does not
        include any valid implementations of the given interface class.
        """
        type_set = filter_plugin_types(module_of_stuff.ClassDefinition,
                                       [int, str, type])
        assert len(type_set) == 0

    def test_includes_subclasses(self) -> None:
        """
        Test filter function where there are some valid implementation classes.
        """
        type_set = filter_plugin_types(
            module_of_stuff.ClassDefinition,
            [int, str, module_of_stuff.Derived, type]
        )
        assert type_set == {
            module_of_stuff.Derived
        }

    def test_duplicate_types(self) -> None:
        """
        Test that if there are duplicate types in the candidate the return is
        as would be expected (i.e. they're not skipped or something, I don't
        know). This is modeling when a type is picked up from multiple sources.
        """
        type_set = filter_plugin_types(
            module_of_stuff.ClassDefinition,
            [int, str, module_of_stuff.Derived, type, module_of_stuff.Derived]
        )
        assert type_set == {
            module_of_stuff.Derived
        }


class TestPluggable:
    """
    Unit and behavior tests for the Pluggable mixin abstract interface.
    """

    @mock.patch("smqtk_core.plugin.discover_via_subclasses")
    @mock.patch("smqtk_core.plugin.discover_via_entrypoint_extensions")
    @mock.patch("smqtk_core.plugin.discover_via_env_var")
    def test_no_plugins(
        self,
        m_d_env: mock.Mock,
        m_d_ent: mock.Mock,
        m_d_sub: mock.Mock
    ) -> None:
        """
        Simulate all sources returning no types for filtering. Returned impls
        set should of course then be empty.
        """
        m_d_env.return_value = set()
        m_d_ent.return_value = set()
        m_d_sub.return_value = set()

        class SomeInterface(Pluggable):
            ...

        impls = SomeInterface.get_impls()
        assert len(impls) == 0

    def test_usable_cls_method(self) -> None:
        """
        Test that `is_usable` returns the appropriate value by default and that
        an override of course returns the expected value.
        The implementations classes should still be constructable regardless
        of this method's return.
        """
        class SomeInterface(Pluggable):
            ...

        class IsUsable(SomeInterface):
            # Default should be "usable"
            ...

        class NotUsable(SomeInterface):
            @classmethod
            def is_usable(cls) -> bool:
                return False

        assert IsUsable.is_usable() is True
        assert NotUsable.is_usable() is False

        # These should both still succeed in this simple case.
        IsUsable()
        NotUsable()
