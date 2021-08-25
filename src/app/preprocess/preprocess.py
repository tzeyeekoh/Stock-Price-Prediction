import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import yfinance as yf

class Preprocess:
    '''Get stock data and preprocess
    '''

    def __init__(self, conf):
        self.stk_range = conf['StockData']['range']
        self.buy_sell_thres = [conf['UserInput']['sell_threshold'], conf['UserInput']['buy_threshold']]
        self.gain_window = conf['UserInput']['gain_window']
        self.test_size = conf['UserInput']['test_size']

    def pipeline(self, ticker):
        '''Pipeline for preprocessing data
        '''
        df_data = self._query_data(ticker, period_range=self.stk_range)
        df_features = self._generate_features(df_data, buy_sell_threshold =self.buy_sell_thres, gain_window = self.gain_window)
        df_scaled = self._scale_data(df_features)
        X_train, X_test, y_train, y_test = self._part_data_train_test(df_scaled, test_size = self.test_size)
        
        return X_train, X_test, y_train, y_test

    def _query_data(self, ticker, period_range="Max"):
        '''Queries latest data from Yahoo finance with yfinance API
        '''
        stk_data = yf.Ticker(ticker)
        print("Stock: ", stk_data.ticker)
        df_data = stk_data.history(period=period_range)

        return df_data


    def _generate_features(self, df_data, buy_sell_threshold, gain_window):
        '''Generate features of interest
        '''
        df_data['Week'] = df_data.index.isocalendar().week
        df_data['Day'] = df_data.index.isocalendar().day

        df_data['PrevDayChng'] = df_data['Close'].pct_change(periods=1).shift(1).fillna(0)
        df_data['Var'] = df_data.Close.rolling(10).var()
        df_data['Var'] = df_data['Var'].fillna(df_data['Var'].mean())

        df_data['52Wk_High'] = df_data.Close.rolling(260, min_periods=1).max()
        df_data['52Wk_Low'] = df_data.Close.rolling(260, min_periods=1).min()

        df_data['EMA5'] = df_data.Close.ewm(span=5, adjust=False).mean()
        df_data['EMA12'] = df_data.Close.ewm(span=12, adjust=False).mean()
        df_data['EMA26'] = df_data.Close.ewm(span=26, adjust=False).mean()
        df_data['MACD'] = df_data.EMA12-df_data.EMA26
        df_data['Signal'] = df_data.MACD.ewm(span=9, adjust=False).mean()
        df_data['MACD_Trigger'] = df_data.MACD - df_data.Signal

        # % Change in 2 weeks
        df_data['Short_Gain'] = df_data.Close.pct_change(10).shift(-10)
        df_data['Short_Gain'] = df_data['Short_Gain'].fillna(df_data['Short_Gain'].mean())

        # % Change in long-term
        df_data['Long_Gain'] = df_data.Close.pct_change(gain_window).shift(-gain_window)
        df_data['Long_Gain'] = df_data['Long_Gain'].fillna(df_data['Long_Gain'].mean())

        bins=[-10]+buy_sell_threshold+[10]
        print("Bin Thresholds: ", bins)
        df_data['Rating'] = pd.cut(df_data.Long_Gain, bins=bins, labels=['Sell', 'Hold', 'Buy',])

        return df_data
    
    def _scale_data(self, df_data):
        '''Scale features with MinMax scaler
        '''
        price_scaler = MinMaxScaler()
        df_data_scaled = df_data
        df_data_scaled[['Close']] = price_scaler.fit_transform(df_data_scaled[['Close']])
        for c in ['Open', 'High', 'Low', '52Wk_High', '52Wk_Low']:
            df_data_scaled[[c]] = price_scaler.transform(df_data_scaled[[c]])

        indicator_cols =['Volume', 'Week', 'Day', 'PrevDayChng', 'MACD', 'Signal', 'EMA5', 'EMA12', 'EMA26', 'Var']
        indicator_scaler = MinMaxScaler()
        df_data_scaled[indicator_cols] = indicator_scaler.fit_transform(df_data_scaled[indicator_cols])

        return df_data_scaled
    
    def _part_data_train_test(self, df_data_scaled, test_size):
        '''Partition dataset into train and test sets
        '''
        df_X_input = df_data_scaled.drop(columns=['Short_Gain', 'Long_Gain','Rating'])
        X_train = df_X_input[:-test_size].values
        X_test = df_X_input[-test_size:].values

        df_y_input = df_data_scaled['Long_Gain']
        y_train = df_y_input[:-test_size].values
        y_test = df_y_input[-test_size:].values

        return X_train, X_test, y_train, y_test