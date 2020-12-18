from functools import partial, wraps
from typing import Any, Callable, List
from unittest.mock import create_autospec


def SpyMock(fn: Callable[..., Any], **kwargs) -> Callable[..., Any]:
    """Create MagicMock for functions to record return_values or exceptions

    Returned MagicMock instance has the following extra fields and methods

    call_values_or_exceptions:
        A List which items are return values or exceptions.

    For example:

    >>> def fn(*args, **kwargs):
    ...     if len(args) == 0:
    ...         raise Exception
    ...     return [args, kwargs]
    >>> s = SpyMock(fn)
    >>> s("Hello", "World")
    [('Hello', 'World'), {}]
    >>> s.call_values_or_exceptions
    [[('Hello', 'World'), {}]]

    >>> s("Goodbye", "Sunday")
    [('Goodbye', 'Sunday'), {}]
    >>> s.call_values_or_exceptions
    [[('Hello', 'World'), {}], [('Goodbye', 'Sunday'), {}]]

    >>> s()
    Traceback (most recent call last):
        ...
    Exception
    >>> s.call_values_or_exceptions
    [[('Hello', 'World'), {}], [('Goodbye', 'Sunday'), {}], Exception()]
    """

    @wraps(fn)
    def inner(*args, **kwargs):
        try:
            r = fn(*args, **kwargs)
            m.call_values_or_exceptions.append(r)
        except Exception as e:
            m.call_values_or_exceptions.append(e)
            raise
        return r

    m = create_autospec(fn, side_effect=inner)
    m.call_values_or_exceptions = []

    @wraps(m.reset_mock)
    def reset_mock(orig, *args, **kwargs):
        m.call_values_or_exceptions = []
        return orig(*args, **kwargs)

    m.reset_mock = partial(reset_mock, m.reset_mock)

    return m


if __name__ == "__main__":
    import doctest

    doctest.testmod()
