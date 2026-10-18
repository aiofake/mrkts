'''User-related operations for the MRKT client'''

from typing import *

class User:
    def __init__(self, client):
        self._client = client

    async def me(self):
        response = await self._client.http.get("me")
        response.raise_for_status()
        return await response.json()
    
    async def balance(self):
        response = await self._client.http.get("balance")
        response.raise_for_status()
        return await response.json()

    async def withdraw(self, nanoTONs: int, walletAddress: str):
        response = await self._client.http.post("wallet/withdraw/tons", json={"nanoTONs": nanoTONs, "wallet": walletAddress})
        response.raise_for_status()
        return await response.json()

    async def activities(self, *, count: int = 20, filters: list = ["Offers", "ChannelOffers", "GiftsCollectionOffers"]):
            response = await self._client.http.get("activities/with-totals", params={"count": count, "isActive": "true", "filters": filters})
            response.raise_for_status()
            return await response.json()
    
    async def transactions(self):
        response = await self._client.http.get("transactions/await")
        response.raise_for_status()
        return await response.json()

    async def configs(self):
            response = await self._client.http.get("configs")
            response.raise_for_status()
            return await response.json()
    
    async def get_locale(self, locale: str):
        response = await self._client.http.get("get_locale", json={"locale": locale})
        response.raise_for_status()
        return await response.json()

    async def tasks(self):
        response = await self._client.http.get("tasks")
        response.raise_for_status()
        return await response.json()

    async def new_tasks(self):
        response = await self._client.http.get("tasks/new")
        response.raise_for_status()
        return await response.json()
    
    async def autoWithdraw(self, nanoTONs: int | None = None):
        """Withdraw the available balance to the account's saved TON wallet."""
        if nanoTONs is None:
            balance = await self.balance()
            balance_data = (
                balance.get("balance") if isinstance(balance, dict) else None
            )
            nanoTONs = (
                balance_data.get("hard")
                if isinstance(balance_data, dict)
                else None
            )
            if nanoTONs is None:
                raise ValueError(
                    "Account response does not contain a withdrawable balance"
                )

        profile = await self.me()
        wallet_data = profile.get("wallet") if isinstance(profile, dict) else None
        wallet = wallet_data.get("ton") if isinstance(wallet_data, dict) else None
        if not wallet:
            raise ValueError("Account response does not contain a saved TON wallet")

        return await self.withdraw(nanoTONs, wallet)