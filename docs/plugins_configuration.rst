Plugins and Configuration
-------------------------
The general concept of `abstract interfaces`__ allows users to create
functionality in terms of the interface, separating the concerns of usage and
implementation.
This tooling is intended to enhance that concept by providing a
straightforward way to expose and discover implementations of an interface,
as well as factory functionality to create instances of an implementation from
a JSON-compliant configuration structure.
We provide two mixin classes and a number of utility functions to achieve this.
While the two mixin classes function independently and can be utilized on their
own, they have been designed such that their combination is symbiotic.

.. __: https://en.wikipedia.org/wiki/Abstract_type
.. _P&C-PluggableMixin:

The :class:`~smqtk_core.plugin.Pluggable` Mixin
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
**Motivation:**
We want to be able to define interfaces to generic concepts and structures
that higher-level functionality can be defined around without strictly catering
themselves to any particular implementation.
We additionally want to allow freedom in implementation variety without much
adding to the implementation burden.

In SMQTK-Core, this is addressed via the :class:`~smqtk_core.plugin.Pluggable`
abstract mixin class:

.. code-block:: python

   import abc
   from smqtk_core.plugin import Pluggable

   class MyInterface(Pluggable):
       @abc.abstractmethod
       def my_behavior(self, x: str) -> int:
           """My fancy behavior."""

   class NumLetters(MyInterface):
       def my_behavior(self, x: str) -> int:
           return len(x)

   class IntCast(MyInterface):
       def my_behavior(self, x: str) -> int:
           return int(x)

   if __name__ == "__main__":
       # Discover currently available implementations and print out their names
       impl_types = MyInterface.get_impls()
       print("MyInterface implementations:")
       for t in impl_types:
           print(f"- {t.__name__}")

Running the above in a ``.py`` file would then output::

    MyInterface implementations:
    - NumLetters
    - IntCast

This is of course a naive example where implementations are defined
right next to the interface.
This is not a requirement.
Implementations may be spread out across other sub-modules within a package, or
even in other packages.
In the below section, `Plugin Discovery Methods`_, and in the example
`Creating an Interface and Exposing Implementations`_, we will show how to
expose implementations of a plugin-enabled interface.

.. _P&C-Pluggable-InterfaceVsImplementation:

Interfaces vs. Implementations
""""""""""""""""""""""""""""""
Classes that inherit from the :class:`~smqtk_core.plugin.Pluggable`
mixin are considered either plugin implementations, or further pluggable
interfaces, depending on whether they fully implement
abstract methods or not, respectively.


Plugin Discovery Methods
""""""""""""""""""""""""
SMQTK-Core's plugin discovery via the
:meth:`~smqtk_core.plugin.Pluggable.get_impls` method currently allows for
finding a plugin implementations in 3 ways:

* sub-classes of an interface type defined in the current runtime.

* within python modules listed in the environment variable specified by
  ``YourInterface.PLUGIN_ENV_VAR``. (default SMQTK-Core environment variable
  name is ``SMQTK_PLUGIN_PATH``, which is defined in
  :attr:`Pluggable.PLUGIN_ENV_VAR`).

* within python modules specified under the entry point extensions namespace
  defined by ``YourInterface.PLUGIN_NAMESPACE`` (default SMQTK-Core extension
  namespace is ``smqtk_plugins``, which is defined in
  :attr:`Pluggable.PLUGIN_NAMESPACE`).

When exposing interface implementations, it is generally recommended to use a
package's entry point extensions (3rd bullet above).


The :class:`~smqtk_core.configuration.Configurable` Mixin
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
**Motivation:**
We want generic helpers to enable serializable configuration for classes while
minimally impacting standard class development.

SMQTK-Core provides the :class:`~smqtk_core.configuration.Configurable` mixin
class as well as other helper utility functions in
:mod:`smqtk_core.configuration` for generating class instances from
configurations.
These use python's :mod:`inspect` module to determine constructor
parameterization and default configurations.

Currently this module uses the JSON-serializable format as the basis for input
and output configuration dictionaries as a means of defining a relatively
simple playing field for communication.
Serialization and deserialization is detached from these configuration
utilities so tools may make their own decisions there.
Python dictionaries are used as a medium in between serialization and
configuration input/output.

Classes that inherit from :class:`~smqtk_core.configuration.Configurable` *do*
need to at a minimum implement the
:meth:`~smqtk_core.configuration.Configurable.get_config` instance method.
This is due to currently lacking the ability to introspect the connection
between constructor parameters and how those values are retained in the class.
See this method's doc-string for more details.


