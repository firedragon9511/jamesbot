from typing import Any
import discord
from discord.flags import Intents
from command_handler import CommandHandler

class JamesBotClient(discord.Client):
    def __init__(self, *, intents: Intents, **options: Any) -> None:
        super().__init__(intents=intents, **options)

        self.command_handler = CommandHandler(self)
    
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
        await self.command_handler.handle(message)

    async def on_member_join(self, member: discord.Member):
        print(f'Member join {member.name}')
        #self.command_handler.handle_welcome(member)

            

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = JamesBotClient(intents=intents)
client.run('MTE3NjI2NjA3MTQyMzA2MjA0Ng.G8rpI9.Ig1Bd5Hy-jdm3iNv9FwDyt5kFj8alZwA7WLY-U')