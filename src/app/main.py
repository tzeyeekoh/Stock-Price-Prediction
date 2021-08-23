from preprocess.preprocess import Preprocess
from config.load_conf import read_config

conf = read_config()
prep = Preprocess(conf)
X_train, X_test, y_train, y_test = prep.pipeline(ticker='F')
print(y_test)