'''CS2 object of Steam client'''
from .skins import Skins

class CS2:
    def __init__(self, client):
        self._client = client
        
        self.skins = Skins(client)
        #self.orders = Orders(client)
        #self.offers = Offers(client)