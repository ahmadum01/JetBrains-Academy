import tensorflow as tf
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import Normalizer
from sklearn.model_selection import GridSearchCV

x_train, y_train, x_test, y_test = tf.keras.datasets.mnist.load_data(path="mnist.npz")
x_train1 = x_train.reshape([x_train.shape[0], x_train.shape[1] * x_train.shape[2]])
z_train, z_test, u_train, u_test = train_test_split(x_train1[0:6000], y_train[0:6000], test_size=0.3, random_state=40)


def fit_predict_eval(model, features_train=z_train, features_test=z_test, target_train=u_train, target_test=u_test):
    normalize = True
    if not normalize:
        model.fit(X=features_train, y=target_train)
        score = model.score(features_test, target_test)
    else:
        model.fit(X=Normalizer().transform(z_train), y=target_train)
        score = model.score(Normalizer().transform(z_test), target_test)
    print(f'Model: {model.__str__()}\nAccuracy: {round(score, 4)}\n')


if __name__ == '__main__':
    model_ = KNeighborsClassifier()
    params = {'n_neighbors': [3, 4, 5, 6],
              'weights': ['uniform', 'distance'],
              'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute']}
    clf = GridSearchCV(model_, params, scoring='accuracy', n_jobs=-1)
    clf.fit(X=Normalizer().transform(z_train), y=u_train)

    print("K-nearest neighbours algorithm")
    print("best estimator: ", clf.best_estimator_)
    print("accuracy:", clf.score(Normalizer().transform(z_test), u_test))

    model2 = RandomForestClassifier()
    clf2 = GridSearchCV(model2, {'n_estimators': [300, 500], 'max_features': ['auto', 'log2'],
                                 'class_weight': ['balanced', 'balanced_subsample'],
                                 'random_state': [40]}, scoring='accuracy', n_jobs=-1)
    clf2.fit(X=Normalizer().transform(z_train), y=u_train)

    print("\nRandom forest algorithm")
    print("best estimator: ", clf2.best_estimator_)
    print("accuracy:", clf2.score(Normalizer().transform(z_test), u_test))