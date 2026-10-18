# Reusable workflows

A workflow is a plain function that accepts `MrktClient` as its first
argument. `client.exec()` invokes it and returns its result, so it works with
both coroutines and async iterators.

## Poll the gifts feed

`fetch_feed()` polls immediately, then waits for the requested interval
between responses:

```python
from mrkts import MrktClient
from mrkts.workflows import fetch_feed


async with MrktClient(
    token="YOUR_ACCESS_TOKEN",
    preload=("market",),
) as client:
    async for response in client.exec(
        fetch_feed,
        interval=2.0,
        count=20,
        collectionNames=["Plush Pepe"],
    ):
        print(response)
```

The interval must be finite and greater than zero. Network and API errors
propagate to the caller, and each response is yielded without reshaping or
deduplication. Close the iterator when finished. The client context owns the
HTTP session.

## Define a workflow

Pass any function that accepts a client first. The function's return value is
returned unchanged:

```python
async def get_balance(client):
    return await client.user.balance()


balance = await client.exec(get_balance)
```

Use `MrktPool.map()` for the separate case of running a callback across
multiple accounts.
