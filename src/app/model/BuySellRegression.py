from keras.layers import Dense
from keras.models import Sequential
from keras.callbacks import EarlyStopping
import tensorflow as tf
import numpy as np

class NeuralNet_Reg:

    def __init__(self, conf):
        '''Initialize Reg NN, set seeds for reproducible results'''
        
    def predict_nextday(self, model, X_test):
        '''Predict future gain based on gain window. Get prediction from latest day'''
        pred_gain = model.predict(X_test)
        latest_gain = pred_gain[-1,0]

        return latest_gain


    def train_NN(self, model, X_train, y_train):
        '''Train NN Regression'''
        callback = EarlyStopping(monitor='val_mae', patience=self.earlystop, restore_best_weights=True, verbose=1)
        model.fit(X_train, y_train, epochs=self.epochs, batch_size=self.batchsize, callbacks=[callback], validation_split=self.val_split)

        return model

    def reg_NN(self, X_train):
        '''NN Regression model'''
        model = Sequential()
        model.add(Dense(20, input_shape=(X_train.shape[1],), activation='relu'))
        model.add(Dense(50, activation='relu'))
        model.add(Dense(30, activation='relu'))
        model.add(Dense(10, activation='relu'))
        model.add(Dense(2, activation='relu'))
        model.add(Dense(1))

        model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])

        return model
