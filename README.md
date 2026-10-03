# MRKT Python Client

An asynchronous Python library for the [MRKT](https://t.me/mrkt) API.
`MrktClient` provides the main transport, while the API is organized into
separate Market, Steam, and User classes. These API classes can be used with
the main client or directly with a custom HTTP transport.

## Features

- Access token and Telegram session authentication
- Market methods for gifts, orders, and offers
- Steam methods, including CS2
- User profile, balance, and transaction methods
- Raw requests through the available HTTP session
- Concurrent multi-account operations with `MrktPool`

## Installation

Python 3.10 or newer is required.

```bash
python -m pip install mrkts
```

The importable module is named `mrkts`.

## Quick Start

The client and its API modules are asynchronous. Provide an access token and
list the modules you need in `preload`:

```python
import asyncio

from mrkts import MrktClient


async def main() -> None:
    async with MrktClient(
        token="YOUR_ACCESS_TOKEN",
        preload=("market", "user"),
    ) as client:
        gifts = await client.market.gifts.collections()
        profile = await client.user.me()
        print(gifts)
        print(profile)


asyncio.run(main())
```

`preload` is empty by default. Available values are `"market"`, `"steam"`, and
`"user"`. Use `client.steam` for Steam methods; CS2 methods are available under
`client.steam.cs2`, for example `client.steam.cs2.skins`.

The HTTP session is created when entering `async with` or calling
`await client.start()`, and is closed when exiting the context. If you do not
use the context manager, make sure to call `await client.close()`.

## Authentication

### Access Token

```python
async with MrktClient(
    token="YOUR_ACCESS_TOKEN",
    preload=("market",),
) as client:
    listings = await client.market.gifts.saling(count=10)
```

### Telegram Session

To authenticate with a Telegram session, install the project dependencies and
provide the session name and the directory containing the session files:

```python
import asyncio

from mrkts import MrktClient


async def main() -> None:
    client = await MrktClient.session(
        "my_telegram_session",
        workdir=".",
        preload=("user",),
    )
    async with client:
        print(await client.user.me())


asyncio.run(main())
```

## API Methods

### Market

```python
async with MrktClient(token="YOUR_ACCESS_TOKEN", preload=("market",)) as client:
    collections = await client.market.gifts.collections()
    listings = await client.market.gifts.saling(
        collectionNames=["Plush Pepe"],
        count=20,
        ordering="Price",
        lowToHigh=True,
    )
    inventory = await client.market.gifts.inventory(isListed=False, count=20)
    orders = await client.market.orders.list(
        collectionNames=["Plush Pepe"],
        count=10,
    )
    activities = await client.market.offers.activities(count=20)
```

`client.market` provides `gifts`, `orders`, and `offers`. Gift methods include
`collections`, `models`, `backdrops`, `saling`, `inventory`, `history`, `feed`,
`buy`, and `sale`.

### User

```python
async with MrktClient(token="YOUR_ACCESS_TOKEN", preload=("user",)) as client:
    profile = await client.user.me()
    balance = await client.user.balance()
    transactions = await client.user.transactions()
```

### Steam / CS2

```python
async with MrktClient(
    token="YOUR_ACCESS_TOKEN",
    preload=("steam", "user"),
) as client:
    steam_link = await client.steam.connect()
    is_connected = await client.steam.connected
    # Use client.steam.cs2.skins to query the CS2 catalog.
```

## Raw HTTP Requests

After `MrktClient` starts, its `http` attribute is an `aiohttp.ClientSession`
configured with the API base URL and authentication headers. Use it to call
endpoints that are not yet covered by the library's API methods:

```python
async with MrktClient(token="YOUR_ACCESS_TOKEN") as client:
    response = await client.http.get("gifts/collections")
    response.raise_for_status()
    collections = await response.json()
    print(collections)
```

For POST requests, pass the request body through `json`:

```python
async with MrktClient(token="YOUR_ACCESS_TOKEN") as client:
    response = await client.http.post(
        "gifts/saling",
        json={"count": 10, "collectionNames": ["Plush Pepe"]},
    )
    response.raise_for_status()
    listings = await response.json()
```

Pass paths relative to the client's base URL:
`https://api.tgmrkt.io/api/v1/`. Raw requests should also be made inside the
client context so that the HTTP session has been initialized.

## Using API Classes Without `preload` or `MrktClient`

With this approach, you are responsible for the base URL, authentication
headers, and closing the HTTP session. To use the built-in authentication and
transport while still creating API classes independently of `preload`, pass
an instance of `MrktClient` to them:

```python
from mrkts import MrktClient
from mrkts.market.gifts import Gifts


async def main() -> None:
    async with MrktClient(token="YOUR_ACCESS_TOKEN") as transport:
        gifts = Gifts(transport)
        print(await gifts.collections())
```

## Multiple Accounts

`MrktPool` runs one coroutine for each client in the pool. Open each client
with `async with` inside the callback:

```python
import asyncio

from mrkts import MrktPool


async def get_balance(client) -> dict:
    async with client as api:
        response = await api.http.get("balance")
        response.raise_for_status()
        return await response.json()


async def main() -> None:
    async with MrktPool(tokens=["TOKEN_1", "TOKEN_2"]) as pool:
        results = await pool.map(get_balance, concurrency=2)
        for result in results:
            if isinstance(result, Exception):
                print(f"Request failed: {result}")
            else:
                print(result)


asyncio.run(main())
```

To create a pool from Telegram sessions, use
`await MrktPool.from_sessions(...)`.

## API Structure

```text
MrktClient
├── market
│   ├── gifts
│   ├── orders
│   └── offers
├── steam
│   └── cs2
│       ├── skins
│       ├── orders
│       └── offers
└── user
```

Specify `"market"`, `"steam"`, or `"user"` in `preload` to access the
corresponding module through `MrktClient`.
