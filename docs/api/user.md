# User

Access user methods with `client.user` after preloading `"user"`.

```python
async with MrktClient(token="YOUR_ACCESS_TOKEN", preload=("user",)) as client:
    profile = await client.user.me()
    balance = await client.user.balance()
    transactions = await client.user.transactions()
```

## Activities

The `filters` argument is passed to the upstream activities endpoint:

```python
orders = await client.user.activities(
    count=20,
    filters=["Orders"],
)
```

The default filters currently include `Offers`, `ChannelOffers`, and
`GiftsCollectionOffers`. Endpoint availability and accepted filters are
controlled by the upstream service.

## Other methods

```python
configs = await client.user.configs()
tasks = await client.user.tasks()
new_tasks = await client.user.new_tasks()
locale = await client.user.get_locale("en")
```

## Withdrawals

`withdraw()` sends a withdrawal request. Use it only after confirming the
amount and destination wallet:

```python
result = await client.user.withdraw(
    nanoTONs=1_000_000_000,
    walletAddress="YOUR_WALLET_ADDRESS",
)
```

Amounts are passed in nanoTONs. Never embed real credentials or wallet
addresses in public examples or commit history.
