import discord
from image_creator import create_quote_image


class MyView(discord.ui.View):
    @discord.ui.select(
        placeholder = "style",
        max_values = 1,
        options = [
            discord.SelectOption(
                label = "light",
            ),
            discord.SelectOption(
                label = "dark",
            ),
            discord.SelectOption(
                label = "grayscale"
            ),

        ]
    ) 
    async def select_callback(self, interaction, select): # the function called when the user is done selecting options
        original_message = interaction.message.reference.cached_message # the message which was quoted

        if original_message is None:
            # Fetch the message manually if it wasn't cached in the bot's memory
            channel = interaction.channel
            original_message = await channel.fetch_message(interaction.message.reference.message_id)

        file_path = await create_quote_image(original_message.content, original_message.author.display_name, original_message.author.name, original_message.created_at, original_message.author.avatar.url, "media/image.png", select.values[0])
        file = discord.File(fp=file_path, filename="image.png")
        await interaction.response.defer()

        await interaction.edit_original_response(attachments=[file]) 
