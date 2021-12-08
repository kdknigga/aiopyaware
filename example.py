import asyncio
import aiohttp
import logging

from pprint import pprint
from aiopyaware.piaware import PiAware

logging.basicConfig(level=logging.DEBUG)

async def main():
    async with aiohttp.ClientSession() as session:
        await run(session)

async def run(session):
    pa = PiAware("http://piaware", session)
    
    await pa.update_status()
    await pa.get_receivers()
    await pa.update_receivers()
    await pa.get_aircraft()
    
    #pprint(pa.status)
    
    status = None
    
    for i, r in pa.receivers.items():
        if i == '1090':
            status = pa.status['radio']['status']
        elif i == '978':
            status = pa.status['uat_radio']['status']
        else:
            raise ValueError(f"Unknown radio freqency")
    
        print(f"{i} MHz Radio:")
        print("  - status: ", status)
        print("  - version: ", r.version)
        print("  - aircraft count: ", str(len(r.aircraft)))
        print("  - aircraft list:")
        for ac in r.aircraft.values():
            text = f"callsign: {ac.get('flight')} "
            text += f"altitude: {ac.get('alt_baro')} "
            text += f"groundspeed: {ac.get('gs')} "
            text += f"track: {ac.get('track')} "
            print(f"    - {ac['hex']}")
            print(f"       {text}")
    

try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass