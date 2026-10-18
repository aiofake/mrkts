import asyncio
import os

from mrkts import MrktClient
from mrkts.workflows import fetch_feed


async def main() -> None:
    async with MrktClient(
        token=os.environ["MRKT_TOKEN"],
        preload=("market",),
    ) as client:
        async for response in client.exec(
            fetch_feed,
            interval=2.0,
            count=20,
        ):
            print(response)


if __name__ == "__main__":
    asyncio.run(main())
