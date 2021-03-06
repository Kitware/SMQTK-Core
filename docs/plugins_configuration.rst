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
   from typing import Dict

   class MyImplementation(MyInterface):

       def __init__(self, paramA: int = 1, paramB: int = 2) -> None:
           """Implementation constructor."""
           ...

       # Abstract method from the Configurable mixin.
       def get_config(self) -> Dict:
           # As per Configurable documentation, this should return the same
           # non-self keys as the constructor.
           return {
               "paramA": ...,
               "paramB": ...,
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


Reference
^^^^^^^^^

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
