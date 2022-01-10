# Contributing to SMQTK-Core

Here we describe at a high level how to contribute to SMQTK-Core.
See the [SMQTK-Core README] file for additional information.

**Table of Contents**
* [Topic Branches and Pull Requests](#topic-branches-and-pull-requests)
  * [Overview: Creating a Pull Request](#overview-creating-a-pull-request)
  * [Integration Branches](#integration-branches)
  * [Branch Naming](#branch-naming)
  * [Commits](#commits)
  * [Testing](#testing)
  * [Release Notes](#release-notes)
    * [Release Note Contribution Exception](#release-note-contribution-exception)
  * [Continuous Integration](#continuous-integration)
  * [Code Reviews](#code-reviews)
* [Coding Style](#coding-style)

## Topic Branches and Pull Requests
We use the term "topic branch" to describe the branch, based off of an
[integration branch], that introduces features and fixes to the code-base with
the intention to be merged back into the [integration branch].

### Overview: Creating a Pull Request

1. The official SMQTK-Core source is maintained on GitHub.

2. Fork SMQTK-Core into your user's namespace and clone this repository
    on your system.

3. Create a topic branch off of the appropriate
   [integration branch], edit files and create commits:

        $ git checkout master  # or appropriate integration branch
        $ git checkout -b <branch-name>
        $ <edit things>
        $ git add <file1> <file2> ...
        $ git commit

4. Add summary of changes in the [pending release notes] file
   ([see below](#release-notes)).

5. Push topic branch with commits to your fork in GitHub:

        $ git push origin HEAD -u

6. Visit the Kitware SMQTK-Core GitHub, browse to the "Pull requests" tab
   and click on the "New pull request" button in the upper-right.
   Click on the "compare across forks" link, browse to your fork and browse to
   the topic branch to submit for the pull request.
   Finally, click the "Create pull request" button to create the request.

### Integration Branches
There a two primary integration branches named ``release`` and ``master``.
Generally, the ``release`` branch contains that last versioned stable release
plus a few patches in preparation for the next patch release.
The ``master`` branch contains new features and API changes since the last
release and is preparing for the next major or minor versioned release.
There may also be additional ``release-v<MAJOR>.<MINOR>`` branches that may be
used as a branching off point to create patch branches for releases older than
the most current release.

Some Pull Request ("PR") branch basing guidance:
* If your PR is a bug fix that applies to the last release, please branch off
  of ``release`` and submit your PR to the ``release`` branch.
* If your PR is a bug fix to a previous patch release of a major or minor
  version, please branch off of the latest patch release of that major or minor
  version.
* If your PR is a new feature or bug fix that applies to ``master`` but not to
  ``release`` then submit your PR to the``master`` branch.

Any PR accepted in ``release`` is implicitly accepted into ``master``, but not
vice versa.

### Branch Naming
Topic branches should be named starting with a ``dev/`` prefix to distinguish
them from integration branches like ``master`` and ``release``.

### Commits
While not a strict requirement, it is beneficial for commits to record a set of
separate, logical changes.
Ideally, each commit should be "logically complete", have correct code style
and passing unit-tests (this is partly enforced by our workflow tools, and such
enforcement may be expanded in the future).

Topic branches will not be merged if they contain "WIP" or "fixup" commits as
these only serve to clutter the history, make it harder to understand what
has changed, and make it harder to revert changes when necessary.
The judicious use of amends, `git commit --fixup=` (followed by an appropriate
`git rebase -i --autosquash ...`) and rebasing is encouraged.

Additionally, commits should follow the accepted conventions for git commit
messages.  In short:

- Use proper spelling and grammar; avoid "twitter speak".
- Use complete sentences (including the first line) and appropriate
  capitalization.  Use imperative mood.
- Try to limit the subject line to 50 characters.  *Don't* end with a period.
- Limit body lines (when necessary; occasionally just a subject is enough) to
  72 characters (unless this is impossible e.g. due to a long URL).

For further reading, see:

- https://chris.beams.io/posts/git-commit/
- https://www.freecodecamp.org/news/writing-good-commit-messages-a-practical-guide/
- https://medium.com/@steveamaza/how-to-write-a-proper-git-commit-message-e028865e5791

### Testing
Generally, all new code should come with tests.
The goal is sustained 80% coverage and higher.
Test files must have 100% coverage of themselves.
Tests should generally be grouped into a file that is parallel in location
under the `tests` directory to the file containing the code being tested.
For example, if new code was added to the file `smqtk_core/utils/foo.py`, tests
for that code should be added to `tests/utils/test_foo.py`.

The `pytest` package is utilized as the test runner.
See `pytest` documentation for further best-practices in writing and formatting
tests.

### Release Notes
When making a topic branch, included in its commits should be additions to the
[pending release notes] file.
These additions should be short, descriptive summaries of the updates,
features or fixes that have been added in the form of bullet points under
applicable sections.
There are broad sections for "Updates" (features or enhancements) and "Fixes"
(typos, bug fixes, etc.).
Most changes based on a ``release`` branch go under "Fixes", and most changes
based on the ``master`` branch go under "Updates".

A topic branch is generally required to provide at least one update to this
file for merger approval.

#### Release Note Contribution Exception
When a new contribution is fixing a bug or minor issue with something that has
an existing release note, it may be the case that no additional release notes
are needed since they would add redundancy to the document.

For example, if the PR is to fix a bug on the master branch that was introduced
since the last release, and the fix does not impact how the feature is
summarized in the release notes, then this should **not** be documented in the
"Fixes" section of the release notes because the bug itself was never released.
In such a case, the release-notes CI check on that follow-on contribution may
be ignored by the reviewers of the contribution.

Generally, a reviewer will assume that a release note is required unless the
contributor makes a case that the check should be ignored.
This will be considered by reviewers on a case-by-case basis.

### Continuous Integration
SMQTK-Core uses GitHub for code review and GitHub Actions for continuous
testing as new pull requests are made.
Most, but not all, CI checks are required to pass before a PR can be merged.
It is generally recommended that *all* checks pass, but there may be exception
cases for non-required CI checks.

See the [review process documentation] for more details on the CI checks
utilized.

### Code Reviews
Pull requests are reviewed by one or more of the core SMQTK-Core maintainers
using the GitHub tools for discussions.
Maintainers should not merge a PR until it conforms to the requirements
described here (e.g. coding style, release notes, etc.) and it is confirmed
that the code has sufficient unit tests and does not break any existing unit
tests.

See the [review process documentation] for more details on the code review
process.

## Coding Style
When developing SMQTK-Core, please keep to the prevailing style of the code
and follow the python-general PEP8 style.
Contention with any particular style decision will fall back onto [black]'s
decision (don't make us add [black] as a required CI check).


[black]: https://github.com/psf/black
[integration branch]: #integration-branches
[pending release notes]: docs/release_notes/pending_release.rst
[review process documentation]: docs/review_process.rst
[SMQTK-Core README]: README.md

---

Parts of this file are adapted from the [KWIVER Contributing file](
https://github.com/Kitware/kwiver/blob/master/CONTRIBUTING.rst).
