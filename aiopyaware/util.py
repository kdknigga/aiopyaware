import aiohttp
import asyncio
import logging

_LOGGER = logging.getLogger(__name__)

async def rmt_json_to_dict(session: aiohttp.ClientSession, url: str) -> dict:
    """Fetch json from http server and return a dict

    Args:
        session (aiohttp.ClientSession)
        url (str): The full URL that will return the json you want

    Returns:
        dict
    """
    _LOGGER.debug(f"Requesting: {url}")
        
    async with session.get(url) as resp:
        json = await resp.json()
        return json

