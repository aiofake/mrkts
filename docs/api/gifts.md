# Gifts

Access gifts through `client.market.gifts` after preloading `"market"`.
Examples below use an access-token client:

```python
async with MrktClient(token="YOUR_ACCESS_TOKEN", preload=("market",)) as client:
    gifts = client.market.gifts
    collections = await gifts.collections()
```

## Browse listings

```python
listings = await client.market.gifts.saling(
    collectionNames=["Plush Pepe"],
    count=20,
    ordering="Price",
    lowToHigh=True,
)
```

`saling()` supports filters including collection, model, backdrop, symbol,
number, price range, gift type, and transferability. It also accepts additional
keyword values that are included in the request payload.

## Inventory

```python
inventory = await client.market.gifts.inventory(
    isListed=False,
    collectionNames=["Plush Pepe"],
    count=20,
)
```

## Catalog and history

```python
collections = await client.market.gifts.collections()
models = await client.market.gifts.models(["Plush Pepe"])
backdrops = await client.market.gifts.backdrops(["Plush Pepe"])
history = await client.market.gifts.history(limit=20)
```

## Buying and listing

These methods perform account actions. Check the selected IDs and prices before
calling them.

```python
result = await client.market.gifts.buy(ids=["GIFT_ID"])
listing = await client.market.gifts.sale(ids=["GIFT_ID"], price=1_000_000_000)
```

`price` is sent as provided by the caller; confirm the API's expected units for
your use case before placing a listing.

## Live feed

```python
feed = await client.market.gifts.feed(
    collectionNames=["Plush Pepe"],
    count=20,
    ordering="Latest",
)
```

Responses are decoded JSON payloads returned by the upstream service. Consult
the live API response when relying on a particular response field.
