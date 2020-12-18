# spymock

![PyPI](https://img.shields.io/pypi/v/python-spymock)
![PyPI - License](https://img.shields.io/pypi/l/python-spymock)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/python-spymock)
![Test](https://github.com/fixpoint/python-spymock/workflows/Test/badge.svg)

This library provides `SpyMock` which is similar to [`MagicMock`](https://docs.python.org/3/library/unittest.mock.html#magic-mock) but recording function return values and exceptions on `call_values_or_exceptions` attribute.

## Installation

```
pip install python-spymock
```

## Usage

Use `spymock.spy` function as-like [`patch.object`](https://docs.python.org/3/library/unittest.mock.html#patch-object) to spy and mock the target attribute like:

```python
import urllib.request

from spymock import spy


def request():
    url = "http://httpbin.org/json"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as res:
        return json.loads(res.read())


def test_request_with_spy():
    with spy(urllib.request, "urlopen") as s:
        assert request() == {
            "slideshow": {
                "author": "Yours Truly",
                "date": "date of publication",
                "slides": [
                    {"title": "Wake up to WonderWidgets!", "type": "all"},
                    {
                        "items": [
                            "Why <em>WonderWidgets</em> are great",
                            "Who <em>buys</em> WonderWidgets",
                        ],
                        "title": "Overview",
                        "type": "all",
                    },
                ],
                "title": "Sample Slide Show",
            }
        }

        # 's' is like MagicMock but it has 'call_values_or_exceptions' attribute
        assert len(s.call_values_or_exceptions) == 1

        r = s.call_values_or_exceptions[0]
        assert isinstance(r, HTTPResponse)
        assert r.status == 200
        assert r.reason == "OK"
```

Or directly create `spymock.SpyMock` instance as-like [`MagicMock`](https://docs.python.org/3/library/unittest.mock.html#magic-mock) like:

```python
import urllib.request

from spymock import SpyMock


def request():
    url = "http://httpbin.org/json"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as res:
        return json.loads(res.read())


def test_request_with_spymock():
    s = SpyMock(request)
    assert s() == {
        "slideshow": {
            "author": "Yours Truly",
            "date": "date of publication",
            "slides": [
                {"title": "Wake up to WonderWidgets!", "type": "all"},
                {
                    "items": [
                        "Why <em>WonderWidgets</em> are great",
                        "Who <em>buys</em> WonderWidgets",
                    ],
                    "title": "Overview",
                    "type": "all",
                },
            ],
            "title": "Sample Slide Show",
        }
    }

    # 's' is like MagicMock but it has 'call_values_or_exceptions' attribute
    assert len(s.call_values_or_exceptions) == 1

    r = s.call_values_or_exceptions[0]
    assert r == {
        "slideshow": {
            "author": "Yours Truly",
            "date": "date of publication",
            "slides": [
                {"title": "Wake up to WonderWidgets!", "type": "all"},
                {
                    "items": [
                        "Why <em>WonderWidgets</em> are great",
                        "Who <em>buys</em> WonderWidgets",
                    ],
                    "title": "Overview",
                    "type": "all",
                },
            ],
            "title": "Sample Slide Show",
        }
    }
```

## License

Distributed under the terms of the [MIT license](./LICENSE).
