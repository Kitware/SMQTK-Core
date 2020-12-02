#!/usr/bin/env python
import ast
from pathlib import Path
import pkg_resources
# noinspection PyUnresolvedReferences
from pkg_resources.extern import packaging
import setuptools
from typing import cast, Generator, Iterable, List, Optional, Tuple, Union
import urllib.parse


###############################################################################
# Some helper functions

def parse_version(fpath: Union[str, Path]) -> str:
    """
    Statically parse the "__version__" number string from a python file.

    TODO: Auto-append dev version based on how forward from latest release
          Basically a simpler version of what setuptools_scm does but without
          the added cruft and bringing the ENTIRE git repo in with the dist
          See: https://github.com/pypa/setuptools_scm/blob/master/setuptools_scm/version.py
          Would need to know number of commits ahead from last version tag.
    """
    with open(fpath, 'r') as file_:
        pt = ast.parse(file_.read())

    class VersionVisitor(ast.NodeVisitor):
        def __init__(self) -> None:
            self.version: Optional[str] = None

        def visit_Assign(self, node: ast.Assign) -> None:
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__version__":
                    self.version = cast(ast.Str, node.value).s

    visitor = VersionVisitor()
    visitor.visit(pt)
    if visitor.version is None:
        raise RuntimeError("Failed to find __version__!")
    return visitor.version


def parse_req_strip_version(filepath: Union[str, Path]) -> List[str]:
    """
    Read requirements file and return the list of requirements specified
    therein but with their version aspects striped.

    See pkg_resources.Requirement docs here:
        https://setuptools.readthedocs.io/en/latest/pkg_resources.html#requirement-objects
    """
    filepath = Path(filepath)
    # Known prefixes of lines that are definitely not requirements
    # specifications.
    skip_prefix_tuple = (
        "#", "--index-url"
    )

    def filter_req_lines(_filepath: Path) -> Generator[str, None, None]:
        """ Filter lines from file that are requirements. """
        with open(_filepath, 'r') as _f:
            for _line in _f:
                _line = _line.strip()
                if not _line or _line.startswith(skip_prefix_tuple):
                    # Empty or has a skippable prefix.
                    continue
                elif _line.startswith('-r '):
                    # sub-requirements file specification, yield that file's
                    # req lines.
                    target = _filepath.parent / _line.split(" ")[1]
                    for _r_line in filter_req_lines(target):
                        yield _r_line
                elif _line.startswith('-e '):
                    # Indicator for URL-based requirement. Look to the egg
                    # fragment.
                    frag = urllib.parse.urlparse(_line.split(' ')[1]).fragment
                    try:
                        egg = dict(
                            cast(Tuple[str, str], part.split('=', 1))
                            for part in frag.split('&')
                            if part  # handle no fragments
                        )['egg']
                    except KeyError:
                        raise packaging.requirements.InvalidRequirement(
                            f"Failed to parse egg name from the requirements "
                            f"line: '{_line}'"
                        )
                    yield egg
                else:
                    yield _line

    def strip_req_specifier(
        req_iter: Iterable[pkg_resources.Requirement]
    ) -> Generator[pkg_resources.Requirement, None, None]:
        """
        Modify requirements objects to null out the specifier component.
        """
        for r in req_iter:
            r.specs = []
            # `specifier` property is defined in extern base-class of the
            # `pkg_resources.Requirement` type.
            # noinspection PyTypeHints
            r.specifier = packaging.specifiers.SpecifierSet()  # type: ignore
            yield r

    return [
        str(req)
        for req in strip_req_specifier(
            pkg_resources.parse_requirements(filter_req_lines(filepath))
        )
    ]


################################################################################

PACKAGE_NAME = "smqtk_core"
SETUP_DIR = Path(__file__).parent

with open(SETUP_DIR / 'README.md') as f:
    LONG_DESCRIPTION = f.read()

VERSION = parse_version(SETUP_DIR / "smqtk_core" / "__init__.py")


if __name__ == "__main__":
    setuptools.setup(
        name=PACKAGE_NAME,
        version=VERSION,
        description=(
            'Python toolkit for pluggable algorithms and data structures '
            'for multimedia-based machine learning'
        ),
        long_description=LONG_DESCRIPTION,
        author='Kitware, Inc.',
        author_email='smqtk-developers@kitware.com',
        url='https://gitlab.kitware.com/smqtk/smqtk-core',
        license='BSD 3-Clause',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: BSD License',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: Unix',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
        ],
        platforms=[
            'Linux',
            'Mac OS-X',
            'Unix',
            # 'Windows',  # Not tested yet
        ],

        packages=[PACKAGE_NAME],
        package_data={PACKAGE_NAME: ["py.typed"]},
        # Required for mypy to be able to find the installed package.
        # https://mypy.readthedocs.io/en/latest/installed_packages.html#installed-packages
        zip_safe=False,

        install_requires=[],
        extras_require={
            'docs': parse_req_strip_version(SETUP_DIR / "requirements" / "docs.txt"),
            'test': parse_req_strip_version(SETUP_DIR / "requirements" / "test.txt"),
        }
    )
