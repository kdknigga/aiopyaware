import aiohttp
import asyncio
import logging

from .util import *

_LOGGER = logging.getLogger(__name__)

class Receiver():
    """A class to represent an ADS-B receiver radio
    """
    
    def __init__(self, data_url: str, session: aiohttp.ClientSession) -> None:
        """Create a new Receiver object

        Args:
            data_url (str): Base URL to find the json files for this receiver (perhaps "http://piaware/skyaware/data/")
            session (aiohttp.ClientSession)
        """
        
        self._data_url = data_url
        self._session = session
        self.version = None
        self.refresh_interval = None
        self.latitude = None
        self.longitude = None
        self.aircraft = dict()

    
    async def update_receiver_data(self) -> None:
        _LOGGER.debug("Updating receiver data")
        data = await rmt_json_to_dict(self._session, f"{self._data_url}/receiver.json")
        self.version = data['version']
        self.refresh_interval = data['refresh']
        self.latitude = data['lat']
        self.longitude = data['lon']
    
    
    async def get_aircraft(self) -> None:
        _LOGGER.debug("Fetching list of aircraft")
        data = await rmt_json_to_dict(self._session, f"{self._data_url}/aircraft.json")
        self.aircraft = { a['hex']: a for a in data['aircraft'] }
    