from unittest.mock import patch

from .spymock import SpyMock


def spy(target, attribute, **kwargs):
    return patch.object(
        target, attribute, new=SpyMock(getattr(target, attribute)), **kwargs
    )
