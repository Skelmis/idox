from typing import Any

import orjson

from idox import MalformedRequest, Request


# noinspection PyMethodMayBeStatic
class Idox:
    def split_request(self, request: str) -> Request:
        """Given a valid HTTP request, return the headers

        Returns
        -------
        Request
            The request as split

        Raises
        ------
        MalformedRequest
            The request did not match the expected HTTP spec
        """
        try:
            # Handle input request
            code = request.replace("\r\n", "\n")
            headers, body = code.split("\n\n")
            headers: list[str] = headers.split("\n")  # type: ignore
            request_type, uri, _ = headers.pop(0).split(" ")
            request_type: str = request_type.upper()
            header_jar: dict[str, str] = {}
            for line in headers:
                k, v = line.split(": ", maxsplit=1)
                header_jar[k] = v

            cookies: list[tuple[str, str]] = []
            raw_cookies = header_jar.get("Cookie", "")
            for cookie in raw_cookies.split(";"):
                if "=" not in cookie:
                    continue
                k, v = cookie.split("=", maxsplit=1)
                cookies.append((k.strip(), v))

            if request_type == "POST":
                is_json = "json" in header_jar.get("Content-Type", "")
                if is_json:
                    body = orjson.loads(body)

            url = header_jar["Host"] + uri
            return Request(
                url=url,
                cookies=cookies,
                headers=header_jar,
                body=body,
                type=request_type,
            )

        except Exception as e:
            raise MalformedRequest from e
