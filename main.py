import asyncio
import io
from pathlib import Path

import click
from click import style as s

from idox import Idox, NumericSequence


async def main():
    click.secho("Starting Idox\r", nl=False)
    idox: Idox = Idox(
        NumericSequence(ending_number=25),
        request_file_path=Path("data/showcase_url.txt"),
        # request_file_path=Path("data/showcase_json_body.txt"),
        # request_file_path=Path("data/showcase_raw_body.txt"),
    )
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


if __name__ == "__main__":
    asyncio.run(main())
