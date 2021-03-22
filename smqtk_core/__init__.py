import abc
import pkg_resources

from .configuration import Configurable  # noqa: F401
from .plugin import Pluggable  # noqa: F401


# It is known that this will fail if SMQTK-Core is not "installed" in the
# current environment. Additional support is pending defined use-case-driven
# requirements.
__version__ = pkg_resources.get_distribution(__name__).version


class Plugfigurable (Pluggable, Configurable, metaclass=abc.ABCMeta):
    """
    When you don't want to have to constantly inherit from two mixin classes
    all the time, we provide this as a convenience that descends from both
    mixin classes: Pluggable and Configurable.
    """
