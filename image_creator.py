from PIL import Image, ImageDraw, ImageFont
import aiohttp
import io

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

async def create_quote_image(quote, author, author_username, quote_date, avatar_url, save_path, background="dark"):
    # Creates quote image and returns its path if created successfully
    # Configurations
    quote = quote[:400] + "..." if len(quote) >= 400 or not quote else quote # symbol limit
    width, height = 1000, 500
    bg_colors = {
        "dark": "black",
        "light": "white",
        "grayscale": "black",
    }
    text_colors = {
        "dark": (255, 255, 255), # contrast with dark background
        "light": (0, 0, 0), # contrast with light background
        "grayscale": (255, 255, 255),
    }
    blur_paths = {
        "dark": "media/quote_blur_dark.png",
        "light": "media/quote_blur_light.png",
        "grayscale": "media/quote_blur_dark.png",
    }
    main_font_path, italic_font_path = "media/Roboto.ttf", "media/Roboto-italic.ttf"

    # Fonts
    font = ImageFont.truetype(main_font_path, 25)
    author_font = ImageFont.truetype(italic_font_path, 25)
    username_font = ImageFont.truetype(main_font_path, 15)
    date_font = ImageFont.truetype(main_font_path, 15)

    # Fetch avatar and prepare images
    avatar_data = await fetch_avatar(avatar_url)
    avatar = Image.open(io.BytesIO(avatar_data)).convert("RGBA").resize((500, 500))
    blur_image = Image.open(blur_paths[background]).convert("RGBA")

    # Create base image
    image = Image.new("RGB", (width, height), bg_colors[background])
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
        draw.text((x, y), line, font=font, fill=text_colors[background])
        y += bbox[3] - bbox[1] + 5

    # Add author details
    draw.text((x, y + 25), f"-{author}", font=author_font, fill=text_colors[background])
    draw.text((x, y + 50), author_username, font=username_font, fill="#808080")
    draw.text((width - 100, height - 30), quote_date.strftime("%Y-%m-%d"), font=date_font, fill=text_colors[background])

    # Convert to grayscale if needed
    if background == "grayscale":
        image = image.convert("LA")

    # Save image
    image.save(save_path)
    return save_path
