SMQTK-Core Pending Release Notes
================================


Updates / New Features
----------------------

Interfaces

* Added a new :class:`~.smqtk_core.Plugfigurable` class that provides a
  convenient handle to inherit from both :class:`.Pluggable` and
  :class:`.Configurable` at the same time.

CI

* Updated gitlab CI rules to trigger the test jobs during merge requests, tag
  builds and branch pipelines when the branch in question is the default branch
  (i.e. master).

* Added python 3.9 to the gitlab matrix of versions tested. Added 3.9 to the
  `setup.py` metadata.

* Updated requirements versions to the latest for each package.


Fixes
-----

Docs

* Minor fixes to the `sphinx_server.py` helper tool: Removed a watch to a
  directory that does not exist.

Misc.

* Fixed `MANIFEST.in.in` file to not include a no-longer-present file and to
  include all `requirements/*.txt` files.

* Removed unnecessary `.dockerignore` file.
