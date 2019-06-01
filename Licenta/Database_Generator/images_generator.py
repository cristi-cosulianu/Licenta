from PIL import Image, ImageDraw, ImageFont, ImageFilter
import auxiliary_functions as auxf
import random

img = Image.open("Background.png")
draw = ImageDraw.Draw(img)
text = str(random.randint(0, 9))
img_fraction = 0.3
font_size = 600
light_font_path = ".\\Fonturi\\Arial_Light.ttf"
bold_font_path = ".\\Fonturi\\Arial_Bold.ttf"
light_font = ImageFont.truetype(light_font_path, font_size)
bold_font = ImageFont.truetype(bold_font_path, font_size * 2)

width, height = img.size
black = (0, 0, 0, 230)
grey = (59, 69, 60, 230)

draw.text((height/20,height/20), text, fill=black, font=light_font)

img.save("./Letters/letter.png")

img = img.resize((28,28))
img.save("./Letters/resized.png")

