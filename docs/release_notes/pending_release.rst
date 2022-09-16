Pending Release Notes
=====================

Updates / New Features
----------------------

CI

* Reverted previous release automation due to unintended side-effects.
  Created a revised publish action to more simply publish the package to pypi,
  guarding against activating on fork of the repository.
  This workflow has been made to be reusable by other repositories' workflows.

* Modified CI unittests workflow to run for PRs targeting branches that match
  the `release*` glob.

* Added additional step in unittest workflow to install optional package
  requirements.

* Reduced CodeCov report submission by skipping this step on scheduled runs.

* Update code-cov action usage to use v3.

Contribution Guide

* Added instructions to update pending release when making a contribution.

Dependencies

* Updated minimum required python version to 3.7 to follow python end of life.

* Updated development abstract dep versions to "*" since we do not currently
  require any specific versions.

Documentation

* Updated release instructions to be clear on where to push created release
  branches. This now includes instructions related to a ``release`` branch.

* Expanded top-level contributing document with more details.

Plugin

* Added a suggestion to fix `NotAModuleError`.

* Removed __new__ override to prevent construction of "not usable"
  implementations. This feature has never been observed/utilized in the wild
  and it's removal simplifies tool interactions and use complexity.

Miscellaneous

* Removed CODE_OF_CONDUCT file. This is not something that we can enforce
  at this time so it will be removed.

* Added SMQTK-Descriptors to the ``README.md`` package list and graphic.

* Added script to help with updating versioning and updating changelog during
  the release process.

* Updated README to include reference to the SMQTK-IQR package.

* Periodic update of pinned dependency versions in lock file.

* Added missing assert failure message to configuration test helper.

* Added properties file for use with SonarQube and SonarCloud.

Fixes
-----
