import aiohttp
import asyncio
import logging

_LOGGER = logging.getLogger(__name__)

class PiAware():
    """A class managing the connection to and state of the piaware device itself.
    """
    
    def __init__(self, address: str, session: aiohttp.ClientSession) -> None:
        self._address = address
        self._session = session
        self.status = {}

    
    async def _get_json(self, path: str) -> dict:
        url = f"{self._address}/{path}"
        _LOGGER.debug(f"Requesting: {url}")
        
        async with self._session.get(url) as resp:
            json = await resp.json()
            return json
        
    async def update_status(self) -> None:
        self.status = await self._get_json("status.json")
