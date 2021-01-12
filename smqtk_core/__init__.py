# REMEMBER: `distutils.version.*Version` types can be used to compare versions
# from strings like this.
# SMQTK prefers to use the strict numbering standard when possible.
__version__ = "0.15.0"

from .configuration import Configurable  # noqa: F401
from .plugin import Pluggable  # noqa: F401
