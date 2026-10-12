# MRKT Python Client

**A small asynchronous Python client for the MRKT API.**

Use the high-level API modules for common operations, send raw requests through
the shared HTTP session, or process many accounts with a bounded pool of
reusable clients.

<div class="grid cards" markdown>

-   **01 · GET STARTED**

    Install the package and make your first asynchronous request.

    [Installation →](getting-started/installation.md)

-   **02 · AUTHENTICATE**

    Use an existing access token or a Telegram session.

    [Authentication →](getting-started/authentication.md)

-   **03 · MULTI-ACCOUNT**

    Reuse a bounded number of HTTP clients across accounts.

    [MrktPool guide →](guides/pool.md)

-   **04 · EXTEND THE API**

    Send raw requests or construct API classes with your own transport.

    [Raw and standalone usage →](guides/raw-and-standalone.md)

</div>

## Quick start

```bash
python -m pip install mrkts
```

```python
import asyncio

from mrkts import MrktClient


async def main() -> None:
    async with MrktClient(
        token="YOUR_ACCESS_TOKEN",
        preload=("market", "user"),
    ) as client:
        profile = await client.user.me()
        collections = await client.market.gifts.collections()
        print(profile)
        print(collections)


asyncio.run(main())
```

All network methods are asynchronous. The client context initializes and closes
the HTTP session for you.

## What's included

| Module | Access | Examples |
| --- | --- | --- |
| Market | `client.market` | Gifts, orders, offers |
| User | `client.user` | Profile, balance, activities, transactions |
| Steam | `client.steam` | Steam linking and CS2 catalog |
| Pool | `MrktPool` | Bounded concurrent account operations |

The API follows the current behavior of the upstream MRKT service. Its routes
and response payloads may change independently of this package.

## Project links

- [Source code](https://github.com/aiofake/mrkts)
- [Report a bug](https://github.com/aiofake/mrkts/issues)
- [PyPI package](https://pypi.org/project/mrkts/)
