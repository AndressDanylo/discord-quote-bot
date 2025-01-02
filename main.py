import discord
import config

# bot setup
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

# functionality
@client.event
async def on_ready():
    # sync commands globally
    await tree.sync()
    print(f'We have logged in as {client.user} and synced commands.')


def get_message_id(link):
    # gets discord message id from link(https://discord.com/channels/{guild id}/{channel id}/{message id})
    return link.split("/")[-1]


@tree.command(name="quote", description="Converts the message into a customized quote image")
@discord.app_commands.describe(message_link="Link to the message you want to quote")
async def quote(interaction, message_link: str):
    try:
        fetched_message = await interaction.channel.fetch_message(get_message_id(message_link))
    except Exception:
        await interaction.response.send_message("This is not a valid link")
    
    await interaction.response.send_message('"' + fetched_message.content + '"')

client.run(config.TOKEN)
