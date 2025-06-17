from typing import NamedTuple

from idox import CaseInsensitiveDict


class Request(NamedTuple):
    url: str
    method: str
    body: str | dict
    headers: CaseInsensitiveDict
    cookies: list[tuple[str, str]]