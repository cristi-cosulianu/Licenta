from PIL import Image, ImageDraw, ImageFont, ImageFilter
import auxiliary_functions as auxf

img = Image.open("Bonuri_crop\\1 - Copy.png")
draw = ImageDraw.Draw(img)
text = "Nuci de cocos"
img_fraction = 0.3
font_size = 65
light_font_path = "E:\\\Fonturi\\Arial_Light.ttf"
bold_font_path = "E:\\Facultate\\Anul III\\Sem II\\Licenta\\Fonturi\\Arial_Bold.ttf"
light_font = ImageFont.truetype(light_font_path, font_size)
bold_font = ImageFont.truetype(bold_font_path, font_size * 2)

width, height = img.size
line_height = 5
h_indent = 13
w_indent_name = 20
w_indent_price = 75
w_indent_total = 70
padding = 20
black = (0, 0, 0, 230)
grey = (59, 69, 60, 230)

product_name, product_price = auxf.load_menu_list()

products_number = 15
total_price = 0
for index in range(products_number):
  total_price = total_price + float(product_price[index])
total_price = str(total_price)

longest_product_name = max(product_name, key=lambda x:len(x))
bottom_boundaries = 80
displayed_producs_number = 0

# Draw product names.
for i in range(products_number):
  if ((h_indent + line_height * i) <= bottom_boundaries): 
    displayed_producs_number = max([i+1, displayed_producs_number])
    draw.text(((width/100) * w_indent_name, (height/100) * (h_indent + line_height * i)), product_name[i], fill=black, font=light_font)
  
# Draw product prices.
for i in range(products_number):
  if ((h_indent + line_height * i) <= bottom_boundaries):
    draw.text(((width/100) * w_indent_price, (height/100) * (h_indent + line_height * i)), product_price[i], fill=black, font=light_font)

# Draw total price.
total_vertical_position = (height/100) * (h_indent + line_height * (displayed_producs_number + 1.3))
draw.text(((width/100) * w_indent_total, total_vertical_position), total_price, fill=grey, font=bold_font)

# Calculate boundaries of the name column.
left = round((width/100) * w_indent_name - padding)
top = round((height/100) * h_indent - padding)
right = round((width/100) * w_indent_name + light_font.getsize(longest_product_name)[0] + padding)
bottom = round((height/100) * (h_indent + line_height * displayed_producs_number))
auxf.apply_unsharp(left, top, right, bottom, img, 3)

# Calculate boundaries of the price column.
left = round((width/100) * w_indent_price - padding)
right = round((width/100) * w_indent_price + light_font.getsize(total_price)[0] + padding)
auxf.apply_unsharp(left, top, right, bottom, img, 3)

# Calculate boundaries of the total price.
left = round((width/100) * w_indent_total - padding)
top = round(total_vertical_position - padding)
right = round((width/100) * w_indent_total + bold_font.getsize(total_price)[0] + padding) 
bottom = round((height/100) * (h_indent + line_height * (displayed_producs_number + 3.3)) + padding)

# Apply filters to make it looks much more realistic.
auxf.apply_unsharp(left, top, right, bottom, img, 5)
img = img.filter(ImageFilter.GaussianBlur(radius = 2))

img.save("pil_red.png")

