from Char_generator import char_database_generator as cdg
from PIL import Image, ImageDraw, ImageFont, ImageFilter

import keras, json
from keras.datasets import mnist
from keras.layers import Dense
from keras.models import Sequential
from keras.optimizers import SGD
import matplotlib.pyplot as plt
from keras.preprocessing import image
from nn_create_model import get_model


img = Image.open("./test_digit_9.png")
 # Cut white edges from image.
img = cdg.cut_white_edges(img)
# Convert image in color range 0 - 255.
img = img.convert("1")
# Make image to be square without distorting the char.
img = cdg.squarify_image(img)
# Resize image as input for NN.
img = img.resize((28,28))
# Transform into np.array.
img = 1 - image.img_to_array(img)
# Reshape array for input format.
img = img.reshape((1,784))

model = get_model()
model.load_weights("mymodel.h5")
img_class = model.predict_classes(img)
prediction = img_class[0]
classname = img_class[0]

print("Class: ",classname)
img = img.reshape((28,28))
plt.imshow(img)
plt.title(classname)
plt.show()