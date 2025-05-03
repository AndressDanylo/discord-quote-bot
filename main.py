import discord
import config
from image_creator import create_quote_image
from my_view import MyView

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
        await interaction.response.send_message(file=discord.File(file, filename="image.png"), view=MyView() if str(interaction.guild) else None) # customization view only appears in servers because discord doesn't allow accessing private or group chat messages required for customization 


@tree.command(name="help", description="How to use the bot")
@discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def help(interaction):
    embed = discord.Embed(title="How to use the bot", color=discord.Color.green())

    embed.add_field(name="", value='Right click on a message and select "Quote" to convert it into a quote image.', inline=False)
    embed.set_image(url=config.HELP_IMAGE)

    await interaction.response.send_message(embed=embed, ephemeral=True)


client.run(config.TOKEN)
