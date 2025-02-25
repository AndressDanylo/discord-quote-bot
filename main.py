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


@tree.context_menu(name="quote")
@discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def quote(interaction, message: discord.Message):
    file_path = await create_quote_image(message.content, message.author.display_name, message.author.name, message.created_at, message.author.avatar.url, "media/image.png")
    with open(file_path, "rb") as file:
        await interaction.response.send_message(file=discord.File(file, filename="image.png"))


# TODO help command
@tree.command(name="help", description="How to use the bot")
@discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def help(interaction):
    embed = discord.Embed(title="How to use the bot", color=discord.Color.green())

    embed.add_field(name="", value='Right click on a message and select "Quote" to convert it into a quote image.', inline=False)
    embed.set_image(url="https://cdn.discordapp.com/attachments/1324074923429462029/1344063226085900379/help_image.png?ex=67bf8bec&is=67be3a6c&hm=c4df96072da2fd15d92fc2d109cddf834310e00770f24c9b4037f8877347b535&")

    await interaction.response.send_message(embed=embed, ephemeral=True)


client.run(config.TOKEN)
