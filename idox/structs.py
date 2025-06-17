from typing import NamedTuple

from idox import CaseInsensitiveDict


class Request(NamedTuple):
    url: str
    method: str
    body: str | dict
    headers: CaseInsensitiveDict
    cookies: list[tuple[str, str]]


class Response(NamedTuple):
    proto: str
    status_code: int
    status_text: str
    headers: CaseInsensitiveDict
    body: str | dict
