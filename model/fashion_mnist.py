from train_model import TrainingModel


#load data to train
input_shape, x_train, x_test, y_train, y_test = TrainingModel.load_data('./data/train-images-idx3-ubyte','./data/train-labels-idx1-ubyte','./data/t10k-images-idx3-ubyte','./data/t10k-labels-idx1-ubyte')

#create model to train
model = TrainingModel.create_model(input_shape)

#training the model
trained_model, score = TrainingModel.train_model(model,x_train,y_train, x_test,y_test)

#output model and score
print(score)