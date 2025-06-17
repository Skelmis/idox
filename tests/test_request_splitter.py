from unittest.mock import Mock

import pytest

from idox import MalformedRequest, Request, Idox


# noinspection DuplicatedCode
def test_get_request(get_request):
    idox: Idox = Idox(Mock(), request_url="https://example.com/{INJECT}")
    request: Request = idox.split_request(get_request)

    assert request.url == "blurp.skelmis.co.nz/"
    assert request.method == "GET"
    assert request.body == ""
    assert request.headers == {
        "X-TEST": "Hello World",
        "Host": "blurp.skelmis.co.nz",
        "Cookie": "one=1; two=2;",
    }
    assert request.headers == {
        "X-tEsT": "Hello World",
        "host": "blurp.skelmis.co.nz",
        "COOKIE": "one=1; two=2;",
    }
    assert request.cookies == [("one", "1"), ("two", "2")]


# noinspection DuplicatedCode
def test_malformed_request(malformed_request):
    with pytest.raises(MalformedRequest):
        idox: Idox = Idox(Mock(), request_url="https://example.com/{INJECT}")
        idox.split_request(malformed_request)


# noinspection DuplicatedCode
def test_post_form_request(post_form_request):
    idox: Idox = Idox(Mock(), request_url="https://example.com/{INJECT}")
    request: Request = idox.split_request(post_form_request)

    assert request.url == "blurp.skelmis.co.nz/test"
    assert request.method == "POST"
    assert request.body == "field1=value1&field2=value2"
    assert request.headers == {
        "Host": "blurp.skelmis.co.nz",
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": "27",
    }
    assert request.cookies == []


# noinspection DuplicatedCode
def test_post_json_request(post_json_request):
    idox: Idox = Idox(Mock(), request_url="https://example.com/{INJECT}")
    request: Request = idox.split_request(post_json_request)

    assert request.url == "blurp.skelmis.co.nz/json"
    assert request.method == "POST"
    assert request.body == {"id": False}
    assert request.headers == {
        "Host": "blurp.skelmis.co.nz",
        "Content-Type": "application/json",
        "Content-Length": "81",
        "Accept": "application/json",
    }
    assert request.cookies == []
