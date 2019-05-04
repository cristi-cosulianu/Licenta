from PIL import Image
import sys, os

directory = "./temp/0001"

for file in os.listdir(directory):
    file = os.path.join(directory, file)
    if os.path.isdir(file):
        continue

    if "bin.png" in file:
        new_file = file[:-7] + "png"
        os.rename(file, new_file)
        file = new_file

    image_name = os.path.splitext(os.path.basename(file))[0]
    letters_dir = os.path.join(directory, "letters_" + image_name)
    if not os.path.exists(letters_dir):
        assert not os.mkdir(letters_dir), "Letter directory can't be created!"

    image = Image.open(file)
    width, height = image.size
    pixel = image.getdata()
    sum_arr = [0] * (width)

    # Sum of pixel to identify spaces between leters.
    for i in range(height):
        for j in range(width):
            pixel_value = 0
            if isinstance(pixel[i*width + j], list):
                pixel_value = 1 - sum(pixel[i*width + j]) / (255 * len(pixel[i*width + j]))
            elif isinstance(pixel[i*width + j], int):
                pixel_value = 1 - pixel[i*width + j] / 255

            sum_arr[j] += pixel_value

    # Average to know what index to chose.
    average = sum(sum_arr) / width
    space_indexs = []

    # Select space indexes using average value.
    for i in range(width):
        if (sum_arr[i] < average / 10):
            space_indexs.append(i)

    # Exclude consecudive indexes.
    i = 0
    while(i < len(space_indexs) - 1):
        if space_indexs[i] + 1 == space_indexs[i + 1]:
            i += 1
            while(i < len(space_indexs) - 1 and space_indexs[i] + 1 == space_indexs[i + 1]):
                space_indexs.pop(i)
        else:
            i += 1

    space_indexs.pop(0)
    counter = 0
    for i in range(0, len(space_indexs) - 1, 1):
        left_x = space_indexs[i]
        left_y = 0
        
        right_x = space_indexs[i + 1]
        right_y = height
        
        letter_img = image.crop((left_x, left_y, right_x, right_y))
        pixel = letter_img.getdata()

        # Sum of pixel to identify spaces between leters.
        suma = 0
        for j in range(len(pixel)):
            pixel_value = 0
            if isinstance(pixel[j], list):
                pixel_value = 1 - sum(pixel[j]) / (255 * len(pixel[j]))
            elif isinstance(pixel[j], int):
                pixel_value = 1 - pixel[j] / 255
            suma += pixel_value
        letter_width = letter_img.size[0]

        print("Suma", str(counter), str(suma), "Width: ", letter_width)

        if (suma < average * letter_width / 3 and letter_width < 20):
            print("Skip!")
            continue

        letter_img.save(letters_dir + "/letter" + str(counter) + ".png")
        counter += 1


        
