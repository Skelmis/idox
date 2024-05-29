import asyncio
from enum import Enum
from pathlib import Path
from typing import Annotated

import typer

from idox import Idox, NumericSequence


class SequenceTypes(str, Enum):
    NUMERIC = "Numeric"


class ProtocolChoices(str, Enum):
    http = "http"
    https = "https"


class TypeChoices(str, Enum):
    get = "GET"
    post = "POST"


app = typer.Typer()


@app.command()
def file(
    ending_number: Annotated[
        int, typer.Argument(help="The number of requests to send up to")
    ],
    request_file_path: Annotated[
        Path, typer.Option(help="The path to the burp file")
    ] = None,
    starting_number: Annotated[
        int, typer.Option(help="The base number to start at")
    ] = 0,
    numeric_step: Annotated[
        int, typer.Option(help="The step between numbers to take on each iteration")
    ] = 1,
    max_concurrency: Annotated[
        int, typer.Option(help="Maximum concurrent requests to make at a time")
    ] = 25,
    output_directory: Annotated[
        Path, typer.Option(help="Directory to store results in")
    ] = Path("./output"),
    injection_point: Annotated[
        str, typer.Option(help="The injection point to put numbers in")
    ] = "$INJECT$",
    protocol: ProtocolChoices = "https",
):
    idox: Idox = Idox(
        NumericSequence(
            ending_number=ending_number,
            starting_number=starting_number,
            jump=numeric_step,
        ),
        request_file_path=request_file_path,
        protocol=protocol,
        output_directory=output_directory,
        max_concurrency=max_concurrency,
        injection_point=injection_point,
    )
    main(idox)


@app.command()
def url(
    url: Annotated[str, typer.Argument(help="The url to make requests to")],
    ending_number: Annotated[
        int, typer.Argument(help="The number of requests to send up to")
    ],
    starting_number: Annotated[
        int, typer.Option(help="The base number to start at")
    ] = 0,
    numeric_step: Annotated[
        int, typer.Option(help="The step between numbers to take on each iteration")
    ] = 1,
    max_concurrency: Annotated[
        int, typer.Option(help="Maximum concurrent requests to make at a time")
    ] = 25,
    output_directory: Annotated[
        Path, typer.Option(help="Directory to store results in")
    ] = Path("./output"),
    injection_point: Annotated[
        str, typer.Option(help="The injection point to put numbers in")
    ] = "$INJECT$",
    request_type: TypeChoices = "GET",
    protocol: ProtocolChoices = "https",
):
    idox: Idox = Idox(
        NumericSequence(
            ending_number=ending_number,
            starting_number=starting_number,
            jump=numeric_step,
        ),
        request_url=url,
        protocol=protocol,
        output_directory=output_directory,
        max_concurrency=max_concurrency,
        injection_point=injection_point,
        request_method=request_type.value,
    )
    main(idox)


def main(idox: Idox):
    async def async_main():
        print("Starting Idox\r", end="")
        await idox.run()
        print("Finished running")

    asyncio.run(async_main())


if __name__ == "__main__":
    app()
