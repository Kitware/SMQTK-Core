Installation
============

There are two ways to get ahold of SMQTK-Core.
The simplest is to install via the :command:`pip` command.
Alternatively, the source tree can be acquired and be locally developed using
`Poetry`_.

For more information on the use of `Poetry`_, follow these links fr
`installation`_ and `usage`_ documentation.

.. _installation: Poetry-installation_
.. _usage: Poetry-usage_


From :command:`pip`
-------------------

.. prompt:: bash

    pip install smqtk-core

This method will install all of the same functionality as when installing from source.
If you have an existing installation and would like to upgrade your version,
provide the ``-U``/``--upgrade`` `option`__.

__ Pip-install-upgrade_


From Source
-----------
The following assumes `Poetry`_ is already installed.

Quick Start
^^^^^^^^^^^

.. prompt:: bash

    cd /where/things/should/go/
    git clone https://github.com/Kitware/smqtk-core.git ./
    poetry install
    # Since we're from source we can test the installation.
    poetry run pytest
    # We can also build the local documentation as it may be more up to date then ReadTheDocs.
    cd docs
    make html


Installing Python dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This project uses `Poetry`_ for depedency management, environment consistency,
version management, package building and publishing to PYPI.
Dependencies are `abstractly defined`_ in the :file:`pyproject.toml` file.
Additionally, `specifically pinned versions`_ are specified in the
:file:`poetry.lock` file for *development* environment consistency.
Both of these files can be found in the root of the source tree.

.. _abstractly defined: Poetry-dependencies_
.. _specifically pinned versions: Poetry-poetrylock_

The following command installs both installation and development dependencies
as specified in the :file:`pyproject.toml` file, with versions specified
(including for transitive dependencies) in the :file:`poetry.lock` file:

.. prompt:: bash

    poetry install


Building the Documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^
The documentation for SMQTK-Core is maintained as a collection of
`reStructuredText`_ documents in the :file:`docs/` folder of the project.
This documentation can be processed by the :program:`Sphinx` documentation tool
into a variety of documentation formats, the most common of which is HTML.

Within the :file:`docs/` directory is a Unix :file:`Makefile` (for Windows
systems, a :file:`make.bat` file with similar capabilities exists).
This :file:`Makefile` takes care of the work required to run :program:`Sphinx`
to convert the raw documentation to an attractive output format.
For example, as shown in the quickstart, calling ``make html`` will generate
HTML format documentation rooted at :file:`docs/_build/html/index.html`.

Calling the command ``make help`` here will show the other documentation
formats that may be available (although be aware that some of them require
additional dependencies such as :program:`TeX` or :program:`LaTeX`)


Live Preview
""""""""""""

While writing documentation in a mark up format such as `reStructuredText`_ it
is very helpful to be able to preview the formatted version of the text.
While it is possible to simply run the ``make html`` command periodically, a
more seamless workflow of this is available.
Within the :file:`docs/` directory is a small Python script called
:file:`sphinx_server.py` that can simply be called with:

.. prompt:: bash

    python sphinx_server.py

This will run a small process that watches the :file:`docs/` folder contents,
as well as the source files in :file:`smqtk_core/`, for changes.
:command:`make html` is re-run automatically when changes are detected.
This will serve the resulting HTML files at http://localhost:5500.
Having this URL open in a browser will provide you with a relatively up-to-date
preview of the rendered documentation.


.. _Pip-install-upgrade: https://pip.pypa.io/en/stable/reference/pip_install/#cmdoption-U
.. _Poetry: https://python-poetry.org
.. _Poetry-installation: https://python-poetry.org/docs/#installation
.. _Poetry-usage: https://python-poetry.org/docs/basic-usage/
.. _Poetry-poetrylock: https://python-poetry.org/docs/basic-usage/#installing-with-poetrylock
.. _Poetry-dependencies: https://python-poetry.org/docs/pyproject/#dependencies-and-dev-dependencies
.. _Sphinx: http://sphinx-doc.org/
.. _reStructuredText: http://docutils.sourceforge.net/rst.html
