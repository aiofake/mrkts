'''Market object of MRKT client'''

from .gifts import Gifts
from .orders import Orders
from .offers import Offers

class MarketClient:
    def __init__(self, client):
        self.gifts = Gifts(client)
        self.orders = Orders(client)
        self.offers = Offers(client)