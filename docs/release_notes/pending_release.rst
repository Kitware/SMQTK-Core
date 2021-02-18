SMQTK-Core Pending Release Notes
================================


Updates / New Features
----------------------

CI

* Updated gitlab CI rules to trigger the test jobs during merge requests, tag
  builds and branch pipelines when the branch in question is the default branch
  (i.e. master).

* Added python 3.9 to the gitlab matrix of versions tested. Added 3.9 to the
  `setup.py` metadata.

* Updated requirements versions to the latest for each package.


Fixes
-----

Misc.

* Fixed `MANIFEST.in.in` file to not include a no-longer-present file and to
  include all `requirements/*.txt` files.
