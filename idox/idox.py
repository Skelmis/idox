import asyncio
import re
from enum import Enum
from pathlib import Path

import httpx
import orjson
from commons import exception_as_string

from idox import MalformedRequest, Request, SequenceT, NumericSequence

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
        *,
        max_concurrency: int = 25,
        output_directory: Path = Path("./output"),
        incoming_request: str | None = None,
        request_file_path: Path | None = None,
        injection_point: str = "$INJECT$",
        sequencer: SequenceT = NumericSequence(),
    ):
        self.output_directory: Path = output_directory
        self.max_concurrent: int = max_concurrency
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self._iter_num = NumericSequence()
        self.sequencer: SequenceT = sequencer

        if incoming_request is None and request_file_path is None:
            raise ValueError(
                "I require at-least one of incoming_request or"
                " request_file_path to work"
            )

        if incoming_request is None:
            with open(request_file_path, "r") as f:
                incoming_request = f.read()

        self.request: Request = self.split_request(incoming_request)

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
                method=request_type,
            )

        except Exception as e:
            raise MalformedRequest from e

    def extension_from_response(self, response: httpx.Response):
        content = response.text
        content_type = response.headers.get("Content-Type")
        if "<!DOCTYPE html>" in content:
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

        else:
            # Let's look at the content disposition now
            # we are passed the shit I threw at the site
            content_disp = response.headers.get("Content-Disposition")
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

        try:
            async with self.semaphore:
                if self.request.body:
                    if isinstance(self.request.body, dict):
                        resp = await ac.request(
                            self.request.method,
                            url=url,
                            cookies=self.request.cookies,
                            json=self.request.body,
                        )
                    else:
                        resp = await ac.request(
                            self.request.method,
                            url=url,
                            cookies=self.request.cookies,
                            content=self.request.body,
                        )
                else:
                    resp = await ac.request(
                        self.request.method,
                        url=url,
                        cookies=self.request.cookies,
                    )
        except Exception as e:
            print(exception_as_string(e))

        if resp.status_code >= 300:
            print(f"Request returned non-200 code. {resp.text}")
            return

        ext = self.extension_from_response(resp)
        ext_path = self.output_directory / ext
        all_path = self.output_directory / "all"
        ext_path.mkdir(parents=True, exist_ok=True)
        all_path.mkdir(parents=True, exist_ok=True)
        byte_content = resp.content
        iter_num = next(self._iter_num)
        with open(ext_path / f"{iter_num}.{ext}", "wb") as f:
            f.write(byte_content)

        with open(all_path / f"{iter_num}.{ext}", "wb") as f:
            f.write(byte_content)

    async def run(self):
        limits = httpx.Limits(
            max_keepalive_connections=None,
            max_connections=None,
            keepalive_expiry=None,
        )
        async with httpx.AsyncClient(limits=limits) as client:
            coros = [self._make_request(client, i) for i in self.sequencer]
            await asyncio.gather(*coros)
