SMQTK-Core Pending Release Notes
================================


Updates / New Features
----------------------

Misc.

* Now standardize to using `Poetry`_ for environment/build/publish management.

  * Collapsed pytest configuration into the :file:`pyproject.toml` file.

  * Updated release process documentation to reflect the use of Poetry.

* Add explicit ReadTheDocs configuration file :file:`.readthedocs.yaml`.


Fixes
-----

CI

* Update CI configurations to use `Poetry`_.

Docs

* Fix incorrect filepath relative to this repository in the release process
  documentation.

* Fix for use with poetry where appropriate.


.. _Poetry: https://python-poetry.org/
