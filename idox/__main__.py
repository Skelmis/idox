import asyncio
from enum import Enum
from pathlib import Path
from typing import Annotated, Literal

import typer

from idox import Idox, NumericSequence


class SequenceTypes(str, Enum):
    NUMERIC = "Numeric"


class ProtocolChoices(str, Enum):
    http = "http"
    https = "https"


def main(
    ending_number: Annotated[
        int, typer.Argument(help="The number of requests to send")
    ],
    request_file_path: Annotated[Path, typer.Option(help="The path to the burp file")],
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

    async def async_main():
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
        print("Starting Idox\r", end="")
        await idox.run()
        print("Finished running")

    asyncio.run(async_main())


if __name__ == "__main__":
    typer.run(main)
