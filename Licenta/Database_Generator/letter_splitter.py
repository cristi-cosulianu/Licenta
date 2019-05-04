from PIL import Image

output = open("./tests/bytes.txt", "w")
image = Image.open("./tests/010001.png")
width, height = image.size
pixel = image.getdata()
sum_arr = [0] * (width)

# Sum of pixel to identify spaces between leters.
for i in range(height):
    for j in range(width):
        pixel_value = 1 - sum(pixel[i*width + j]) / (255 * len(pixel[i*width + j]))
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
        pixel_value = 1 - sum(pixel[j]) / (255 * len(pixel[j]))
        suma += pixel_value
    letter_width = letter_img.size[0]

    print("Suma", str(counter), str(suma), "Width: ", letter_width)

    if (suma < average * letter_width / 3 and letter_width < 20):
        print("Skip!")
        continue

    letter_img.save("./tests/Letters/letter" + str(counter) + ".png")
    counter += 1


    
