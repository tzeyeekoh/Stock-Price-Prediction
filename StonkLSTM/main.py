import config
import data_preprocessor as pp
import train_LSTM as tr
import LSTM_prediction as pr
import data_postprocessing as ds


'''
Predict price
'''
price_prediction = pr.pred_price(config.pred_days)
print(price_prediction)
ds.price_plot(price_prediction)