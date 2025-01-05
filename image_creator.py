from PIL import Image, ImageDraw, ImageFont
import aiohttp
import io


async def fetch_discord_avatar(avatar_url):
    # downloads user avatar
    async with aiohttp.ClientSession() as session:
            async with session.get(avatar_url) as response:
                if response.status == 200:
                    avatar_data = await response.read()
                    return avatar_data
                else:
                    raise Exception("Failed to fetch avatar")


async def create_quote_image(quote_text, quote_author, quote_author_avatar, save_path):
        # creates quote image and saves it to given directory
        image_size = (1000, 500)
        background_color = (0, 0, 0)
        text_color = (255, 255, 255)
        text_position = (500,400)
        blur_image = Image.open("media/quote_blur.png").convert("RGBA")

        # open avatar
        avatar_data = await fetch_discord_avatar(quote_author_avatar)
        avatar_image = Image.open(io.BytesIO(avatar_data)).convert("RGBA")
        avatar_image = avatar_image.resize((500, 500)) 

        # blank image to draw on
        image = Image.new("RGBA", image_size, color=background_color)
        draw = ImageDraw.Draw(image)

        # image handling
        draw.text(text_position, quote_text, fill=text_color, font=ImageFont.load_default())
        image.paste(avatar_image, (-50, 0), avatar_image)
        image.paste(blur_image, (0, 0), blur_image)


        # image save
        image.save(save_path)
