from PIL import Image, ImageDraw, ImageFont
import io

FONT_LOC = " ~/.config/sway/UbuntuMonoNerdFontMono-Regular.ttf"

# background_color = (0, 0, 0)
# text_color = (0, 127, 0)


background_color = (255, 255, 255)
text_color = (127, 127, 127)

def create_ascii_char_gif(chars, duration=500):
    images = []
    font = ImageFont.truetype(FONT_LOC, 16)

    left, top, right, bottom = font.getbbox(chars[0])

    text_width = right
    text_height = bottom

    for x in range(len(chars)):
        image = Image.new('RGB', (int(text_width), int(text_height*len(chars))), color=background_color)
        draw = ImageDraw.Draw(image)

        for y in range(len(chars)):
            # print((x+y) % (len(chars)))
            draw.text((-left, -top+text_height*y), chars[(y-x) % (len(chars))], fill=text_color, font=font)

        images.append(image)

    output = io.BytesIO()
    images[0].save(output, format='GIF', save_all=True, append_images=images[1:], duration=duration, loop=0)

    with open('animated_char.gif', 'wb') as f:
        f.write(output.getvalue())


def ascii_char(char):
    font = ImageFont.truetype(FONT_LOC, 16)

    left, top, right, bottom = font.getbbox(char)

    text_width = right
    text_height = bottom

    image = Image.new('RGB', (int(text_width), int(text_height)), color=background_color)
    draw = ImageDraw.Draw(image)

    draw.text((-left, -top/2), char, fill=text_color, font=font)


    # output = io.BytesIO()
    image.save("./char.png")

def website_cursor():
    images = []
    font = ImageFont.truetype(FONT_LOC, 16)

    frames = [
        "astatin3@dev:/$  ",
        "astatin3@dev:/$█ ",
    ]

    left, top, right, bottom = font.getbbox(frames[0])

    text_width = right
    text_height = bottom

    for i in range(len(frames)):
        image = Image.new('RGB', (int(text_width), int(text_height)), color=background_color)
        draw = ImageDraw.Draw(image)

        draw.text((-left, 0), frames[i], fill=text_color, font=font)

        images.append(image)

    output = io.BytesIO()
    images[0].save(output, format='GIF', save_all=True, append_images=images[1:], duration=500, loop=0)

    with open('cursor.gif', 'wb') as f:
        f.write(output.getvalue())

# create_ascii_char_gif([
#     ".-~^*@#/",
#     "-~^*@#/.",
#     "~^*@#/.-",
#     "^*@#/.-~",
#     "*@#/.-~^",
#     "@#/.-~^*",
#     "#/.-~^*@",
#     "/.-~^*@#",
# ])

ascii_char("`")

# website_cursor()