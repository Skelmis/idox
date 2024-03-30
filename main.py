import asyncio
from pathlib import Path

from idox import Idox, NumericSequence


async def main():
    idox: Idox = Idox(
        NumericSequence(ending_number=25),
        request_file_path=Path("data/showcase_url.txt"),
        # request_file_path=Path("data/showcase_json_body.txt"),
        # request_file_path=Path("data/showcase_raw_body.txt"),
    )
    await idox.run()


if __name__ == "__main__":
    asyncio.run(main())
