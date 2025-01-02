import discord
import config

# bot setup
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

# functionality
@client.event
async def on_ready():
    # Sync commands globally
    await tree.sync()
    print(f'We have logged in as {client.user} and synced commands.')


@tree.command(name="quote", description="Use this command in reply to a message you want to quote")
async def quote(interaction):
    await interaction.response.send_message(f"Quoted by {interaction.user}")


client.run(config.TOKEN)
