# Client lifecycle

`MrktClient` owns the authenticated `aiohttp.ClientSession`. Enter the client
context before making requests and let it close the session when finished.

```python
import asyncio

from mrkts import MrktClient


async def main() -> None:
    async with MrktClient(
        token="YOUR_ACCESS_TOKEN",
        preload=("market", "user", "steam"),
    ) as client:
        me = await client.user.me()
        inventory = await client.market.gifts.inventory(count=10)
        print(me, inventory)


asyncio.run(main())
```

## Preloaded modules

Modules are not attached unless requested. `preload` accepts any combination
of:

| Name | Available as |
| --- | --- |
| `"market"` | `client.market` |
| `"steam"` | `client.steam` |
| `"user"` | `client.user` |

```python
client = MrktClient(token="YOUR_ACCESS_TOKEN", preload=("market", "user"))
```

If a required module was not preloaded, create a new client with the desired
`preload` values.

## Explicit lifecycle

Context managers are recommended. When a context manager is not suitable,
start and close the client explicitly:

```python
client = MrktClient(token="YOUR_ACCESS_TOKEN", preload=("user",))
await client.start()
try:
    profile = await client.user.me()
finally:
    await client.close()
```

Starting a client with `session=...` refreshes its access token from that
Telegram session. The session-based helper is described in
[Authentication](authentication.md).

## Object layout

```text
MrktClient
├── market
│   ├── gifts
│   ├── orders
│   └── offers
├── steam
│   └── cs2
│       └── skins
└── user
```

See the [API reference](../api/gifts.md) for module-specific examples.
