# coc_connection_manager.py
import coc
from dotenv import load_dotenv
import os

class COCConnectionManager:
    def __init__(self):
        load_dotenv('bot/secret/coc.env')
        self.email = os.getenv("EMAIL")
        self.password = os.getenv("PASSWORD")
        self.client = None

    def create_client(self):
        if not (self.email and self.password):
            raise ValueError("EMAIL and PASSWORD must be defined in the environment.")
        
        self.client = coc.EventsClient(key_names="DeathZone Legend Test Bot")
        return self.client

    async def login(self):
        if self.client is None:
            raise Exception("Client is not initialized, call create_client first.")
        
        try:
            await self.client.login(self.email, self.password)
            print("Logged into Clash of Clans successfully.")
        except Exception as error:
            print(f"Failed to login to Clash of Clans: {error}")
            raise

    async def logout(self):
        if self.client is not None:
            await self.client.close()
            print("Logged out of Clash of Clans.")