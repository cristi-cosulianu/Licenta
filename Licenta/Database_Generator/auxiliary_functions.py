from PIL import Image, ImageDraw, ImageFont, ImageFilter
import json

def apply_unsharp(left, top, right, bottom, img, radius):
    # Crop the image.
    img_crop = img.crop((left, top, right, bottom))
    # Apply unsharp mask filter.
    img_crop = img_crop.filter(ImageFilter.UnsharpMask(radius=radius, percent=250, threshold=20))
    # Put back the image with filter.
    img.paste(img_crop, (left, top, right, bottom))
    img_crop.save("crop.png")

def load_menu_list():
    json_content = open("menu_db.json").read()
    menu_dict = json.loads(json_content)
    names = list(menu_dict.keys())
    prices = list(menu_dict.values())
    return (names, prices)