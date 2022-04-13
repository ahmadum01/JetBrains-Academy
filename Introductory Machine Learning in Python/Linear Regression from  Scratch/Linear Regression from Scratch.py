import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

f1 = [2.31, 7.07, 7.07, 2.18, 2.18, 2.18, 7.87, 7.87, 7.87, 7.87]
f2 = [65.2, 78.9, 61.1, 45.8, 54.2, 58.7, 96.1, 100.0, 85.9, 94.3]
f3 = [15.3, 17.8, 17.8, 18.7, 18.7, 18.7, 15.2, 15.2, 15.2, 15.2]
y = [24.0, 21.6, 34.7, 33.4, 36.2, 28.7, 27.1, 16.5, 18.9, 15.0]


class CustomLinearRegression:
    def __init__(self, *, fit_intercept=True):
        self.fit_intercept = fit_intercept
        self.coefficient = None
        self.intercept = None
        self.lin_array = None
        self.return_dict = None

    def fit(self, X, y):
        if self.fit_intercept:
            X = self.add_ones(X)
            self.lin_array = np.linalg.inv(X.T @ X) @ X.T @ y
            self.intercept = self.lin_array[0]
            self.coefficient = self.lin_array[1:]
            self.return_dict = {'Intercept': self.intercept,
                                'Coefficient': self.coefficient}
        else:
            self.coefficient = np.linalg.inv(X.T @ X) @ X.T @ y

            self.return_dict = {'Coefficient': self.coefficient}

    def predict(self, X):
        if self.fit_intercept:
            # Add column of 1's to array
            X = self.add_ones(X)
            return X @ self.lin_array
        else:
            return X @ self.coefficient

    def r2_score(self, y, yhat):
        r2_num = np.sum((y - yhat) ** 2)
        r2_den = np.sum((y - y.mean()) ** 2)
        self.return_dict['R2'] = 1 - (r2_num / r2_den)

    def rmse(self, y, yhat):
        mse = (1/y.shape[0]) * np.sum((y - yhat) ** 2)
        rmse = np.sqrt(mse)
        self.return_dict['RMSE'] = rmse

    @staticmethod
    def add_ones(target_array):
        x1 = np.ones((target_array.shape[0], 1))
        new_array = np.concatenate((x1, target_array), axis=1)
        return new_array


def main():
    df = pd.DataFrame([f1, f2, f3, y]).T
    model = CustomLinearRegression()
    model.fit(df.iloc[:, 0:-1].values, df.iloc[:, -1].values)

    regSci = LinearRegression(fit_intercept=True)
    regSci.fit(df.iloc[:, 0:-1].values, df.iloc[:, -1].values)

    yhat = model.predict(df.iloc[:, 0:-1].values)
    model.r2_score(df.iloc[:, -1].values, yhat)
    model.rmse(df.iloc[:, -1].values, yhat)

    dict_ = model.return_dict
    dict_['Intercept'] = regSci.intercept_ - dict_['Intercept']
    dict_['Coefficient'] = regSci.coef_ - dict_['Coefficient']
    yhat = regSci.predict(df.iloc[:, 0:-1].values)
    dict_['R2'] = r2_score(df.iloc[:, -1].values, yhat) - dict_['R2']
    dict_['RMSE'] = np.sqrt(mean_squared_error(df.iloc[:, -1].values, yhat)) - dict_['RMSE']
    print(dict_)


if __name__ == '__main__':
    main()