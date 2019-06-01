from Char_generator import char_database_generator as cdg

import keras
import os
import numpy as np
from keras.datasets import mnist
from keras.layers import Dense
from keras.models import Sequential
from keras.optimizers import SGD
from keras.preprocessing import image

def get_model():
    model = Sequential()
    model.add(Dense(units=128,activation="relu",input_shape=(784,)))
    model.add(Dense(units=128,activation="relu"))
    model.add(Dense(units=128,activation="relu"))
    model.add(Dense(units=10,activation="softmax"))
    model.compile(optimizer=SGD(0.001),loss="categorical_crossentropy",metrics=["accuracy"])
    return model

def load_my_data(chars_dir_name):
    train_x = []
    train_y = []

    for (root, dirs, files) in os.walk("Char_generator"):
        basename_dir = os.path.basename(root)
        if (chars_dir_name in root and basename_dir != chars_dir_name):
            char = cdg.get_char_from_dir_name(basename_dir)
            for file in files:
                file_path = os.path.join(root, file)
                img = image.load_img(path = file_path, color_mode = "grayscale", target_size = (28, 28, 1))
                # Value 1 where is black.
                img = 1 - image.img_to_array(img) / 255
                img = img.reshape((1,784))
                train_x.append(img)
                train_y.append(char)
    train_x = np.array(train_x)
    train_y = np.array(train_y)

    return train_x, train_y

if __name__ == "__main__":
    train_x, train_y = load_my_data(cdg.train_chars_dir_name)
    test_x, test_y = load_my_data(cdg.test_chars_dir_name)
    train_x = train_x.reshape(10000, 784)
    test_x = test_x.reshape(1000, 784)
    train_y = keras.utils.to_categorical(train_y, 10)
    test_y = keras.utils.to_categorical(test_y, 10)

    model = get_model()
    model.fit(train_x,train_y,batch_size=32,epochs=10,verbose=1)
    model.save("mymodel.h5")

    accuracy = model.evaluate(x=test_x,y=test_y,batch_size=32)
    print("Accuracy: ",accuracy[1])


# import keras
# import os
# import numpy as np
# from keras.datasets import mnist
# from keras.layers import Dense
# from keras.models import Sequential
# from keras.optimizers import SGD

# def get_model():
#     model = Sequential()
#     model.add(Dense(units=128,activation="relu",input_shape=(784,)))
#     model.add(Dense(units=128,activation="relu"))
#     model.add(Dense(units=128,activation="relu"))
#     model.add(Dense(units=10,activation="softmax"))
#     model.compile(optimizer=SGD(0.001),loss="categorical_crossentropy",metrics=["accuracy"])
#     return model

# (train_x, train_y) , (test_x, test_y) = mnist.load_data()
# train_x = train_x.reshape(60000,784)
# test_x = test_x.reshape(10000,784)
# train_y = keras.utils.to_categorical(train_y,10)
# test_y = keras.utils.to_categorical(test_y,10)

# model = get_model()
# # model.load_weights("mnistmodel.h5")
# model.fit(train_x,train_y,batch_size=32,epochs=10,verbose=1)
# model.save("mnistmodel.h5")


# accuracy = model.evaluate(x=test_x,y=test_y,batch_size=32)
# print("Accuracy: ",accuracy[1])

