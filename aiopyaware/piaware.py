import aiohttp
import asyncio
import logging

from .util import *
from .receiver import Receiver

_LOGGER = logging.getLogger(__name__)


class PiAware:
    """A class managing the connection to and state of the piaware device itself."""

    def __init__(self, address: str, session: aiohttp.ClientSession) -> None:
        self._address = address
        self._session = session
        self.status = {}
        self.receivers = {"1090": None, "978": None}

    async def update_status(self) -> None:
        _LOGGER.debug("Updating piaware status")
        self.status = await rmt_json_to_dict(
            self._session, f"{self._address}/status.json"
        )

    async def get_receivers(self) -> None:
        if len(self.status) == 0:
            await self.update_status()

        if "radio" in self.status:
            self.receivers["1090"] = Receiver(
                f"{self._address}/skyaware/data/", self._session
            )

        if "uat_radio" in self.status:
            self.receivers["978"] = Receiver(
                f"{self._address}/skyaware/data-978/", self._session
            )

        await self.update_receivers()

    async def update_receivers(self) -> None:
        for r in self.receivers.values():
            if r:
                await r.update_receiver_data()

    async def get_aircraft(self) -> None:
        for r in self.receivers.values():
            if r:
                await r.get_aircraft()