The Convenient Combination: :class:`~smqtk_core.Plugfigurable`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
It will likely be desirable to utilize both the :class:`.Pluggable` and
:class:`.Configurable` mixins when constructing your own new interfaces.
To facilitate this, and to reduce excessive typing, we provide the
:class:`.Plugfigurable` helper class.
This class does not add or change any functionality.
It is merely a convenience to indicate the multiply inherit from both mixin
types.
Also regarding multiple in inheritance, either :class:`.Pluggable' nor
:class:`.Configurable` define a `__init__` method, so


Examples
^^^^^^^^

Creating an Interface and Exposing Implementations
""""""""""""""""""""""""""""""""""""""""""""""""""
In this example, we will show:
  * A simple interface definition that inherits from both :class:`.Pluggable`
    and :class:`.Configurable` via the convenient :class:`.Plugfigurable`
    class.
  * A sample implementation that is defined in a different module.
  * The subsequent exposure of that implementation via a python package's entry
    point extensions.

Let's start with the example interface definition which, let's say, is defined
in the :file:`MyPackage.interface` module of our hypothetical :mod:`MyPackage`
package:

.. code-block:: python

   # File: MyPackage/interface.py
   import abc
   from smqtk_core import Plugfigurable

   class MyInterface(Plugfigurable):
       """
       A new interface that transitively inherits from Pluggable and Configurable.
       """

       @abc.abstractmethod
       def my_behavior(self, x: str) -> int:
           """My fancy behavior."""

Then, in another package module, :mod:`MyPackage.implementation`, let's say we
define the following implementation. This implementation will need to define
all parent class abstract methods in order for the class to satisfy the
definition of an "implementation" (see
:ref:`P&C-Pluggable-InterfaceVsImplementation`).

.. code-block:: python

   # File: MyPackage/implementation.py
   from MyPackage.interface import MyInterface
   from typing import Any, Dict

   class MyImplementation(MyInterface):

       def __init__(self, paramA: int = 1, paramB: int = 2):
           """Implementation constructor."""
           self.a = paramA
           self.b = paramB

       # Abstract method from the Configurable mixin.
       def get_config(self) -> Dict[str, Any]:
           # As per Configurable documentation, this should return the same
           # non-self keys as the constructor.
           return {
               "paramA": self.a,
               "paramB": self.b,
           }

       # Abstract method from MyInterface
       def my_behavior(self, x: str) -> int:
           """My fancy implementation."""
           ...

Lastly, our implementation should be exposed via our package's entrypoint
metadata, using the "smqtk_plugins" namespace. This namespace value is derived
from the base :class:`~smqtk_core.plugin.Pluggable` mixin's
``PLUGIN_NAMESPACE`` class property.
Entry point metadata may be specified for a package either via the
:func:`setuptools.setup` function, the `setup.cfg` file, or, when using poetry,
a ``[tool.poetry.plugins."..."]`` section in the :file:`pyproject.toml` file.
This is illustrated in the following:

    a) :func:`setuptools.setup` function

       .. code-block:: python

          from setuptools import setup
          setup(
              entry_points={
                  "smqtk_plugins": [
                      "unique_key = MyPackage.implementation",
                      ...
                  ]
              }
          )

    b) The :file:`setup.cfg` file

       .. code-block:: cfg

          [options.entry_points]
          smqtk_plugins =
              unique_key = MyPackage.implementation
              ...

    c) with Poetry in the :file:`pyproject.toml` file

       .. code-block:: toml

          [tool.poetry.plugins."smqtk_plugins"]
          "my_plugins" = "MyPackage.implementation"
          ...

Now, this implementation will show up as an available implementation of the
interface class:

.. code-block:: python

   >>> from MyPackage.interface import MyInterface
   >>> MyInterface.get_impls()
   {<class 'MyPackage.implementation.MyImplementation'>}

The :class:`MyImplementation` class above should also be all set for
configuration because it defines the one required abstract method
:meth:`~smqtk_core.configuration.Configurable.get_config` and because it's
constructor is only anticipating JSON-compliant data-types.
If more complicated types are desired by the constructor, that is completely
OK!
In such cases, additional methods would need to be overridden as defined in the
:mod:`smqtk_core.configuration` module.

Supporting configuration with more complicated constructors
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
In the above example, only very simple, already-JSON-compliant data types were
utilized in the constructor.
This not intended to imply that there is a restriction in constructor
specification.
Instead, the :class:`.Configurable` mixin provides overridable methods to
insert conversion to and from JSON-compliant dictionaries, to provide a class
"default" configuration as well as for factory-generation of a class instance
from an input configuration.

Instead of the above implementation, let us consider a slightly more complex
implementation of ``MyInterface`` defined above.
In this new implementation we show the implementation of two additional class
methods from the :class:`.Configurable` mixin:
:meth:`.Configurable.get_default_config` and  :meth:`.Configurable.from_config`.
These allow us to customize the how we maintain JSON-compliance.

.. code-block:: python

    from MyPackage.interface import MyInterface
    from typing import Any, Dict, Type, TypeVar
    from datetime import datetime


    C = TypeVar("C", bound="DateContainer")


    class DateContainer (MyInterface):
        """
        This example implementation takes in datetime instances as constructor
        parameters, one of which has a default.
        Both parameters in this example require a `datetime` instance value at
        construction time, but since `b_date` has a default value, it is not
        strictly required that an input configuration provide a value for the
        `b_date` parameter since there is a default to draw upon.
        """

        def __init__(
            self,
            a_date: datetime,
            b_date: datetime = datetime.utcfromtimestamp(0),
        ):
            self.a_date = a_date
            self.b_date = b_date

        # NEW FROM PREVIOUS EXAMPLE
        # Abstract method from the Configurable mixin.
        @classmethod
        def get_default_config(cls) -> Dict[str, Any]:
            # Utilize the mixin-class implementation to introspect our
            # constructor and make a parameter-to-value dictionary.
            cfg = super().get_default_config()
            # We are ourself, so we know that cfg['a_date'] has a default value
            # and it will be a datetime instance.
            cfg['b_date'] = datetime_to_str(cfg['b_date'])
            # We know that `a_date` is not given a default, so its "default"
            # value of None, which is JSON-compliant, is left alone.
            return cfg

        # NEW FROM PREVIOUS EXAMPLE
        # Abstract method from the Configurable mixin.
        @classmethod
        def from_config(
            cls: Type[C],
            config_dict: Dict,
            merge_default: bool = True
        ) -> C:
            # Following the example found in the Configurable.from_config
            # doc-string.
            config_dict = dict(config_dict)
            # Convert required input data into the constructor-expected types.
            # This implementation will expectedly error if the expected input
            # is missing.
            config_dict['a_date'] = str_to_datetime(config_dict['a_date'])
            # b_date might not be there because there's a default that can fill
            # in.
            b_date = config_dict.get('b_date', None)
            if b_date is not None:
              config_dict['b_date'] = str_to_datetime(b_date)
            return super().from_config(config_dict, merge_default=merge_default)

        # Abstract method from the Configurable mixin.
        def get_config(self) -> Dict[str, Any]:
            # This now matches the same complex-to-JSON conversion as the
            # `get_default_config`. We show the use of a helper function to
            # reduce code duplication.
            return {
                "a_date": datetime_to_str(self.date),
            }

        # Abstract method from MyInterface
        def my_behavior(self, x: str) -> int:
            """My fancy implementation."""
            ...


    def datetime_to_str(dt: datetime) -> str:
        """ Local helper function for config conversion from datetime. """
        # This conversion may be arbitrary to the level of detail that this
        # local implementation considers important. We choose to use strings
        # here as an example, but there's nothing special that requires that
        # other than JSON type compliance.
        return str(dt)


    def str_to_datetime(s: str) -> datetime:
        """ Local helper function for config conversion into datetime """
        # Reverse of above converter.
        if '.' in s:  # has decimal seconds
            return datetime.strptime(s, "%Y-%m-%d %H:%M:%S.%f")
        return datetime.strptime(s, "%Y-%m-%d %H:%M:%S")


The above then allows us to create instances of this instance with the JSON
config:

.. code-block:: python

    >>> inst = DateContainer.from_config({
    ...   "a_date": "2021-01-01 00:00:00.123123"
    ...   "b_date": "1970-01-01 00:00:01",
    ... })
    >>> str(inst.a_date)
    '2021-01-01 00:00:00.123123'
    >>> str(inst.b_date)
    '1970-01-01 00:00:01'

Or even just:

.. code-block:: python

    >>> inst = DateContainer.from_config({
    ...   "a_date": "2021-01-01 00:00:00.123123"
    ... })
    >>> str(inst.a_date)
    '2021-01-01 00:00:00.123123'
    >>> str(inst.b_date)
    '1970-01-01 00:00:00'

While such inline usage is less likely to be called so directly as opposed to
just calling the constructor, this form is useful when constructing directly
from a deserialized configuration:

.. code-block:: python

    >>> # Maybe received this from a web request!
    >>> from_file = '{"a_date": "2021-01-01 00:00:00.123123", "b_date": "1970-01-01 00:00:01"}'=
    >>> import json
    >>> inst = DateContainer.from_config(json.loads(from_file))
    >>> str(inst.a_date)
    '2021-01-01 00:00:00.123123'
    >>> str(inst.b_date)
    '1970-01-01 00:00:01'

Instances may also be "cloned" by creating a new instance from the current
configuration output from another instance using the
:meth:`.Configurable.get_config` instance method:

.. code-block:: python

    >>> # assume and `inst` from above
    >>> inst2 = DataContainer.from_config(inst.get_config())
    >>> assert inst.a_date == inst2.a_date
    >>> assert inst.b_date == inst2.b_date

This is again a little silly in the demonstration context because we know what
instance type and attributes are to construct a second one, however if the
concrete instance is not known at runtime, this may be an alternate means of
constructing a duplicate instance (at least "duplicate" in regards to
construction).


Multiple Implementation Choices
"""""""""""""""""""""""""""""""
One usage mode of :mod:`smqtk_core.configuration` configuration is when a
configuration slot may be comprised of one of multiple
:class:`.Configurable`-implementing choices.
Also found in the :mod:`smqtk_core.configuration` module are additional helper
functions for navigating this use-case:
  * :func:`.make_default_config`
  * :func:`.to_config_dict`
  * :func:`.from_config_dict`

These methods utilize JSON-compliant dictionaries to represent configurations
that follow the schema::

    {
        "type": "object",
        "properties": {
            "type": {"type": "string"},
        },
        "additionalProperties": {"type": "object"},
    }

Getting Defaults from a group of types
''''''''''''''''''''''''''''''''''''''
When programmatically creating a multiple-choice configuration
structure for output, the :func:`.make_default_config` function may be
convenient to use.
This takes in some :class:`~typing.Iterable` of
:class:`.Configurable`-inheriting types and returns a JSON-compliant
dictionary.
This may be useful, for example, when a higher-order tool wants to
programmatically generate a default configuration for itself for serialization
or for some other interface.

This function may be called with an independently generated :class:`.Iterable`
of inputs, however this also melds well with the:meth:`.Pluggable.get_impls`
class method.
For example, let us use the pluggable :class:`MyInterface` class defined above:

.. code-block:: python

    >>> from smqtk_core.configuration import make_default_config
    >>> cfg_dict = make_default_config(MyInterface.get_impls())
    >>> cfg_dict
    {
        "type": None,
        "__main__.MyImplementation": {
            "paramA": 1,
            "paramB": 2
        },
        "__main__.DateContainer": {
            "a_date": None,
            "b_date": "1970-01-01 00:00:00"
        }
    }

See the method documentation for additional details.

Factory constructing from configuration
'''''''''''''''''''''''''''''''''''''''
The opposite of above, the :func:`.from_config_dict` will take a configuration
multiple-choice dictionary structure and "hydrate" an instance of the
configured type with the configured parameters (if it's available, of course).
This function again takes an :class:`.Iterable` of
:class:`.Configurable`-inheriting types which again melds well with the
:class:`.Pluggable.get_impls` class method where applicable.

For example, if we take the "default" configuration output above, change the
``"type"`` value to refer to the "MyImplementation" type and pass it to this
function, we get a fully constructed instance:

.. code-block:: python

    >>> from smqtk_core.configuration import from_config_dict
    >>> # Let's modify the config away from default values.
    >>> cfg_dict['__main__.MyImplementation'] = {'paramA': 77, 'paramB': 444}
    >>> inst = from_config_dict(cfg_dict, MyInterface.get_impls())
    >>> assert inst.a == 77
    >>> assert inst.b == 444

See the method documentation for additional details.

Help with writing unit tests for Configurable-implementing types
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
When creating new implementations of things that includes
:class:`.Configurable` functionality it is often good to include tests that
make sure the expected configuration capabilities operate as they should.
We include a helper function to lower the cost of adding such a test:
:func:`.configuration_test_helper`.
This will exercise certain runtime-assumptions that are not strictly required
to define and construct :class:`.Configurable`-inheriting types.

For an example, let's assume we are writing a unit test for the above-defined
:class:`.MyImplementation` class:

.. code-block:: python

    >>> from smqtk_core.configuration import configuration_test_helper
    >>>
    >>> class TestMyImplementation:
    ...     def test_config(self):
    ...         inst = MyImplementation(paramA=77, paramB=444)
    ...         for i in configuration_test_helper(inst):
    ...             # Checking that yielded instance properties are as expected
    ...             assert i.a == 77
    ...             assert i.b == 444

See the method documentation for additional details.


Module References
^^^^^^^^^^^^^^^^^

:mod:`smqtk_core`
"""""""""""""""""
.. automodule:: smqtk_core
   :members:

:mod:`smqtk_core.plugin`
""""""""""""""""""""""""
.. automodule:: smqtk_core.plugin
   :members:

:mod:`smqtk_core.configuration`
"""""""""""""""""""""""""""""""
.. automodule:: smqtk_core.configuration
   :members:
