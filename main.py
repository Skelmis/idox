import asyncio

from idox import Idox


async def main():
    idox: Idox = Idox()
    await idox.run()


if __name__ == "__main__":
    asyncio.run(main())
