import numpy as np

from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

import config
import data_query as dq

model = load_model('LSTMmodel.h5')
model.summary()

def X_input(inputs):
    sc = MinMaxScaler(feature_range = (0, 1))
    inputs = sc.fit_transform(inputs)
    inputs = np.array(inputs)
    inputs = np.reshape(inputs,(1,60,1))
    return inputs

def pred_price(days):
    pred_price_lst = []
    for i in range(days):
        sc = MinMaxScaler(feature_range = (0, 1))
        df = dq.load_dataset()

        x_price = df.iloc[len(df)-60+i:len(df), 1:2].values
        if pred_price_lst:
            x_price = np.append(x_price, np.concatenate(pred_price_lst, axis=0), axis=0)
        
        x_price = sc.fit_transform(x_price)
        x_price = np.array(x_price)
        x_price = np.reshape(x_price,(1,config.train_length,1))

        pred_price_i = model.predict(x_price)
        print(pred_price_i)
        pred_price_i = sc.inverse_transform(pred_price_i)
        pred_price_lst.append(pred_price_i)

    return pred_price_lst
