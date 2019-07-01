from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random, os, json, sys

image_extension = ".png"
train_chars_dir_name = "Chars_train"
test_chars_dir_name = "Chars_test"

alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.=:/+-*"

marks_dict = {
    ".": "_point",
    "=": "_equal",
    ":": "_colon",
    "/": "_slash",
    "+": "_plus",
    "-": "_minus",
    "*": "_prod"
}

if __name__ == "__main__":
    curr_directory = os.getcwd()
else:
    curr_directory = os.path.join(os.getcwd(), "Char_generator")

def create_char_image(char):
    image = Image.open(os.path.join(curr_directory, "Background.png"))
    draw = ImageDraw.Draw(image)
    if (char in "gpq"):
        font_size = 650
        x = 60
        y = -120
        xy = (x, y)
    elif (char in "J1234567890"):
        font_size = 650
        x = 60
        y = 0
        xy = (x, y)
    elif (char in "j"):
        font_size = 650
        x = 200
        y = -120
        xy = (x, y)
    elif (char in "iIl"):
        font_size = 650
        x = 200
        y = 0
        xy = (x, y)
    elif (char in "y"):
        font_size = 650
        x = 100
        y = -120
        xy = (x, y)
    elif (char in "W"):
        font_size = 550
        x = 0
        y = 40
        xy = (x, y)
    else: 
        font_size = 500
        x = 50
        y = 100
        xy = (x, y)
    light_font_path = os.path.join(curr_directory, "Fonturi\\Arial_Light.ttf")
    light_font = ImageFont.truetype(light_font_path, font_size)

    width, height = image.size
    black = (0, 0, 0, 230)

    draw.text(xy, char, fill=black, font=light_font)
    # Apply filters to make it looks much more realistic.
    image = image.filter(ImageFilter.UnsharpMask(radius= 5, percent=250, threshold=20))
    image = image.filter(ImageFilter.GaussianBlur(radius = 2))

    return image

def get_vector_sum_of_pixels(image):
    width, height = image.size
    pixel = image.getdata()
    sum_arr = [0] * (width)
    # Sum of pixel to identify spaces between leters.
    for i in range(height):
        for j in range(width):
            pixel_value = 0
            # print(pixel[i*width + j])
            if isinstance(pixel[i*width + j], list) or isinstance(pixel[i*width + j], tuple):
                pixel_value = 1 - sum(pixel[i*width + j]) / (255 * len(pixel[i*width + j]))
            elif isinstance(pixel[i*width + j], int):
                pixel_value = 1 - pixel[i*width + j] / 255

            sum_arr[j] += pixel_value
    return sum_arr

def get_text_indexes(sum_arr):
    space_indexs = []

    for index in range(len(sum_arr)):
        if (sum_arr[index] == 0):
            space_indexs.append(index)

    # Exclude consecutive indexes.
    i = 0
    while(i < len(space_indexs) - 1):
        if space_indexs[i] + 1 == space_indexs[i + 1]:
            i += 1
            while(i < len(space_indexs) - 1 and space_indexs[i] + 1 == space_indexs[i + 1]):
                space_indexs.pop(i)
        else:
            i += 1
    if (len(space_indexs) >= 2):
        space_indexs.pop(0)
        space_indexs.pop(len(space_indexs) - 1)

    return space_indexs

def cut_white_edges(image):
    width, height = image.size
    sum_arr = [0] * (width)

    sum_arr = get_vector_sum_of_pixels(image)
    left_right_indexes = get_text_indexes(sum_arr)
    if (len(left_right_indexes) >= 2):
        left_x = left_right_indexes[0]
        right_x = left_right_indexes[1]
    else:
        left_x = 0
        right_x = width

    new_image = image.rotate(90, expand=True)

    sum_arr = get_vector_sum_of_pixels(new_image)
    top_bottom_indexes = get_text_indexes(sum_arr)
    if (len(top_bottom_indexes) >= 2):
        top_y = top_bottom_indexes[0]
        bottom_y = top_bottom_indexes[1]
    else:
        top_y = 0
        bottom_y = height

    image = image.crop((left_x, top_y, right_x, bottom_y))
    return image

def squarify_image(image):
    width, height = image.size
    max_wh = max(width, height)
    square_img = Image.new("1", (max_wh, max_wh), "white")

    left_x = round(max_wh / 2 - width / 2)
    rifht_x = left_x + width
    square_img.paste(image, (left_x, 0, rifht_x, height))
    return square_img

def get_char_dir_name(char, chars_dir_name):
    if (marks_dict.get(char)):
        char_dir_name = os.path.join(chars_dir_name, "_" + marks_dict.get(char))
    elif "A" <= char and char <= "Z":
        char_dir_name = os.path.join(chars_dir_name, "_" + char)
    else:
        char_dir_name = os.path.join(chars_dir_name, char)
    return char_dir_name

def get_char_from_dir_name(char_dir_name):
    if(char_dir_name[0] == "_"):
        char_dir_name = char_dir_name[1:]

    if (char_dir_name in marks_dict.values()):
        index = marks_dict.values().index(char_dir_name)
        char = marks_dict.keys()[index]
    else:
        char = char_dir_name
    return char

def create_char_dir(char, chars_dir_name):
    char_dir_name = get_char_dir_name(char, chars_dir_name)
    if not os.path.isdir(char_dir_name):
        os.mkdir(char_dir_name)
    return char_dir_name

def write_image_to_json(image, label, filename):
    width, height = image.size
    pixels = []
    for w in range(width):
        for h in range(height):
            pixels.append((255 - image.getpixel((w,h))) / 255)
    print(pixels)

    json_data = json.dumps(dict({
        "label": label,
        "pixels": pixels
    }))
    with open("img.json", "w") as jsonfile:
        jsonfile.write(json_data)

def main(chars_dir_name, NR_INSTANCES):
    # Create chars directory.
    if not os.path.isdir(chars_dir_name):
        os.mkdir(chars_dir_name)

    # Iterate trough alphabet.
    for index in range(len(alphabet)):

        # Select char from alphabet.
        char = alphabet[index]
        print("Char: ", char)

        # Create char directory.
        char_dir_name = create_char_dir(char, chars_dir_name)

        # Generate a chosen number of instances of that char.
        for i in range(NR_INSTANCES):
            
            # Create an image with a char received as parameter.
            image = create_char_image(char)
            # Convert image in color range 0 - 255.
            image = image.convert("1")
            # Resize image as input for NN.
            image = image.resize((28,28))
            # Save image in char directory.
            filename = str(i) + image_extension
            image.save(os.path.join(char_dir_name, filename))
        
if __name__ == "__main__":
    main(train_chars_dir_name, 1)
    # main(test_chars_dir_name, 100)