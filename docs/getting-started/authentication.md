# Authentication

`MrktClient` accepts either an MRKT access token or a Telegram session. Keep
credentials out of source control and avoid printing tokens or authenticated
request headers.

## Access token

Pass an access token directly:

```python
from mrkts import MrktClient


async with MrktClient(
    token="YOUR_ACCESS_TOKEN",
    preload=("user",),
) as client:
    print(await client.user.me())
```

## Telegram session

The package uses Pyrogram to read the Telegram session and obtain an MRKT
token. The session file must already exist in `workdir`.

```python
from mrkts import MrktClient


async def main() -> None:
    client = await MrktClient.session(
        "my_telegram_session",
        workdir="./sessions",
        preload=("user",),
    )
    async with client:
        print(await client.user.me())
```

The session name is passed without the session-file extension. Protect both
the session file and its directory like a password.

## Telegram Web App init data

If your application already has Telegram Web App `init_data`, it can be
exchanged for an access token with `get_token`:

```python
from mrkts.auth import get_token
from mrkts import MrktClient


async def main() -> None:
    token = await get_token("TELEGRAM_WEB_APP_INIT_DATA")
    async with MrktClient(token=token, preload=("user",)) as client:
        print(await client.user.me())
```

`MrktClient.init_data(...)` also creates a client from init data.

## Proxy

Pass a proxy URL to `MrktClient` or `MrktClient.session`:

```python
client = MrktClient(
    token="YOUR_ACCESS_TOKEN",
    proxy="http://127.0.0.1:8080",
    preload=("user",),
)
```

For Telegram sessions, use a proxy format supported by Pyrogram, such as
`socks5://host:port`.
