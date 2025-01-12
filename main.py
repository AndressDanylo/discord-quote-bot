import discord
import config
from image_creator import create_quote_image

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
    fetched_message = await interaction.channel.fetch_message(get_message_id(message_link))
    file_path = await create_quote_image(fetched_message.content, fetched_message.author.display_name, fetched_message.author.avatar.url, "media/image.png")
    print(file_path)
    with open(file_path, "rb") as file:
        await fetched_message.channel.send(file=discord.File(file, filename="image.png"))
    
    await interaction.response.send_message('"' + fetched_message.content + '"')


# TODO help command
@tree.command(name="help", description="Help")
async def help(interaction):
    await interaction.response.send_message("Help")


client.run(config.TOKEN)
