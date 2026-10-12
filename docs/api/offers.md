# Offers

Access offer methods with `client.market.offers` after preloading `"market"`.

## Create an offer

```python
result = await client.market.offers.create(
    price=1_000_000_000,
    giftSaleId="GIFT_SALE_ID",
)
```

## Find or cancel offers

```python
offers = await client.market.offers.myOffersByGift("GIFT_ID", count=20)
result = await client.market.offers.cancel("OFFER_ID")
```

Creating and cancelling offers changes account state. Validate the target IDs
and amounts before sending these requests.
