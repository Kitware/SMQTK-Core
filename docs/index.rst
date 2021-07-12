Social Media Query ToolKit -- Core
==================================

| `Source Code (GitHub) <https://github.com/kitware/smqtk-core>`_
| `ReadTheDocs Documentation <https://smqtk-core.readthedocs.io>`_

This pure-python package provides a bedrock of interfaces and utilities to
supercharge abstract interfaces with the ability to find their own
implementations, as well as to be able to factory construct arbitrary
implementations of an abstract interface with an input JSON-compliant
configuration dictionary.
These features may be utilized separately but are designed to work
synergistically.

.. code-block:: python

   from smqtk_core import Pluggable, Configurable
   from smqtk_core.configuration import from_config_dict


   # An abstract interface.
   class MyNewInterface (Pluggable, Configurable):
       @abc.abstractmethod
       def work(self) -> None:
           "Abstract method for implementations to define."


   if __name__ == "__main__"
       # Discover currently available implementations of the defined interface.
       implementation_set: Set[Type[MyNewInterface]] = MyNewInterface.get_impls()

       # With a configuration from some source (see the smqtk_core.configuration module)
       # we can instantiate a concrete instance for use.
       from my_app import get_config_from_somewhere
       config_json: Dict[str, Any] = get_config_from_somewhere()
       instance: MyNewInterface = from_config_dict(config_json, implementation_set)

       # Use the new instance!
       instance.work()

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   plugins_configuration
   releasing
   faq


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
