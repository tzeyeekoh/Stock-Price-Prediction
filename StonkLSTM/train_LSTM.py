import config
import data_preprocessor as pp

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout


def train_LSTM_model(X_train, y_train):
    model = Sequential()
    model.add(LSTM(units = 50, return_sequences=True, input_shape = (60,1)))
    model.add(Dropout(0.2))
    model.add(LSTM(units = 50))
    model.add(Dense(units = 1))
    
    model.compile(optimizer = 'adam', loss = 'mse')
    model.fit(X_train, y_train, epochs = 150, batch_size=32)

    model.save('LSTMmodel.h5')
    print('Model saved as LSTMmodel.h5')

    score = model.evaluate(X_train, y_train)
    print(model.metrics_names,score)

X_train, y_train = pp.load_train_set(config.train_attr)
train_LSTM_model(X_train, y_train)