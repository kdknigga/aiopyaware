import asyncio
import aiohttp
import logging
from pprint import pprint as pp

from aiopyaware.piaware import PiAware

logging.basicConfig(level=logging.DEBUG)

async def main():
    async with aiohttp.ClientSession() as session:
        await run(session)

async def run(session):
    pa = PiAware("http://piaware", session)
    
    await pa.update_status()
    
    #pp(pa.status)
    print(f"1090 Radio Status: {pa.status['radio']['status']}")
    print(f"978 Radio Status: {pa.status['uat_radio']['status']}")


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass