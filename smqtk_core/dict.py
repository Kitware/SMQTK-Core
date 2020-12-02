"""
Utility functions pertaining to python dictionaries.
"""
import copy
from typing import Dict


def merge_dict(a: Dict, b: Dict, deep_copy: bool = False) -> Dict:
    """
    Merge dictionary b into dictionary a.

    This is different than normal dictionary update in that we don't bash
    nested dictionaries, instead recursively updating them.

    For congruent keys, values are are overwritten, while new keys in ``b`` are
    simply added to ``a``.

    Values are assigned (not copied) by default. Setting ``deep_copy`` causes
    values from ``b`` to be deep-copied into ``a``.

    :param a: The "base" dictionary that is updated in place.
    :param b: The dictionary to merge into ``a`` recursively.
    :param deep_copy: Optionally deep-copy values from ``b`` when assigning
        into ``a``.

    :return: ``a`` dictionary after merger (not a copy).

    """
    for k in b:
        if k in a and isinstance(a[k], dict) and isinstance(b[k], dict):
            merge_dict(a[k], b[k], deep_copy)
        elif deep_copy:
            a[k] = copy.deepcopy(b[k])
        else:
            a[k] = b[k]
    return a
