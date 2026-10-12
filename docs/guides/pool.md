# Multi-account pool

`MrktPool` runs a callback for each account while reusing a bounded number of
worker clients. This avoids creating an HTTP session for every account.

```python
import asyncio

from mrkts import MrktPool


async def get_balance(client):
    return await client.user.balance()


async def main() -> None:
    async with MrktPool(
        tokens=["TOKEN_1", "TOKEN_2", "TOKEN_3"],
        preload=("user",),
        concurrency=2,
    ) as pool:
        results = await pool.map(get_balance)

    for result in results:
        if isinstance(result, Exception):
            print(f"Account failed: {result}")
        else:
            print(result)


asyncio.run(main())
```

## Pool options

| Option | Description |
| --- | --- |
| `tokens` | Access tokens, one per account |
| `sessions` | Telegram session names; choose one of `tokens` or `sessions` |
| `workdir` | Directory containing Telegram session files |
| `preload` | API modules each worker needs |
| `concurrency` | Maximum number of reusable workers (default: `5`) |
| `proxy` | Optional proxy used by worker clients |
| `unlimited` | Create a worker per account instead of bounding workers |

For Telegram sessions, the `from_sessions` classmethod provides a clear entry
point:

```python
pool = await MrktPool.from_sessions(
    ["account_a", "account_b"],
    workdir="./sessions",
    preload=("user",),
    concurrency=2,
)
```

## Result behavior

- Results preserve the input account order.
- A callback exception is returned in that account's result slot; it does not
  discard successful results from other accounts.
- Within an open pool context, repeated `map()` calls reuse worker clients.
- Exiting the pool context closes its worker sessions.
- Without a pool context, `map()` starts workers and closes them when that call
  completes.

```python
async with MrktPool(tokens=tokens, preload=("user",), concurrency=4) as pool:
    balances = await pool.map(get_balance)
    profiles = await pool.map(lambda client: client.user.me())
```

Callbacks should await all work before returning. Do not retain a worker client
or launch background requests that continue after the callback finishes: the
same worker can be assigned to another account.

The results list necessarily grows with the number of accounts. `concurrency`
bounds active workers and concurrent requests, not the final result list.
`unlimited=True` can use substantially more memory and should only be used
when the account count is small.

## Concurrency per call

Override the pool default for a particular operation:

```python
results = await pool.map(get_balance, concurrency=1)
```
