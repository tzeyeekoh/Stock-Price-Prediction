from sklearn.ensemble import RandomForestRegressor

class RandFor_Reg:

    def __init__(self, conf):
        '''Initialize Reg NN, set seeds for reproducible results'''
        self.n_est = conf['RFParams']['n_est']
        self.max_depth = conf['RFParams']['max_depth']

    def predict_nextday(self, model, X):
        '''Predict future gain based on gain window. Get prediction from latest day'''
        pred_gain = model.predict(X)
        latest_gain = pred_gain[-1]

        return latest_gain, pred_gain


    def train_rf(self, model, X_train, y_train):
        '''Train NN Regression'''
        model.fit(X_train, y_train)

        return model

    def rf_model(self):
        '''Random Forest Regression model
        Tune hyperparameters with google colab'''
        model = RandomForestRegressor(n_estimators=self.n_est, 
            criterion='mse', max_depth=self.max_depth, random_state=1)
        
        return model
