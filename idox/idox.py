import asyncio
import re
from collections import defaultdict
from enum import Enum
from pathlib import Path

import httpx
import orjson
from commons import exception_as_string

from idox.exceptions import MalformedRequest
from idox.sequences import SequenceT
from idox.structs import Request

disp_pattern = re.compile(r".*filename=\"[a-zA-Z0-9`; -_=\[\]]*\.(.*)\"")


class InjectionPoint(Enum):
    URL = 1
    BODY = 2
    COOKIES = 3
    HEADERS = 4


# noinspection PyMethodMayBeStatic
class Idox:
    def __init__(
        self,
        sequencer: SequenceT,
        *,
        max_concurrency: int = 25,
        output_directory: Path = Path("./output"),
        request_file_path: Path | None = None,
        request_url: str | None = None,
        request_method: str = "GET",
        injection_point: str = "{INJECT}",
        protocol: str = "https",
    ):
        self.output_directory: Path = output_directory
        self.max_concurrent: int = max_concurrency
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.sequencer: SequenceT = sequencer
        self.protocol: str = protocol

        self.seen_codes: dict[int, int] = defaultdict(lambda: 0)
        self.seen_errors: dict[str, int] = defaultdict(lambda: 0)

        if request_url is None and request_file_path is None:
            raise ValueError(
                "I require at-least one of incoming_request or"
                " request_file_path to work"
            )

        if request_url is None:
            with open(request_file_path, "r") as f:
                incoming_request = f.read()

            self.request: Request = self.split_request(incoming_request)

        else:
            self.request: Request = Request(
                url=request_url,
                method=request_method,
                body="",
                cookies=[],
                headers={},
            )

        # Find the injection point
        self._injection_string: str = injection_point
        if injection_point in self.request.url:
            self._injection_point: InjectionPoint = InjectionPoint.URL
        elif injection_point in str(self.request.headers):
            self._injection_point: InjectionPoint = InjectionPoint.HEADERS
        elif injection_point in str(self.request.cookies):
            self._injection_point: InjectionPoint = InjectionPoint.COOKIES
        elif injection_point in str(self.request.body):
            self._injection_point: InjectionPoint = InjectionPoint.BODY
        else:
            raise ValueError(f"Failed to find {self._injection_string} in the request")

    @classmethod
    def split_request(cls, request: str) -> Request:
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
            try:
                raw_headers, body = code.split("\n\n")
            except ValueError:
                # Likely missing an extra line just assume body is empty
                raw_headers, body = code.removesuffix("\n"), ""

            headers: list[str] = raw_headers.split("\n")  # type: ignore
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
                method=request_type,
            )

        except Exception as e:
            raise MalformedRequest from e

    def extension_from_response(self, response: httpx.Response):
        content = response.text
        content_type = response.headers.get("Content-Type", "")
        # TODO Add more extensions
        if "<!DOCTYPE html>" in content or "</html>" in content:
            extension = "html"

        elif content.startswith("<?xml"):
            extension = "xml"

        elif (
            "X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"
            in content
        ):
            # Eicar me up
            extension = "txt"

        elif "image/png" in content_type:
            extension = "png"

        elif "image/jpeg" in content_type:
            extension = "jpeg"

        elif "application/pdf" in content_type:
            extension = "pdf"

        elif "application/json" in content_type:
            extension = "json"

        else:
            # Let's look at the content disposition now
            # we are passed the shit I threw at the site
            content_disp = response.headers.get("Content-Disposition")
            if content_disp is None:
                return "txt"

            try:
                extension_find = disp_pattern.search(content_disp)
                extension = extension_find.group(1).lstrip(".")
            except (ValueError, AttributeError, TypeError) as e:
                extension = "txt"
                print(exception_as_string(e))

        return extension

    async def _make_request(self, ac: httpx.AsyncClient, current_iter: str):
        url = self.request.url
        if self._injection_point is InjectionPoint.URL:
            url = self.request.url.replace(self._injection_string, current_iter)

        # Guesstimate this is correct
        if not url.startswith("http"):
            url = self.protocol + "://" + url

        try:
            async with self.semaphore:
                if self.request.body:
                    if isinstance(self.request.body, dict):
                        body = self.request.body
                        if self._injection_point is InjectionPoint.BODY:
                            body = orjson.dumps(body)
                            body = body.replace(self._injection_string, current_iter)
                            body = orjson.loads(body)

                        resp = await ac.request(
                            self.request.method,
                            url=url,
                            cookies=self.request.cookies,
                            json=body,
                            headers=self.request.headers,
                        )
                    else:
                        body = self.request.body
                        if self._injection_point is InjectionPoint.BODY:
                            body = body.replace(self._injection_string, current_iter)

                        resp = await ac.request(
                            self.request.method,
                            url=url,
                            cookies=self.request.cookies,
                            content=body,
                            headers=self.request.headers,
                        )
                else:
                    resp = await ac.request(
                        self.request.method,
                        url=url,
                        cookies=self.request.cookies,
                        headers=self.request.headers,
                    )
        except Exception as e:
            self.seen_errors[e.__class__.__name__] += 1
            return

        ext = self.extension_from_response(resp)
        ext_path = self.output_directory / ext
        all_path = self.output_directory / "all"
        code_path = self.output_directory / "status_code" / str(resp.status_code)
        ext_path.mkdir(parents=True, exist_ok=True)
        all_path.mkdir(parents=True, exist_ok=True)
        code_path.mkdir(parents=True, exist_ok=True)
        byte_content = resp.content
        output_name = f"{current_iter}.{ext}"
        base_all_path = (all_path / output_name).absolute()
        with open(base_all_path, "wb") as f:
            f.write(byte_content)

        r_1 = (ext_path / output_name).absolute()
        r_1.unlink(missing_ok=True)
        r_1.hardlink_to(base_all_path)
        r_2 = (code_path / output_name).absolute()
        r_2.unlink(missing_ok=True)
        r_2.hardlink_to(base_all_path)

        self.seen_codes[resp.status_code] += 1

    async def run(self):
        limits = httpx.Limits(
            max_keepalive_connections=None,
            max_connections=None,
            keepalive_expiry=None,
        )
        async with httpx.AsyncClient(limits=limits) as client:
            coros = [self._make_request(client, i) for i in self.sequencer]
            await asyncio.gather(*coros)
