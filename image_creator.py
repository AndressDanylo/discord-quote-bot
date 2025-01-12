from PIL import Image, ImageDraw, ImageFont
import aiohttp
import io
import asyncio

def wrap_text(text, font, max_width, draw):
    lines = []
    words = text.split()
    current_line = words.pop(0)

    for word in words:
        bbox = draw.textbbox((0, 0), current_line + ' ' + word, font=font)
        if bbox[2] <= max_width:
            current_line += ' ' + word
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)
    return lines

async def fetch_avatar(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.read()
            raise Exception("Failed to fetch avatar")

async def create_quote_image(quote, author, avatar_url, save_path):
    # Configurations
    width, height = 1000, 500
    bg_color, text_color = "black", (255, 255, 255)
    blur_path = "media/quote_blur.png"
    main_font_path, author_font_path, italic_font_path = "media/DMS.ttf", "media/Roboto.ttf", "media/Roboto-italic.ttf"

    # Fonts
    font = ImageFont.truetype(font_path, 25)
    author_font = ImageFont.truetype(author_font_path, 25)
    italic_font = ImageFont.truetype(italic_font_path, 15)

    # Fetch avatar and prepare images
    avatar_data = await fetch_avatar(avatar_url)
    avatar = Image.open(io.BytesIO(avatar_data)).convert("RGBA").resize((500, 500))
    blur_image = Image.open(blur_path).convert("RGBA")

    # Create base image
    image = Image.new("RGBA", (width, height), bg_color)
    image.paste(avatar, (-50, 0), avatar)
    image.paste(blur_image, (0, 0), blur_image)

    # Draw text
    draw = ImageDraw.Draw(image)
    max_text_width = 400
    lines = wrap_text(quote, font, max_text_width, draw)

    total_height = sum(draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1] for line in lines) + (len(lines) - 1) * 5
    y = (height - total_height) // 2

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x = (width + 400 - text_width) // 2
        draw.text((x, y), line, font=font, fill=text_color)
        y += bbox[3] - bbox[1] + 5

    # Add author details
    draw.text((x, y + 25), author, font=author_font)
    draw.text((x, y + 50), "@danyila", font=italic_font)

    # Save image
    image.save(save_path)
