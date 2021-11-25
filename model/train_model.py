import struct
import numpy as np
import keras
from keras.utils import to_categorical
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Conv2D , MaxPooling2D , Activation
from keras.layers import Dense , Dropout , Flatten
from keras.layers import BatchNormalization
from keras import backend as K


class TrainingModel:
    #extract dataset from ubyte files
    def read_idx(filename):
        with open(filename , 'rb') as f:
            zero , data_type , dims = struct.unpack('>HBB' , f.read(4))
            shape = tuple(struct.unpack('>I' , f.read(4))[0] for d in range(dims))
            return np.frombuffer(f.read() , dtype = np.uint8).reshape(shape)

    
    #load process and one hot encode the data
    def load_data(_x_train, _y_train, _x_test, _y_test):
        x_train = read_idx(_x_train)
        y_train = read_idx(_y_train)
        x_test = read_idx(_x_test)
        y_test = read_idx(_y_test)

        print('Number of samples' , len(x_train))
        print('Number of labels ' , len(y_train))
        print('Images Dimensions' , x_train[0].shape)
        print('Label Dimensions' , y_train.shape)


        # data processing and augmentation
        img_rows = x_train[0].shape[0]
        img_cols = x_train[0].shape[1]

        x_train = x_train.reshape(x_train.shape[0] , img_rows , img_cols , 1)
        x_test = x_test.reshape(x_test.shape[0] , img_rows , img_cols , 1)

        print(x_train.shape)
        print(x_test.shape)

        x_train = x_train.astype('float32')
        x_test = x_test.astype('float32')

        x_train /= 255
        x_test /= 255

        print(x_train.shape)
        print(x_test.shape)

        #one hot encoding
        y_train = to_categorical(y_train)
        y_test = to_categorical(y_test)

        num_classes = y_test.shape[1]
        print(num_classes)
        num_pixels = x_train.shape[1] * x_train.shape[2]
        print(num_pixels)

        input_shape = (img_rows , img_cols , 1)

        return input_shape, x_train, x_test, y_train, y_test


    def create_model(input_shape):
        #Creating Model
        model = Sequential()

        #two sets of CRP
        model.add(Conv2D(20 , kernel_size = (5,5), input_shape = input_shape))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(MaxPooling2D(pool_size = (2,2) , strides = (2,2)))

        model.add(Conv2D(50 , kernel_size = (5,5)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(MaxPooling2D(pool_size = (2,2) , strides = (2,2)))


        model.add(Flatten())

        model.add(Dense(500 , activation = 'relu'))
        model.add(Dropout(0.5))
        model.add(Dense(num_classes , activation='softmax'))

        model.compile(loss = 'categorical_crossentropy' , optimizer = keras.optimizers.Adadelta() , metrics =['accuracy'])

        print(model.summary())

        return model

    
    def train_model(model, x_train, y_train, x_test, y_test):
        batch_size = 64
        epochs = 10

        final_model = model.fit(x_train , y_train , batch_size = batch_size , epochs = epochs , verbose = 1 , validation_data = (x_test , y_test) )#verbose how much information to see when training

        score = model.evaluate(x_test , y_test , verbose = 1)
        print("Test loss:" , score[0])
        print("Test accuracy:" , score[1])

        return final_model, score