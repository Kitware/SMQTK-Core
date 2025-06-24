Pending Release Notes
=====================

Updates / New Features
----------------------

CI

* Synchronize workflow files with other smqtk repositories so they share their
  format and parameterization more similarly.

* Add configuration for codecov to required different coverage percentage for
  the package source vs. the tests.

* Added explicit provision of codecov repository token to github action.

* Add testing for py3.11 and py3.12.

* Update publish automation to make use of py3.8 and updates a check to ensure
  the git ref_name that triggered the workflow matches the package version to
  be published.

* Updated ``readthedocs.yml`` to using the ``poetry`` install command to
  install the package and its dependencies.

* Updated GitHub actions to use the latest versions of actions.

* Updated GitHub ``poetry`` install action to constrain to ``poetry<2.0``.

Fixes
-----
