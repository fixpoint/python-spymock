import json
import urllib.request
from http.client import HTTPResponse

from spymock import SpyMock, spy


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
