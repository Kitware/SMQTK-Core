SMQTK Review Process
********************

The purpose of this document is to define the process for reviewing and integrating branches into SMQTK.
This encompasses all `SMQTK repositories`_.

See ``CONTRIBUTING.md`` for guidelines on contributing to SMQTK.

See `release process`_ for guidelines on the release process for SMQTK.

.. _`release process`: release_process.html

.. _`SMQTK repositories`: https://github.com/kitware/?q=smqtk-&type=&language=&sort=

.. contents:: The review process consists of the following steps:

Pull Request
============

A PR is initiated by a user intending to integrate a branch from their forked repository.
Before the branch is integrated into the SMQTK master branch, it must first go through a series of checks and a review to ensure that the branch is consistent with the rest of the repository and doesn't contain any issues.

Workflow Status
---------------

The submitter must set the status of their PR.

Draft
^^^^^
Indicates that the submitter does not think that the PR is in a mergeable state. Once they complete their work and think that the PR is mergeable, they may set the status to ``Open``.

Open
^^^^
Indicates that a PR is ready for review.
This indicates that the submitter of the PR thinks that the branch is ready to be merged.
If the submitter is still working on the PR and simply wants feedback, they must request it and leave their branch marked as a ``Draft``.

Closed
^^^^^^
Indicates that the PR is resolved or discarded.


Continuous Integration
======================

kwrobot
-------
Runs basic checks on the commits submitted in a PR.
Should kwrobot find any issues with the build, the diagnostics are written out prompting the submitter to correct the reported issues.
If there are no issues, kwrobot simply reports a successful build.
The branch must pass this check before it can be merged.

Some reports such as whitespace issues will need to be corrected by rewriting the commit

LGTM Analysis
-------------
Runs a more advanced code analysis tool over the branch that can address issues that the submitter might not have noticed.
Should LGTM find an issue, it will write a comment on the PR.
The comment should be addressed by the submitter before continuing to submit for review.

lint
----
Runs flake8 to quality check the code style. You can run this check manually in your local repository with ``poetry run flake8``.

MyPy
----
Performs static type analysis. You can run this check manually in your local repository with ``poetry run mypy``.

Unittests
---------
Runs the unittests created under ``tests/``. You can run this check manually  in your local repository with ``poetry run pytest``.

Human Review
============

Once the automatic checks are either resolved or addressed, the submitted PR will need to go through a human review.
Reviewers should add comments to provide feedback and raise potential issues.
Should the PR pass their review, the reviewer should then indicate that it has their approval using the Github review interface to flag the PR as ``Approved``.

A review can still be requested before the checks are resolved, but the PR must be marked as a ``Draft``.
Once the PR is in a mergeable state, it will need to undergo a final review to ensure that there are no outstanding issues.

If a PR is not a draft and has an approving review, it can be merged at any time.

Resolving a Branch
==================

Merge
-----

Once a PR receives an approving review and is no longer marked as a ``Draft``, the repository maintainers can merge, closing the pull request.
It is recommended that the submitter delete their branch after the PR is merged.

Close
-----

If it is decided that the PR will not be integrated into SMQTK, then it can be closed through Github.
