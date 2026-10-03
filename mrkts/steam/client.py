'''Steam object of MRKT client'''
from .cs2.client import CS2

class SteamClient:
    def __init__(self, client):
        self._client = client
        
        self.cs2 = CS2(client)
        #self.dota2 = Dota2(client)

    async def connect(
        self, 
        *,
        languageCode = "en",
        redirectUri = "https://www.mrkt.land/steam-link?return=https%3A%2F%2Ft.me%2Fmrkt%2Fapp%3Fstartapp%3Dopensteamlinked",
        open = False,
    ):
        from webbrowser import open_new_tab
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
    
    @property
    async def connected(self) -> bool:
        user = await self._client.user.me()
        return True if user.get("steamUser") else False

    @property
    async def tradeLink(self) -> str:
        user = await self._client.user.me()
        return user.get("steamUser", {}).get("tradeLink", "")