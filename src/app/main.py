from preprocess.preprocess import Preprocess

prep = Preprocess()
X_train, X_test, y_train, y_test = prep.pipeline(ticker='F')
print(y_test)