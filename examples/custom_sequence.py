import asyncio

from idox import Idox, SequenceT


class MySequence(SequenceT):
    def __init__(self):
        self.iter = iter(["T-USER-1A", "T-USER-1B", "T-USER-2A", "T-USER-2B"])


async def main():
    idox: Idox = Idox(MySequence(), request_url="https://blurp.skelmis.co.nz/{INJECT}")
    await idox.run()


if __name__ == "__main__":
    asyncio.run(main())
