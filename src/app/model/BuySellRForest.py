from sklearn.ensemble import RandomForestRegressor
import tensorflow as tf
import numpy as np

class RandFor_Reg:

    def __init__(self, conf):
        '''Initialize Reg NN, set seeds for reproducible results'''


    def predict_nextday(self, model, X_test):
        '''Predict future gain based on gain window. Get prediction from latest day'''
        pred_gain = model.predict(X_test)
        latest_gain = pred_gain[-1]

        return latest_gain


    def train_rf(self, model, X_train, y_train):
        '''Train NN Regression'''
        model.fit(X_train, y_train)

        return model

    def rf_model(self):
        '''Random Forest Regression model
        Tune hyperparameters with google colab'''
        model = RandomForestRegressor(n_estimators=100, 
            criterion='mse', max_depth=10, random_state=1)
        
        return model
