Pending Release Notes
=====================

Updates / New Features
----------------------

CI

* Reverted previous release automation due to unintended side-effects.
  Created a revised publish action to more simply publish the package to pypi,
  guarding against activating on fork of the repository.
  This workflow has been made to be reusable by other repositories' workflows.

* Also run CI unittests for PRs targetting branches that match the `release*`
    glob.

* Added additional step in unittest workflow to install optional package
  requirements.

Contribution Guide

* Add instructions to update pending release when making a contribution.

Documentation

* Update release instructions to be clear on where to push created release
  branches. This now includes instructions related to a ``release`` branch.

* Expanded top-level contributing document with more details.

Plugin

* Add a suggestion to fix `NotAModuleError`.

Miscellaneous

* Removed CODE_OF_CONDUCT file. This is not something that we can enforce
  at this time so it will be removed.

* Add SMQTK-Descriptors to the ``README.md`` package list and graphic.

* Add script to help with updating versioning and updating changelog during
  the release process

* Updated README to include reference to the SMQTK-IQR package.

Fixes
-----

Dependency Versions

* Update the locked version of urllib3 to address a security vulnerability.
  Due to this being an implicit dependency, this change only affects those who
  create development environments from this repo using `poetry`.

* Update the developer dependency and locked version of ipython to address a
  security vulnerability.

* Removed `jedi = "^0.17.2"` requirement since recent `ipython = "^7.17.3"`
  update appropriately addresses the dependency.
