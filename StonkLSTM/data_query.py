import yfinance as yf

import config

def load_dataset():
    Stk = yf.Ticker(config.ticker)
    df_data = Stk.history(start= config.train_set_startdate)
    df_data.reset_index(level=0, inplace=True)
    return df_data
