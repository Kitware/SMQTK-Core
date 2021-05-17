Pending Release Notes
=====================


Updates / New Features
----------------------

Dependencies

* Remove dependency on ``setuptool``'s ``pkg_resources`` module.
  Taking the stance of bullet #5 in from `Python's Packaging User-guide`_ with
  regards to getting this package's version.
  The "needs to be installed" requirement from before is maintained.

* Added dependency on the ``importlib-metadata`` backport package for
  installations in environments that use python version less-than 3.8.

* Added ``ipython`` (and appropriately supporting version of ``jedi``) as
  development dependencies.
  Minimum versioning is set to support python 3.6 (current versions follow
  `NEP 29`_ and thus require python 3.7+).

Documentation

* Clarified plugin implementation entrypoint example to include setuptools
  ``setuptools.setup()`` function and ``setup.cfg`` file.

* Revisions from proof-reading.

Plugins

* Entry-point discovery functionality now uses ``importlib_metadata`` /
  ``importlib.metadata`` as appropriate for the version of python being used.

Testing

* Added terminal-output coverage report in the standard pytest config in the
  ``pyproject.toml`` file.


Fixes
-----


.. _Python's Packaging User-guide: https://packaging.python.org/guides/single-sourcing-package-version/
.. _NEP 29: https://packaging.python.org/guides/single-sourcing-package-version/
