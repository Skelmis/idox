from typing import NamedTuple


class Request(NamedTuple):
    url: str
    method: str
    body: str | dict
    headers: dict[str, str]
    cookies: list[tuple[str, str]]
