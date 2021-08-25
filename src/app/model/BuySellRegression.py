from keras.layers import Dense
from keras.models import Sequential
from keras.callbacks import EarlyStopping
import numpy as np
np.random.seed(1)

class NeuralNet_Reg:

    def __init__(self):
        pass

    def predict_nextday():
        pass

    def train_NN(model, X_train, X_test, y_train, y_test):
        callback = EarlyStopping(monitor='mae', patience=3, restore_best_weights=True, verbose=1)
        model.fit(X_train, y_train, epochs=100, batch_size=256, callbacks=[callback])
        print(model.evaluate(X_test, y_test))

    def reg_NN(self, X_train):
        model = Sequential()
        model.add(Dense(20, input_shape=(X_train.shape[1],), activation='relu'))
        model.add(Dense(50, activation='relu'))
        model.add(Dense(30, activation='relu'))
        model.add(Dense(10, activation='relu'))
        model.add(Dense(2, activation='relu'))
        model.add(Dense(1))

        model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])

        return model
