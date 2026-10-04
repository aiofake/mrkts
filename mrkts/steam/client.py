'''Steam object of MRKT client'''

from .cs2.client import CS2
from webbrowser import open_new_tab

class SteamClient:
    def __init__(self, client):
        self._client = client
        
        self.cs2 = CS2(client)
        #self.dota2 = Dota2(client)

    async def connect(
        self, 
        *,
        languageCode: str = "en",
        redirectUri: str = "https://www.mrkt.land/steam-link?return=https%3A%2F%2Ft.me%2Fmrkt%2Fapp%3Fstartapp%3Dopensteamlinked",
        open: bool = False,
    ):
        payload = {
            'redirectUri': redirectUri,
            'languageCode': languageCode
        }
        response = await self._client.http.post('auth/link/sign-in-link', json=payload)
        response.raise_for_status()
        return await response.json() if not open else open_new_tab((await response.json()).get('url'))

    async def disconnect(
        self,
    ):
        response = await self._client.http.post('auth/disconnect/steam')
        response.raise_for_status()
        return await response.json()
    
    async def connected(self) -> bool:
        user = await self._client.user.me()
        return bool(user.get("steamUser"))

    async def setTradeLink(self, tradeLink: str):
        try:
            payload = {
                "tradeLink": tradeLink
            }
            response = await self._client.http.post('steam/trade-link', json=payload)
            response.raise_for_status()
            return True
        except Exception as e: raise e
    
    async def tradeLink(self) -> str:
        user = await self._client.user.me()
        return user.get("steamUser", {}).get("tradeLink", "")

    async def getTradeLink(self, open: bool = False):
        user = await self._client.user.me()
        redirectTo = f"https://steamcommunity.com/profiles/{user.get('steamUser', {}).get('id')}/tradeoffers/privacy#trade_offer_access_url"
        return redirectTo if not open else open_new_tab(redirectTo)