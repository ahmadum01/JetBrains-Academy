import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression


class CustomLogisticRegression:
    def __init__(self, fit_intercept=True, l_rate=0.01, n_epoch=100):
        self.fit_intercept = fit_intercept
        self.l_rate = l_rate
        self.n_epoch = n_epoch
        self.errors_1 = []
        self.errors_2 = []

    def sigmoid(self, t):
        return 1 / (1 + np.exp(-t))

    def predict_proba(self, row, coef_):
        t = np.dot(row, coef_)
        return self.sigmoid(t)

    def fit_mse(self, X_train, y_train):
        if self.fit_intercept:
            X_train = np.c_[np.ones(len(X_train)), X_train]
        self.coef_ = np.zeros(X_train.shape[-1])

        for i_epoch in range(self.n_epoch):
            for i, row in enumerate(X_train):
                y_hat = self.predict_proba(row, self.coef_)
                self.coef_ = self.coef_ - self.l_rate * (y_hat - y_train[i]) * y_hat * (1 - y_hat) * row
                if i_epoch == 0:
                    self.errors_1.append(y_train[i] - y_hat)
                elif i_epoch == self.n_epoch - 1:
                    self.errors_2.append(y_train[i] - y_hat)

    def fit_log_loss(self, X_train, y_train):
        if self.fit_intercept:
            X_train = np.c_[np.ones(len(X_train)), X_train]
        self.coef_ = np.zeros(X_train.shape[-1])
        for i in range(self.n_epoch):
            y_hat = self.predict_proba(X_train, self.coef_)
            if i == 0:
                self.errors_1 = y_train - y_hat
            elif i == self.n_epoch - 1:
                self.errors_2 = y_train - y_hat
            self.coef_ = self.coef_ - self.l_rate * np.dot((y_hat - y_train), X_train) / len(X_train)

    def predict(self, X_test, cut_off=0.5):
        if self.fit_intercept:
            X_test = np.c_[np.ones(len(X_test)), X_test]
        predictions = []
        for row in X_test:
            y_hat = self.predict_proba(row, self.coef_)
            if y_hat > cut_off:
                predictions.append(1)
            else:
                predictions.append(0)
        return np.array(predictions)


if __name__ == '__main__':
    mse = CustomLogisticRegression(fit_intercept=True, l_rate=0.01, n_epoch=1000)
    logloss = CustomLogisticRegression(fit_intercept=True, l_rate=0.01, n_epoch=1000)
    lr = LogisticRegression()
    X, y = load_breast_cancer(return_X_y=True, as_frame=True)
    X = X.loc[:, ['worst concave points', 'worst perimeter', 'worst radius']]
    y = np.array(y)
    standardize = StandardScaler()
    standardize.fit(X)
    X_norm = standardize.transform(X)
    X_norm_train, X_norm_test, y_train, y_test = train_test_split(X_norm, y, train_size=0.8, random_state=43)
    mse.fit_mse(X_norm_train, y_train)
    y_pred_mse = mse.predict(X_norm_test)
    logloss.fit_log_loss(X_norm_train, y_train)
    y_pred_log_loss = logloss.predict(X_norm_test)
    lr.fit(X_norm_train, y_train)
    y_pred_lr = lr.predict(X_norm_test)

    accuracy_mse = accuracy_score(y_test, y_pred_mse)
    accuracy_log_loss = accuracy_score(y_test, y_pred_log_loss)
    accuracy_lr = accuracy_score(y_test, y_pred_lr)
    out_dict = {'mse_accuracy': accuracy_mse, 'logloss_accuracy': accuracy_log_loss, 'sklearn_accuracy': accuracy_lr,
                'mse_error_first': mse.errors_1, 'mse_error_last': mse.errors_2,
                'logloss_error_first': logloss.errors_1.tolist(), 'logloss_error_last': logloss.errors_2.tolist()}

    out_str = f"""Answers to the questions:  
                    1) 0.00003
                    2) 0.00000
                    3) 0.00153
                    4) 0.00580
                    5) expanded
                    6) expanded"""
    print(out_dict)
    print(out_str)