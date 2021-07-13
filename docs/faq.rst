Frequently Asked Questions
==========================

What is SMQTK?
^^^^^^^^^^^^^^
SMQTK is an open-source light-weight framework for developing interfaces that have built-in implementation discovery and factory construction from configuration.

Why would I use SMQTK over KWIVER?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
You should use SMQTK if you want to define your own python algorithm implementations and don't want to develop in C++.
However, if the algorithm implementations that you want to use are already defined in KWIVER, then KWIVER would be the better option.\
For more info, see the ``README.md``

I've used SMQTK before, but what are these broken out packages?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
In 2021, ``SMQTK v0.14.0`` was broken out from one monolithic library into several distinct libraries labeled as ``SMQTK-Core``, ``SMQTK-Classifier``, ``SMQTK-Image-IO``, and more.
The decision was part of a new effort to reduce technical debt and isolate functionality to preserve the light-weight design.

Can I contribute to SMQTK?
^^^^^^^^^^^^^^^^^^^^^^^^^^
Of course!
To add in your own implementation see ``CONTRIBUTING.md``.
Additionally you can contribute by helping review any outstanding branches in any one of the SMQTK repos.
For guidelines on reviewing please see `review_process`_

.. _`review_process`: review_process.html

What does SMQTK encompass?
^^^^^^^^^^^^^^^^^^^^^^^^^^
SMQTK is currently composed of 7 different libraries, all of which are pip installable.
``SMQTK-Core`` provides the underlying tooling and is utilized by the other 6 packages which provide more complex functionality and pluggable implementations.
The following are all the packages associated with SMQTK:

* `SMQTK-Core`_ provides the basic tools for developing interfaces.

* `SMQTK-Dataprovider`_ provides data structure abstractions.

* `SMQTK-Image-IO`_ provides interfaces and implementations around image input/output.

* `SMQTK-Descriptors`_ provides algorithms and data structures around computing descriptor vectors.

* `SMQTK-Classifier`_ provides interfaces and implementations around classification.

* `SMQTK-Indexing`_ provides interfaces and implementations around the k-nearest-neighbor algorithm.

* `SMQTK-Relevancy`_ provides interfaces and implementations around providing search relevancy estimation.

.. _`SMQTK-Core`: https://github.com/Kitware/SMQTK-Core
.. _`SMQTK-Dataprovider`: https://github.com/Kitware/SMQTK-Dataprovider
.. _`SMQTK-Image-IO`: https://github.com/Kitware/SMQTK-Image-IO
.. _`SMQTK-Descriptors`: https://github.com/Kitware/SMQTK-Descriptors
.. _`SMQTK-Classifier`: https://github.com/Kitware/SMQTK-Classifier
.. _`SMQTK-Indexing`: https://github.com/Kitware/SMQTK-Indexing
.. _`SMQTK-Relevancy`: https://github.com/Kitware/SMQTK-Relevancy
