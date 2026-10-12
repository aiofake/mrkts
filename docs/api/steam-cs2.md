# Steam and CS2

Preload `"steam"` to access Steam linking helpers and the CS2 namespace:

```python
async with MrktClient(
    token="YOUR_ACCESS_TOKEN",
    preload=("steam", "user"),
) as client:
    link = await client.steam.connect()
    skins = client.steam.cs2.skins
```

## Steam account

```python
result = await client.steam.connect()
trade_link = await client.steam.tradeLink()
await client.steam.setTradeLink("YOUR_STEAM_TRADE_LINK")
```

`connect(open=True)` and `getTradeLink(open=True)` open a browser window. Their
default behavior is to return the generated URL.

To disconnect a linked Steam account:

```python
result = await client.steam.disconnect()
```

## CS2 skin listings

`client.steam.cs2.skins.saling(...)` submits a set of catalog filters to the
CS2 trade-items endpoint. The current method requires its filter parameters,
including list filters, price range, count, ordering, and cursor values.

```python
skins = await client.steam.cs2.skins.saling(
    subTypeInternalNames=[],
    modelInternalNames=[],
    exteriorInternalNames=[],
    finishInternalNames=[],
    qualityInternalNames=[],
    rarityInternalNames=[],
    colorNames=[],
    stickerNames=[],
    stickerColorNames=[],
    keychainNames=[],
    collectionNames=[],
    teamNames=[],
    playerNames=[],
    stickerCollectionNames=[],
    stickerTeamNames=[],
    stickerPlayerNames=[],
    tradeItemNames=[],
    count=20,
    minFloat=0.0,
    maxFloat=1.0,
    returnable=False,
    luckyBuy=False,
    hasPattern=False,
    minPatternIndex=0,
    maxPatternIndex=0,
    hasBlueGem=False,
    minBlueGem=0,
    maxBlueGem=0,
    hasFade=False,
    minFade=0,
    maxFade=0,
    minPrice=0,
    maxPrice=0,
    ordering="Price",
    lowToHigh=True,
    query="",
    hasHighlight=False,
    cursor="",
    searchAfterCursor="",
    excludedIds=[],
    removeSelfSales=False,
)
```

The filter names and payload shape mirror the current library implementation.
The API may require values or support options differently as it evolves.
