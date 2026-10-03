"""Skins object of CS2 client."""

class Skins:
    def __init__(self, client):
        self._client = client

    async def saling(
        self,
        *,
        subTypeInternalNames: list[str],
        modelInternalNames: list[str],
        exteriorInternalNames: list[str],
        finishInternalNames: list[str],
        qualityInternalNames: list[str],
        rarityInternalNames: list[str],
        colorNames: list[str],
        stickerNames: list[str],
        stickerColorNames: list[str],
        keychainNames: list[str],
        collectionNames: list[str],
        teamNames: list[str],
        playerNames: list[str],
        stickerCollectionNames: list[str],
        stickerTeamNames: list[str],
        stickerPlayerNames: list[str],
        tradeItemNames: list[str],
        count: int,
        minFloat: float,
        maxFloat: float,
        returnable: bool,
        luckyBuy: bool,
        hasPattern: bool,
        minPatternIndex: int,
        maxPatternIndex: int,
        hasBlueGem: bool,
        minBlueGem: int,
        maxBlueGem: int,
        hasFade: bool,
        minFade: int,
        maxFade: int,
        minPrice: int,
        maxPrice: int,
        ordering: str,
        lowToHigh: bool,
        query: str,
        hasHighlight: bool,
        cursor: str,
        searchAfterCursor: str,
        excludedIds: list[str],
        removeSelfSales: bool,
        **kwargs
    ):
        payload = {
            'subTypeInternalNames': subTypeInternalNames,
            'modelInternalNames': modelInternalNames,
            'exteriorInternalNames': exteriorInternalNames,
            'finishInternalNames': finishInternalNames,
            'qualityInternalNames': qualityInternalNames,
            'rarityInternalNames': rarityInternalNames,
            'colorNames': colorNames,
            'stickerNames': stickerNames,
            'stickerColorNames': stickerColorNames,
            'keychainNames': keychainNames,
            'collectionNames': collectionNames,
            'teamNames': teamNames,
            'playerNames': playerNames,
            'stickerCollectionNames': stickerCollectionNames,
            'stickerTeamNames': stickerTeamNames,
            'stickerPlayerNames': stickerPlayerNames,
            'tradeItemNames': tradeItemNames,
            'count': count,
            'minFloat': minFloat,
            'maxFloat': maxFloat,
            'returnable': returnable,
            'luckyBuy': luckyBuy,
            'hasPattern': hasPattern,
            'minPatternIndex': minPatternIndex,
            'maxPatternIndex': maxPatternIndex,
            'hasBlueGem': hasBlueGem,
            'minBlueGem': minBlueGem,
            'maxBlueGem': maxBlueGem,
            'hasFade': hasFade,
            'minFade': minFade,
            'maxFade': maxFade,
            'minPrice': minPrice,
            'maxPrice': maxPrice,
            'ordering': ordering,
            'lowToHigh': lowToHigh,
            'query': query,
            'hasHighlight': hasHighlight,
            'cursor': cursor,
            'searchAfterCursor': searchAfterCursor,
            'excludedIds': excludedIds,
            'removeSelfSales': removeSelfSales,
            **kwargs
        }
        payload = {k: v for k, v in payload.items() if v is not None}

        response = await self._client.http.post('steam/trade-items/saling', json=payload)
        response.raise_for_status()
        return await response.json()

    async def feed(
            self,
            *,
            subTypeInternalNames: list[str],
            modelInternalNames: list[str],
            exteriorInternalNames: list[str],
            finishInternalNames: list[str],
            qualityInternalNames: list[str],
            rarityInternalNames: list[str],
            colorNames: list[str],
            collectionNames: list[str],
            teamNames: list[str],
            playerNames: list[str],
            count: int,
            cursor: str,
            stickerNames: list[str],
            keychainNames: list[str],
            tradeItemNames: list[str],
            minFloat: int,
            maxFloat: int,
            returnable: bool,
            luckyBuy: bool,
            hasPattern: bool,
            minPatternIndex: int,
            maxPatternIndex: int,
            hasBlueGem: bool,
            minBlueGem: int,
            maxBlueGem: int,
            hasFade: bool,
            minFade: int,
            maxFade: int,
            minPrice: int,
            maxPrice: int,
            type: list[str],
            ordering: str,
            lowToHigh: bool,
            query: str,
            hasHighlight: bool,
            **kwargs
        ):
            payload = {
                'subTypeInternalNames': subTypeInternalNames,
                'modelInternalNames': modelInternalNames,
                'exteriorInternalNames': exteriorInternalNames,
                'finishInternalNames': finishInternalNames,
                'qualityInternalNames': qualityInternalNames,
                'rarityInternalNames': rarityInternalNames,
                'colorNames': colorNames,
                'collectionNames': collectionNames,
                'teamNames': teamNames,
                'playerNames': playerNames,
                'count': count,
                'cursor': cursor,
                'stickerNames': stickerNames,
                'keychainNames': keychainNames,
                'tradeItemNames': tradeItemNames,
                'minFloat': minFloat,
                'maxFloat': maxFloat,
                'returnable': returnable,
                'luckyBuy': luckyBuy,
                'hasPattern': hasPattern,
                'minPatternIndex': minPatternIndex,
                'maxPatternIndex': maxPatternIndex,
                'hasBlueGem': hasBlueGem,
                'minBlueGem': minBlueGem,
                'maxBlueGem': maxBlueGem,
                'hasFade': hasFade,
                'minFade': minFade,
                'maxFade': maxFade,
                'minPrice': minPrice,
                'maxPrice': maxPrice,
                'type': type,
                'ordering': ordering,
                'lowToHigh': lowToHigh,
                'query': query,
                'hasHighlight': hasHighlight,
                **kwargs
            }
            payload = {k: v for k, v in payload.items() if v is not None}
            
            response = await self._client.http.post('steam/feed', json=payload)
            response.raise_for_status()
            return await response.json()

    async def models(
        self,
        **kwargs
    ):
        response = await self._client.http.get('steam/trade-item-properties/models', params=kwargs)
        response.raise_for_status()
        return await response.json()

    async def variants(
        self,
        **kwargs
    ):
        response = await self._client.http.get('steam/trade-item-properties/variants', params=kwargs)
        response.raise_for_status()
        return await response.json()
    
    async def exteriors(
        self,
        **kwargs
    ):
        response = await self._client.http.get('steam/trade-item-properties/exteriors', params=kwargs)
        response.raise_for_status()
        return await response.json()

    async def rarities(
        self,
        **kwargs
    ):
        response = await self._client.http.get('steam/trade-item-properties/rarities', params=kwargs)
        response.raise_for_status()
        return await response.json()

    async def finishes(
        self,
        modelInternalName: str | None = None,
        **kwargs
    ):
        response = await self._client.http.get('steam/trade-item-properties/finishes', params={"modelInternalName": modelInternalName, **kwargs})
        response.raise_for_status()
        return await response.json()

    async def collections(
        self,
    ):
        response = await self._client.http.get('steam/trade-item-properties/collections')
        response.raise_for_status()
        return await response.json()

    async def types(
        self,
        **kwargs
    ):
        response = await self._client.http.get('steam/trade-item-properties/types', params=kwargs)
        response.raise_for_status()
        return await response.json()

    async def qualities(
        self,
        **kwargs
    ):
        response = await self._client.http.get('steam/trade-item-properties/qualities', params=kwargs)
        response.raise_for_status()
        return await response.json()

    async def item(
        self,
        *,
        steamId: str,
    ):
        response = await self._client.http.get(f'steam/trade-items/item/{steamId}')
        response.raise_for_status()
        return await response.json()

    async def tradeItem(
        self,
        *,
        steamId: str,
        count: int,
        cursor: str,
        minPrice: int,
        maxPrice: int,
        type: list[str],
        ordering: str,
        lowToHigh: bool,
        **kwargs
    ):
        payload = {
            'count': count,
            'cursor': cursor,
            'minPrice': minPrice,
            'maxPrice': maxPrice,
            'type': type,
            'ordering': ordering,
            'lowToHigh': lowToHigh,
            **kwargs
        }
        response = await self._client.http.post(f'steam/feed/trade-item/{steamId}', json=payload)
        response.raise_for_status()
        return await response.json()