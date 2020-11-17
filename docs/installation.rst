Installation
============

There are two ways to get ahold of SMQTK-Core.
The simplest is to install via the :command:`pip` command.
Alternatively, the source tree can be acquired and build/install SMQTK-Core via CMake or ``setuptools``.


From :command:`pip`
-------------------

.. prompt:: bash

    pip install --upgrade smqtk-core

This method will install all of the same functionality as when installing from source.

Extras
^^^^^^
A few extras are defined for the ``smqtk-core`` package:

- ``docs``
    - Dependencies for building SMQTK-Core documentation.
- ``test``
    - Dependencies for run SMQTK-Core testing components.


From Source
-----------

Quick Start
^^^^^^^^^^^

.. prompt:: bash

    # Check things out
    cd /where/things/should/go/
    git clone https://github.com/Kitware/smqtk-core.git smqtk-core
    # Install pinned python dependencies to environment
    pip install -r ./smqtk-core/requirements.txt
    # Install the smqtk-core package.
    pip install -e ./smqtk-core/
    # Running tests
    cd ./smqtk-core/
    pytest


Installing Python dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. prompt:: bash

    pip install -r requirements.txt

SMQTK-Core pinned python dependencies are rooted in :file:`requirements.txt`
file found in the root of the source tree.
This defers to modular component requirements located in the
:file:`requirements/` directory.
These files detail different dependencies, and their exact, latest versions
tested.

There are no required third-party dependencies for this package.

If you wish to be able to build the Sphinx_ based documentation for the
project, the :file:`requirements/docs.txt` lists the appropriate pinned
depedencies.
There is a separate requirements file specifically for use by the ReadTheDocs
build process, :file:`docs/readthedocs-reqs.txt`, which takes into account that
RTD has its own pinned versions for some packages.


Building the Documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^

All of the documentation for SMQTK-Core is maintained as a collection of
`reStructuredText_` documents in the :file:`docs` folder of the project.
This documentation can be processed by the :program:`Sphinx` documentation tool
into a variety of documentation formats, the most common of which is HTML.

Within the :file:`docs` directory is a Unix :file:`Makefile` (for Windows
systems, a :file:`make.bat` file with similar capabilities exists).
This :file:`Makefile` takes care of the work required to run :program:`Sphinx`
to convert the raw documentation to an attractive output format.
For example::

    make html

Will generate HTML format documentation rooted at
:file:`docs/_build/html/index.html`.

The command::

    make help

Will show the other documentation formats that may be available (although be
aware that some of them require additional dependencies such as :program:`TeX`
or :program:`LaTeX`.)


Live Preview
""""""""""""

While writing documentation in a mark up format such as ``reStructuredText`` it
is very helpful to be able to preview the formatted version of the text.
While it is possible to simply run the ``make html`` command periodically, a
more seamless version of this is available.
Within the :file:`docs` directory is a small Python script called
:file:`sphinx_server.py` that can simply be called with::

    python sphinx_server.py

It will run small process that watches the :file:`docs` folder for changes in
the raw documentation :file:`*.rst` files and re-runs :command:`make html` when changes are detected.
It will serve the resulting HTML files at http://localhost:5500.
Thus having that URL open in a browser will provide you with a relatively up to date preview of the rendered documentation.


.. _Sphinx: http://sphinx-doc.org/
.. _reStructuredText: http://docutils.sourceforge.net/rst.html
