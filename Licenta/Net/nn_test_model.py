import numpy
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.utils import np_utils
from keras.preprocessing import image
import matplotlib.pyplot as plt



# # fix random seed for reproducibility
# seed = 7
# numpy.random.seed(seed)

# # load data
# (X_train, y_train), (X_test, y_test) = mnist.load_data()

# # flatten 28*28 images to a 784 vector for each image
# num_pixels = X_train.shape[1] * X_train.shape[2]
# X_train = X_train.reshape(X_train.shape[0], num_pixels).astype('float32')
# X_test = X_test.reshape(X_test.shape[0], num_pixels).astype('float32')

# # normalize inputs from 0-255 to 0-1
# X_train = X_train / 255
# X_test = X_test / 255

# # one hot encode outputs
# y_train = np_utils.to_categorical(y_train)
# y_test = np_utils.to_categorical(y_test)
# num_classes = y_test.shape[1]

# # define baseline model
# def baseline_model():
# 	# create model
# 	model = Sequential()
# 	model.add(Dense(num_pixels, input_dim=num_pixels, kernel_initializer='normal', activation='relu'))
# 	model.add(Dense(num_classes, kernel_initializer='normal', activation='softmax'))
# 	# Compile model
# 	model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
# 	return model

# build the model
# model = baseline_model()
# Fit the model
# model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=200, verbose=2)
# model.save("./model", overwrite=True)
# Final evaluation of the model
# model.load_weights("./model")

# scores = model.evaluate(X_test, y_test, verbose=0)
# print("Baseline Error: %.2f%%" % (100-scores[1]*100))


import keras, json
from keras.datasets import mnist
from keras.layers import Dense
from keras.models import Sequential
from keras.optimizers import SGD
import matplotlib.pyplot as plt
from keras.preprocessing import image
from Char_generator.char_database_generator import squarify_image
from PIL import Image, ImageDraw, ImageFont, ImageFilter


(train_x, train_y) , (test_x, test_y) = mnist.load_data()
train_x = train_x.reshape(60000,784)
test_x = test_x.reshape(10000,784)
train_y = keras.utils.to_categorical(train_y,10)
test_y = keras.utils.to_categorical(test_y,10)


model = Sequential()
model.add(Dense(units=128,activation="relu",input_shape=(784,)))
model.add(Dense(units=128,activation="relu"))
model.add(Dense(units=128,activation="relu"))
model.add(Dense(units=10,activation="softmax"))
model.compile(optimizer=SGD(0.001),loss="categorical_crossentropy",metrics=["accuracy"])
model.load_weights("mnistmodel.h5")

# # Un script care preia imaginile si le face background alb ca sa le dea forma patrata
# # Ceva gen sa preia w si h al imaginei originale, vede care e mai mare, creata o imagine
# # patrata alba cu dimensiunea aflta si deseneaza in mijloc imaginea cu litera.
img = Image.open("../Ocropus/temp/0001/letters_010001/letter4.png")
img = squarify_image(img)
img.save("../Ocropus/temp/0001/letters_010001/letter4.png")

img = image.load_img(path="../Ocropus/temp/0001/letters_010001/letter4.png",grayscale=True,target_size=(28,28,1))
# # img = image.load_img(path="./Untitled.png",grayscale=True,target_size=(28,28,1))
img = image.img_to_array(img)

import json, numpy as np
alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.=:/+-*"
with open("./Char_generator/img.json", "r") as jsonfile:
    json_data = jsonfile.read()
    json_data = json.loads(json_data)
    label = int(json_data["label"])
    pixels = np.array(json_data["pixels"])
    test_x = []
    test_x.append(pixels)
    test_x.append(pixels)
    test_x = np.array(test_x)

    test_y = []
    test_y.append(label)
    test_y.append(label)
    test_y = np.array(test_y)
    test_y = keras.utils.to_categorical(test_y,10)


test_img = img.reshape((1,784))
img_class = model.predict_classes(test_img)
prediction = img_class[0]
classname = img_class[0]

print("Class: ",classname)
img = img.reshape((28,28))
plt.imshow(img)
plt.title(classname)
plt.show()