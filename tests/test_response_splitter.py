from unittest.mock import Mock

import pytest

from idox import Idox, Response, MalformedResponse


def test_html_resp(html_resp):
    idox: Idox = Idox(Mock(), request_url="https://example.com/{INJECT}")
    response: Response = idox.split_response(html_resp)
    assert response.status_code == 200
    assert response.proto == "HTTP/2"
    assert response.status_text == "OK"
    assert response.headers == {
        "Date": "Tue, 17 Jun 2025 09:55:27 GMT",
        "Content-Type": "text/html; charset=utf-8",
    }
    assert (
        response.body
        == '<!doctype html>\n<html lang="en">\n  <head>HEAD</head>\n  <body>BODY</body>\n</html>'
    )


def test_html_resp_with_nested_newline(html_extra_newline_resp):
    idox: Idox = Idox(Mock(), request_url="https://example.com/{INJECT}")
    response: Response = idox.split_response(html_extra_newline_resp)
    assert response.status_code == 200
    assert response.proto == "HTTP/2"
    assert response.status_text == "OK"
    assert response.headers == {
        "Date": "Tue, 17 Jun 2025 09:55:27 GMT",
        "Content-Type": "text/html; charset=utf-8",
    }
    assert (
        response.body
        == '<!doctype html>\n<html lang="en">\n  <head>HEAD</head>\n  <body>BODY</body>\n\n\n</html>'
    )


def test_404(not_found):
    idox: Idox = Idox(Mock(), request_url="https://example.com/{INJECT}")
    response: Response = idox.split_response(not_found)
    assert response.status_code == 404
    assert response.proto == "HTTP/1.1"
    assert response.status_text == "Not Found"
    assert response.headers == {
        "content-type": "text/html; charset=utf-8",
    }
    assert (
        response.body
        == '{"status": "FAILED"}'
    )


def test_malformed_response(malformed_request):
    with pytest.raises(MalformedResponse):
        idox: Idox = Idox(Mock(), request_url="https://example.com/{INJECT}")
        idox.split_response(malformed_request)
