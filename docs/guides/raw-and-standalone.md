# Raw requests and standalone API classes

Use a high-level method when one is available. Raw requests are useful for API
routes that the library does not wrap yet.

## Raw request through `MrktClient`

The client HTTP session is available as `client.http` after the client starts.
Paths are relative to `https://api.tgmrkt.io/api/v1/`.

```python
from mrkts import MrktClient


async def main() -> None:
    async with MrktClient(token="YOUR_ACCESS_TOKEN") as client:
        response = await client.http.get("gifts/collections")
        response.raise_for_status()
        collections = await response.json()
        print(collections)
```

POST example:

```python
async with MrktClient(token="YOUR_ACCESS_TOKEN") as client:
    response = await client.http.post(
        "gifts/saling",
        json={"count": 10, "collectionNames": ["Plush Pepe"]},
    )
    response.raise_for_status()
    listings = await response.json()
```

`raise_for_status()` makes unsuccessful HTTP responses explicit. Handle
`aiohttp.ClientResponseError` at the application boundary if you need custom
retry or reporting behavior.

## Use an API class with `MrktClient` transport

The module classes can be constructed directly when you want to choose exactly
which wrapper to use, without `preload`:

```python
from mrkts import MrktClient
from mrkts.market.gifts import Gifts


async def main() -> None:
    async with MrktClient(token="YOUR_ACCESS_TOKEN") as transport:
        gifts = Gifts(transport)
        collections = await gifts.collections()
        print(collections)
```

## Use an API class with your own transport

The API classes expect a client-like object with an `.http` attribute. This
lets you supply your own `aiohttp.ClientSession` and manage its lifecycle:

```python
from types import SimpleNamespace

from aiohttp import ClientSession
from mrkts.market.gifts import Gifts


async def main() -> None:
    headers = {"cookie": "access_token=YOUR_ACCESS_TOKEN"}
    async with ClientSession(
        base_url="https://api.tgmrkt.io/api/v1/",
        headers=headers,
    ) as session:
        transport = SimpleNamespace(http=session)
        gifts = Gifts(transport)
        print(await gifts.collections())
```

This approach makes you responsible for authentication headers, base URL,
timeouts, proxy configuration, and session cleanup. The same pattern applies
to `Orders`, `Offers`, `User`, and other API classes; check each class's
constructor and required client attributes.
