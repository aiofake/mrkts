# FAQ

## Is the library synchronous?

No. Network operations are async methods and must be awaited from an
`async def` function.

## Do I need to preload every module?

No. Preload only modules used by that client. Supported values are `"market"`,
`"steam"`, and `"user"`.

## How do I close the HTTP session?

Prefer `async with MrktClient(...)`. Otherwise pair `await client.start()` with
`await client.close()` in a `finally` block.

## Does `MrktPool.map()` keep one HTTP session per account?

By default, no. It creates at most the configured number of reusable workers
and assigns accounts to those workers. `unlimited=True` opts into one worker
per account.

## Why did an endpoint return an HTTP error?

The library sends requests to the upstream MRKT API, so route availability,
authentication rules, filters, and response shapes are ultimately controlled
by that service. Check the exception and current API behavior; a wrapper method
does not guarantee that an upstream route is currently available.

## How do I make a request not implemented by the library?

Use the initialized `client.http` session as shown in
[Raw requests and standalone API classes](guides/raw-and-standalone.md).

## Where should I report an issue?

Open a ticket on the [GitHub issue tracker](https://github.com/aiofake/mrkts/issues).
