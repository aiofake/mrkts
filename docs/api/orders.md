# Orders

Access order methods with `client.market.orders` after preloading `"market"`.

## Browse orders

```python
orders = await client.market.orders.list(
    collectionNames=["Plush Pepe"],
    count=20,
)
```

The listing method accepts collection, model, backdrop, symbol, price, sort,
query, and cursor filters.

## Create an order

```python
created = await client.market.orders.create(
    collectionName="Plush Pepe",
    priceMinNanoTONs=500_000_000,
    priceMaxNanoTONs=1_000_000_000,
    quantity=1,
)
```

This submits an order to the account. Verify price units and parameters before
using it with a real account.

## Manage orders

```python
my_orders = await client.market.orders.getMyOrders(count=20)
top_orders = await client.market.orders.top(collectionName="Plush Pepe")
```

Cancel an order using its ID:

```python
cancelled = await client.market.orders.cancel("ORDER_ID")
```

`cancel()` returns `False` when the server responds with an HTTP error and
returns `True` on success. Other failures may still raise.

## Fill orders and order history

```python
fill_result = await client.market.orders.fill(
    orderId="ORDER_ID",
    giftIds="GIFT_ID",
)
history = await client.market.orders.giftsHistory(limit=20)
```

The current method signature accepts `giftIds` as a string. Check the upstream
API expectations for the number and format of IDs before calling it.
