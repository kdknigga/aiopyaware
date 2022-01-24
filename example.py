import argparse
import asyncio
import aiohttp
import locale
import logging

from pprint import pprint
from aiopyaware.piaware import PiAware

locale.setlocale(locale.LC_ALL, "")


async def main(closest=None, refresh=None):
    async with aiohttp.ClientSession() as session:
        pa = PiAware("http://piaware", session)
        await pa.get_receivers()

        r_refresh = max([r.refresh_interval for r in pa.receivers.values()])/1000

        if refresh:
            if r_refresh > refresh:
                refresh = r_refresh
                logging.warning(
                    f"Overriding refresh interval setting with larger value provided by the PiAware: {refresh}"
                )

            while True:
                if closest:
                    await show_closest(pa, closest)
                else:
                    await dump_status(pa)

                print("")
                await asyncio.sleep(refresh)
        else:
            if closest:
                await show_closest(pa, closest)
            else:
                await dump_status(pa)


def _print_ac_list(aircraft_list: list) -> None:
    for ac in aircraft_list:
        distance = ac.get("distance")
        alt = ac.get("alt_baro")
        gs = ac.get("gs")
        track = ac.get("track")

        text = f"callsign: {ac.get('flight')} "

        if distance:
            text += f"distance: {distance:.1f}nm "
        else:
            text += f"distance: Unknown "

        if alt:
            text += f"altitude: {alt:n}ft "
        else:
            text += f"altitude: Unknown "

        if gs:
            text += f"groundspeed: {ac.get('gs')}kt "
        else:
            text += f"groundspeed: Unknown "

        if track:
            text += f"track: {ac.get('track')}° "
        else:
            text += f"track: Unknown "

        print(f"    - {ac['hex']}")
        print(f"       {text}")


def _filter_aircraft(pa: PiAware, seen: int = 60) -> dict:
    for i, r in pa.receivers.items():
        for ac in r.aircraft.values():
            if "distance" in ac and ac["distance"]:
                if "seen" in ac and ac["seen"] < 60:
                    yield ac


async def show_closest(pa: PiAware, closest: int):
    await pa.get_aircraft()
    sorted_aircraft = sorted(_filter_aircraft(pa), key=lambda i: i["distance"])

    _print_ac_list(sorted_aircraft[:closest])


async def dump_status(pa: PiAware):
    await pa.update_status()
    await pa.update_receivers()
    await pa.get_aircraft()

    status = None

    for i, r in pa.receivers.items():
        if i == "1090":
            status = pa.status["radio"]["status"]
        elif i == "978":
            status = pa.status["uat_radio"]["status"]
        else:
            raise ValueError(f"Unknown radio freqency")

        print(f"{i} MHz Radio:")
        print("  - status: ", status)
        print("  - version: ", r.version)
        print("  - aircraft count: ", str(len(r.aircraft)))
        print("  - aircraft list:")
        _print_ac_list(r.aircraft.values())


parser = argparse.ArgumentParser()
parser.add_argument(
    "-c", "--closest", help="Display the X closest aircraft to the receiver", type=int
)
parser.add_argument(
    "-i",
    "--refresh-interval",
    help="The time to wait between refreshes.  If this number is smaller than the refresh interval provided by the PiAware, the larger interval will be used.",
    type=int,
)
parser.add_argument(
    "-l",
    "--log-level",
    help="Amount of logging desired.  (default: %(default)s)",
    choices=["debug", "info", "warning", "error", "critical"],
    default="warning",
)
args = parser.parse_args()

log_level_map = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}
logging.basicConfig(level=log_level_map[args.log_level])

try:
    asyncio.run(main(closest=args.closest, refresh=args.refresh_interval))
except KeyboardInterrupt:
    pass
