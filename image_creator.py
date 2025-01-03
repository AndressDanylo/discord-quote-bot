from PIL import Image, ImageDraw, ImageFont


def create_quote_image(quote_text, save_path):
    # creates quote image and saves it to given directory
    image_size = (1000, 500)
    background_color = (0, 0, 0)
    text_color = (255, 255, 255)
    text_position = (500,400)

    # blank image to draw on
    image = Image.new("RGB", image_size, color=background_color)
    draw = ImageDraw.Draw(image)

    # image handling
    draw.text(text_position, quote_text, fill=text_color, font=ImageFont.load_default())

    #image save
    image.save(save_path)

create_quote_image("quote", "media/image.png")