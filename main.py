import discord
import config

# bot setup
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# functionality
@client.event
async def on_message(message):
    if message. author == client.user:
        return
    else:
        await message.channel.send(message.content)

client.run(config.TOKEN)