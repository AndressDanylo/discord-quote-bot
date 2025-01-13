import discord
import config
from image_creator import create_quote_image

# bot setup
intents = discord.Intents.all()
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


@tree.context_menu(name="quote")
@discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def quote(interaction, message: discord.Message):
    file_path = await create_quote_image(message.content, message.author.display_name, message.author.name, message.created_at, message.author.avatar.url, "media/image.png")
    with open(file_path, "rb") as file:
        await interaction.response.send_message(file=discord.File(file, filename="image.png"))


# TODO help command
@tree.command(name="help", description="Help")
async def help(interaction):
    await interaction.response.send_message("Help")


client.run(config.TOKEN)
