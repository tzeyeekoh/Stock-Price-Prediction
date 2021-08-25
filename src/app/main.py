from preprocess.preprocess import Preprocess
from model.BuySellRegression import NeuralNet_Reg
from config.load_conf import read_config

conf = read_config()
prep = Preprocess(conf)
NN = NeuralNet_Reg()

X_train, X_test, y_train, y_test = prep.pipeline(ticker='F')
print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)
print(X_test[-1])

model = NN.reg_NN(X_train)
model = NN.train_NN(model, X_train, y_train)
print(model.predict(X_test))

future_gain = NN.predict_nextday(model, X_test)
print(future_gain)