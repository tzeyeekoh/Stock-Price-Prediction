import numpy as np
from sklearn.preprocessing import MinMaxScaler

import config
from data_query import load_dataset

def split_sequence(sequence, n_steps):
	X, y = list(), list()
	for i in range(len(sequence)):
		end_ix = i + n_steps
		if end_ix > len(sequence)-1:
			break
		seq_x, seq_y = sequence[i:end_ix], sequence[end_ix]
		X.append(seq_x)
		y.append(seq_y)
	return np.array(X), np.array(y)

def load_train_set(attr):
    df_training_set = load_dataset()
    training_set = df_training_set[attr].values
    training_set = training_set.reshape(-1,1)

    sc = MinMaxScaler(feature_range = (0, 1))
    training_set_scaled = sc.fit_transform(training_set)
    training_set_scaled = np.reshape(training_set_scaled,len(training_set_scaled))

    X_train, y_train = split_sequence(training_set_scaled, config.train_length)
    X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
    return X_train, y_train