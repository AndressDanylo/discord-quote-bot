from PIL import Image, ImageDraw, ImageFont
import aiohttp


async def fetch_discord_avatar(avatar_url):
    # downloads user avatar
    async with aiohttp.ClientSession() as session:
            async with session.get(avatar_url) as response:
                if response.status == 200:
                    avatar_data = await response.read()
                    return avatar_data
                else:
                    raise raise Exception("Failed to fetch avatar")


def create_quote_image(quote_text, quote_author, save_path):
    # creates quote image and saves it to given directory
    image_size = (1000, 500)
    background_color = (0, 0, 0)
    text_color = (255, 255, 255)
    text_position = (500,400)

    # TODO open avatar

    # blank image to draw on
    image = Image.new("RGB", image_size, color=background_color)
    draw = ImageDraw.Draw(image)

    # image handling
    draw.text(text_position, quote_text, fill=text_color, font=ImageFont.load_default())

    # image save
    image.save(save_path)

create_quote_image("quote", "author", "media/image.png")