import discord
from config import Token


class Client(discord.Client):
   async def on_ready(self):
        print(f'logged on as {self.user}!')

intents = discord.Intents.default()
intents.message_content = True

client = Client(intents=intents)
client.run('MTMxMDc3Njk3MjU3MzU0MDQyMw.GO3xW_.ZfLpcNGq41bLl39RszPINnFnugtCYAdv0sboOw')
