import enum
from functools import wraps
from typing import Callable


@enum.unique
class WrappedMethodType (enum.Enum):
    """
    Enumeration of the ways to interpret a given function for appliation to the
    wrapped class: an instance method, a class method, or to use it as-is ("raw").
    A "raw" function will be assumed to be appropriately parameterized for use
    in a class.
    """
    NONE = enum.auto()
    INSTANCE = enum.auto()
    CLASS = enum.auto()
    STATIC = enum.auto()


def _wrap_function(func: Callable, wrapped_method_type: WrappedMethodType):
    """
    Wrap an input callable in preparation for assignment to a class as a
    property of some kind.

    :param func: Function to wrap.
    :param wrapped_method_type: Enum flag for how we should wrap the given
        function, or not at all. By default we wrap the given function as an
        instance method in the generated class.
    :return: Function wrapped for membership in a class type.
    """
    # Wrap the function appropriately as a member or class method
    if wrapped_method_type == WrappedMethodType.INSTANCE:
        @wraps(func)
        def mem_func(self, *args, **kwargs):
            return func(*args, **kwargs)
    elif wrapped_method_type == WrappedMethodType.CLASS:
        @classmethod
        @wraps(func)
        def mem_func(cls, *args, **kwargs):
            return func(*args, **kwargs)
    elif wrapped_method_type == WrappedMethodType.STATIC:
        mem_func = staticmethod(func)
    elif wrapped_method_type == WrappedMethodType.NONE:
        mem_func = func
    else:
        raise ValueError(
            f"Invalid enumerate value provided. "
            f"Expected one of the `WrappedMethodType` constants. "
            f"Instead given: {wrapped_method_type}")
    return mem_func


def wrap_inline(
    parent_cls: type,
    method_name: str,
    wrapped_method_type: WrappedMethodType = WrappedMethodType.INSTANCE,
):
    """
    For when you really don't want to write a sub-class.

    Probably no real good reason to use this. Just write a sub-class. There
    are so many ways to do that with new and existing functional components.

    A basic use of this utility might look like the following:
        >>> import abc, smqtk_core
        >>> class SomeParentClass (smqtk_core.Pluggable):
        ...     @abc.abstractmethod
        ...     def work_function(self) -> str:
        ...         ''' Some abstract function. '''
        >>> # Our local code where we want to quickly define an implementation
        >>> # of the interface without writing class definition boiler-plate.
        >>> @wrap_inline(SomeParentClass,"work_function")
        ... def implementation():
        ...     return "product"
        >>> inst = implementation()
        >>> inst.work_function()
        'product'
        >>> # We've also now created and, via subclassing, registered an
        >>> # implementation for the pluggable interface:
        >>> SomeParentClass.get_impls()
        {<class 'abc.implementation'>}

    This could be chained as well, but really, just make a sub-class:
        >>> @implementation.wrap_another('other_method')
        ... def implementation():
        ...     return "other product"
        >>> inst = implementation()
        >>> inst.work_function()
        'product'
        >>> inst.other_method()
        'other product'

    When using `smqtk_core.Plugabble`, which tracks distinct sub-class
    implementations, chaining wrappings will create multiple implementations.
    This may be OK if wrapping for multiple abstract functions, but the above
    example will create a second registered "implementation" of the
    `SomeParentClass` interface:
        >>> # Additional wrapping creates additional class types.
        >>> SomeParentClass.get_impls()
        {<class 'abc.implementation'>, <class 'abc.implementation'>}

    :param parent_cls: Parent class to descend from.
    :param method_name: String name of the property the decorated function
        should take on in the generated class.
    :param wrapped_method_type: Enum flag for how we should wrap the given
        function, or not at all. By default we wrap the given function as an
        instance method in the generated class.

    :return: Decorator function closure.
    """
    def closure(func):
        return type(
            func.__name__,
            (parent_cls,),
            {
                method_name: _wrap_function(func, wrapped_method_type),
                "wrap_another": classmethod(wrap_inline),
            }
        )

    return closure
