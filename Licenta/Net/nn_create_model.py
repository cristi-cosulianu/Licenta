import keras
from keras.datasets import mnist
from keras.layers import Dense
from keras.models import Sequential
from keras.optimizers import SGD
(train_x, train_y) , (test_x, test_y) = mnist.load_data()
#train_x = train_x.astype('float32') / 255
#test_x = test_x.astype('float32') / 255
# print(train_x.shape)
# print(train_y.shape)
# print(test_x.shape)
# print(test_y.shape)
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

# model.fit(train_x,train_y,batch_size=32,epochs=10,verbose=1)
# model.save("mnistmodel.h5")

accuracy = model.evaluate(x=test_x,y=test_y,batch_size=32)
print("Accuracy: ",accuracy[1])

# def load_my_dataset():
    