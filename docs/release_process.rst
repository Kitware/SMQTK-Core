Steps of the SMQTK Release Process
==================================
Three types of releases are expected to occur:
- major
- minor
- patch

See the ``CONTRIBUTING.md`` file for information on how to contribute features
and patches.

The following process should apply when any release that changes the version
number occurs.

Create and merge version update branch
--------------------------------------

Patch Release
^^^^^^^^^^^^^
A patch release should only contain fixes for bugs or issues with an existing
release.
No new features or functionality should be introduced in a patch release.
As such, patch releases should only ever be based on an existing release point.

1. Create a new branch off of the appropriate ``vX.Y.Z`` tag named something
   like ``release-patch-{NEW_VERSION}``, where ``NEW_VERSION`` is an increase
   in the ``Z`` version component.

   a. Use ``poetry version patch`` to increase the patch value appropriately in
      the :file:`pyproject.toml` file. This is important because the automated
      release process will try to publish the version listed in this file and it
      will error out if the version it tries to upload to PYPI already exists.

   b. Rename the ``docs/release_notes/pending_patch.rst`` file to
      ``docs/release_notes/v{VERSION}.rst``, matching the new version value.
      Add a descriptive paragraph under the title section summarizing this
      release. During the automated process, this new, versioned file will referenced
      to create the header of the release on Github.

   c. Add a reference to the new release notes RST file in
      ``docs/release_notes.rst``.

   d. In a separate commit, add back a blank pending release notes file stub.
      See `Stub Pending Notes File`_.

2. Tag branch from the command line (see `Tag new version`_ below ). After the
   tag is pushed, a CI check and build will automatically run. Should everything
   pass without issue, the build will be published on PYPI. If the build or
   tests fail, then an issue and branch should be created to address and solve
   the errors before proceeding with the publishing of the branch.

3. Merge version bump branch into ``master`` branch.

Major and Minor Releases
^^^^^^^^^^^^^^^^^^^^^^^^
Major and minor releases may add one or more trivial or non-trivial features
and functionalities.

1. Create a new branch off of the ``master`` named something like
   ``release-[major,minor]-{NEW_VERSION}``.

   a. Use ``poetry version patch`` to increase the patch value appropriately in
      the :file:`pyproject.toml` file. This is important because the automated
      release process will try to publish the version listed in this file and it
      will error out if the version it tries to upload to PYPI already exists.

   b. Rename the ``docs/release_notes/pending_release.rst`` file to
      ``docs/release_notes/v{VERSION}.rst``, matching the new version value.
      Add a descriptive paragraph under the title section summarizing this
      release. During the automated process, this new, versioned file will referenced
      to create the header of the release on Github.

   c. Add a reference to the new release notes RST file in
      ``docs/release_notes.rst``.

   d. In a separate commit, add back a blank pending release notes file stub.
      See `Stub Pending Notes File`_.

2. Tag branch from the command line (see `Tag new version`_ below ). After the
   tag is pushed, a CI check and build will automatically run. Should everything
   pass without issue, the build will be published on PYPI. If the build or
   tests fail, then an issue and branch should be created to address and solve
   the errors before proceeding with the publishing of the branch.

3. Merge version bump branch into the ``master`` branch.


Stub Pending Notes File
^^^^^^^^^^^^^^^^^^^^^^^
The following is the basic content that goes into the stub pending release
notes file:

.. code-block::

    Pending Release Notes
    =====================

    Updates / New Features
    ----------------------

    Fixes
    -----

Tag new version
---------------
Release branches should be tagged in order to record where in the git tree a
particular release refers to.
The branch off of ``master`` is usually the target of such tags.

Currently the ``From GitHub`` method is preferred as it creates a "verified"
release.

From GitHub
^^^^^^^^^^^
Navigate to the `releases page on GitHub`_ and click the ``Draft a new
release`` button in upper right.

Fill in the new version in the ``Tag version`` text box (e.g. ``v#.#.#``)
and use the same string in the ``Release title`` text box.
The "@" target should be the release branch created above.

Copy and past this version's release notes into the ``Describe this release``
text box.

Remember to check the ``This is a pre-release`` check-box if appropriate.

Click the ``Public release`` button at the bottom of the page when complete.

From Git on the Command Line
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Create a new git tag using the new version number (format:
``v<MAJOR.<MINOR>.<PATCH>``) on the merge commit for the version update branch
merger::

    $ git tag -a -m "[Major|Minor|Patch] release v#.#.#"

Push this new tag to GitHub (or appropriate remote)::

    $ git push origin v#.#.#

To add the release notes to GitHub, navigate to the `tags page on GitHub`_
and click on the "Add release notes" link for the new release tag.  Copy and
paste this version's release notes into the description field and the version
number should be used as the release title.

Create new version release to PYPI
----------------------------------

__ https://python-poetry.org/docs/repositories/#configuring-credentials

We will use Poetry again to perform package building and publishing.
See `this documentation`__ on how to set and store your PYPA credentials in Poetry.

Make sure the source is checked out on the appropriate  version tag, the repo
is clean (no uncommited files/edits). ``git clean`` may help ensure a clean
state::

    $ git checkout <VERSION_TAG>
    $ git clean -xdi  # NOTE: `-i` makes this an interactive command.

Build source and wheel packages for the current version::

    $ poetry build

The files in `./dist/` may be inspected for correctness before publishing to
PYPA with::

    $ poetry publish


.. _Poetry's version command: https://python-poetry.org/docs/cli/#version
.. _releases page on GitHub: https://github.com/Kitware/SMQTK-Core/releases
.. _tags page on GitHub: https://github.com/Kitware/SMQTK-Core/tags
