import asyncio
import io
import sys
from enum import Enum
from pathlib import Path
from typing import Annotated

import click
from click import style as s
import typer

from idox import Idox, NumericSequence, FileSequence, SequenceT


class SequenceTypes(str, Enum):
    NUMERIC = "Numeric"


class ProtocolChoices(str, Enum):
    http = "http"
    https = "https"


class TypeChoices(str, Enum):
    get = "GET"
    post = "POST"
    head = "HEAD"
    options = "OPTIONS"
    put = "PUT"
    delete = "DELETE"
    trace = "TRACE"
    patch = "PATCH"
    connect = "CONNECT"


app = typer.Typer(pretty_exceptions_show_locals=False, no_args_is_help=True)


@app.command()
def file(
    ending_number: Annotated[
        int, typer.Argument(help="The number of requests to send up to")
    ] = None,
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
    ] = "{INJECT}",
    sequence_file: Annotated[
        Path,
        typer.Option(
            help="The path to a file containing the ID's to use instead of auto incrementing id's"
        ),
    ] = None,
    protocol: ProtocolChoices = "https",
):
    sequence = get_sequencer(
        ending_number, numeric_step, sequence_file, starting_number
    )
    idox: Idox = Idox(
        sequence,
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
    ] = "{INJECT}",
    sequence_file: Annotated[
        Path,
        typer.Option(
            help="The path to a file containing the ID's to use instead of auto incrementing id's"
        ),
    ] = None,
    request_type: TypeChoices = "GET",
    protocol: ProtocolChoices = "https",
):
    sequence = get_sequencer(
        ending_number, numeric_step, sequence_file, starting_number
    )

    idox: Idox = Idox(
        sequence,
        request_url=url,
        protocol=protocol,
        output_directory=output_directory,
        max_concurrency=max_concurrency,
        injection_point=injection_point,
        request_method=request_type.value,
    )
    main(idox)


def get_sequencer(
    ending_number: int | None,
    numeric_step: int,
    sequence_file: Path | None,
    starting_number: int,
) -> SequenceT:
    if ending_number is not None and sequence_file is not None:
        ctx = click.get_current_context()
        ctx.fail(
            "The parameters ending_number and --sequence-file cannot be used together. "
            "Please remove one and try again."
        )

    if ending_number is not None:
        sequence = NumericSequence(
            ending_number=ending_number,
            starting_number=starting_number,
            jump=numeric_step,
        )

    elif sequence_file is not None:
        if not sequence_file.exists():
            ctx = click.get_current_context()
            ctx.fail(
                "The file provided in --sequence-file does not exist. Please try again."
            )

        sequence = FileSequence(sequence_file)

    else:
        ctx = click.get_current_context()
        ctx.fail("Please provide either an ending_number or --sequence-file parameter.")

    return sequence  # noqa


def main(idox: Idox):
    async def async_main():
        click.secho("Starting Idox\r", nl=False)
        await idox.run()
        click.secho("Enumeration of target has finished\n\n", nl=False)

        output_stats = io.StringIO()
        output_stats.write(s("Statistics by response status code:\n"))
        for k, v in sorted(idox.seen_codes.items()):
            if k < 200:
                # 100's
                fg = "white"
            elif k < 300:
                # 200's
                fg = "green"
            elif k < 400:
                # 300's
                fg = "blue"
            elif k < 500:
                # 400's
                fg = "red"
            else:
                fg = "magenta"

            output_stats.write(s(k, fg=fg))
            output_stats.write(": ")
            output_stats.write(s(v, bold=True))
            output_stats.write("\n")

        output_stats.write(f"\nTotal requests made: ")
        output_stats.write(s(sum(idox.seen_codes.values()), bold=True))

        if idox.seen_errors:
            output_stats.write("\n\nSeen errors:\n")
            for k, v in sorted(idox.seen_errors.items()):
                output_stats.write(f"{k}: ")
                output_stats.write(s(v, bold=True))
                output_stats.write("\n")

            output_stats.write(f"\nTotal errors seen: ")
            output_stats.write(s(sum(idox.seen_errors.values()), bold=True))

        click.echo(output_stats.getvalue())

    asyncio.run(async_main())


if __name__ == "__main__":
    app()
