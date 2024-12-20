import asyncio
import logging
from typing import AsyncGenerator

import coc
from coc import Client
from dotenv import load_dotenv
import os

# Laden der .env Datei
load_dotenv('bot/secret/coc.env')

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
KEY_NAMES = os.getenv('KEY_NAMES').split(",")  # API-Schlüssel als Liste laden

# logging
logging.basicConfig(level=logging.WARNING) # dies dann wieder auf info oder debug setzen
logger = logging.getLogger("coc.http")
logger.setLevel(logging.INFO)


class AbstractClient:
    """Class holding the async generator used to get the client and login on demand"""

    def __init__(self):
        self.__async_gen = self.__yield_client()  # create the async generator
        self.lock = asyncio.Lock()

    async def __yield_client(self) -> AsyncGenerator[coc.Client, None]:
        """Get the async generator which always yields the client"""
        async with coc.Client(loop=asyncio.get_event_loop()) as client:
            await client.login(EMAIL, PASSWORD)  # be aware that hard coding credentials is bad practice!
            while True:
                try:
                    yield client
                except GeneratorExit:
                    break

    async def get_client(self) -> Client:
        """Get the actual logged in client"""
        async with self.lock:
            if not hasattr(self, '__async_gen') and not hasattr(self, '_AbstractClient__async_gen'):
                self.__async_gen = self.__yield_client()  # create async generator if needed
            coc_client = await self.__async_gen.__anext__()
            return coc_client

    @property
    async def client(self) -> Client:
        """Get the actual logged in client"""
        async with self.lock:
            if not hasattr(self, '__async_gen') and not hasattr(self, '_AbstractClient__async_gen'):
                self.__async_gen = self.__yield_client()  # create async generator if needed
            coc_client = await self.__async_gen.__anext__()
            return coc_client

    async def shutdown(self):
        """Log out and close the ClientSession"""
        await self.__async_gen.aclose()


abstractClient = AbstractClient()
