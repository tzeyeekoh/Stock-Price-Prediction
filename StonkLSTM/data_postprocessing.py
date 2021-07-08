import matplotlib.pyplot as plt
import numpy as np

import config
import data_query as dq

def price_plot(pred_price_lst):
    df = dq.load_dataset()
    pred_price_lst = np.concatenate(pred_price_lst, axis=0)

    prev_close_price = [df.iloc[len(df)-1:]['Close'].values]
    pred_price_lst = np.concatenate([prev_close_price, pred_price_lst], axis=0)
    print(pred_price_lst)

    num_days = [x for x in range(1, config.pred_days +2)]
    plt.plot(num_days, np.concatenate(pred_price_lst, axis=0), color = 'blue', label = 'Predicted')
    plt.show()