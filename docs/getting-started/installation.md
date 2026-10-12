# Installation

## Requirements

- Python 3.10 or newer
- An MRKT access token, or a Pyrogram-compatible Telegram session

Install the package from PyPI:

```bash
python -m pip install mrkts
```

The distribution is named `mrkts`, and it is imported as `mrkts`.

## Verify the installation

```bash
python -c "from mrkts import MrktClient, MrktPool; print('mrkts is ready')"
```

## Development install

Clone the [GitHub repository](https://github.com/aiofake/mrkts) and install it
in editable mode:

```bash
git clone https://github.com/aiofake/mrkts.git
cd mrkts
python -m pip install -e .
```

## Next steps

- [Authenticate with an access token or Telegram session](authentication.md)
- [Create and manage a client](client.md)
- [Use a pool for multiple accounts](../guides/pool.md)
