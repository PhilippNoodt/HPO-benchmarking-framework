from sklearn.ensemble import RandomForestRegressor
from hyperopt import fmin, tpe, hp, Trials
from sklearn.metrics import mean_squared_error
from math import sqrt
from tensorflow import keras

import preprocessing as pp

FOLDER = 'datasets'
TRAIN_FILE = 'train.csv'
TEST_FILE = 'test.csv'
SAMPLE_SUB = 'sample_submission.csv'

train_raw = pp.load_data(FOLDER, TRAIN_FILE)
test_raw = pp.load_data(FOLDER, TEST_FILE)

X_train, y_train, X_val, y_val, X_test = pp.process(train_raw, test_raw, standardization=False, logarithmic=False,
                                                    count_encoding=False)


def train_evaluate_rf(X_train, y_train, X_val, y_val, params):
    rf_reg = RandomForestRegressor(**params, random_state=0)
    rf_reg.fit(X_train, y_train)

    y_pred = rf_reg.predict(X_val)

    val_loss = sqrt(mean_squared_error(y_val, y_pred))

    return val_loss

def train_evaluate_keras(X_train, y_train, X_val, y_val, params): # Assign budget as the number of epochs (int)
    model = keras.Sequential()

    model.add(keras.layers.InputLayer(input_shape=len(X_train.keys())))

    model.add(keras.layers.Dense(params['width_1stlayer'], activation='relu'))

    if params['hidden_layer_no1'][1] > 0:
        model.add(keras.layers.Dense(params['hidden_layer_no1'][1], activation='relu'))

    if params['hidden_layer_no1'][1] > 0 and params['hidden_layer_no2'][1] > 0:
        model.add(keras.layers.Dense(params['hidden_layer_no2'][1], activation='relu'))

    model.add(keras.layers.Dropout(params['dropout_rate']))
    model.add(keras.layers.Dense(1))

    optimizer = keras.optimizers.RMSprop(learning_rate=params['lr'])

    model.compile(optimizer=optimizer, loss='mse')

    model.fit(X_train, y_train, epochs=10, batch_size=128, validation_data=(X_val, y_val), verbose=1)

    y_pred = model.predict(X_val)

    val_loss = sqrt(mean_squared_error(y_val, y_pred))

    return val_loss

# Objective functions to be minimized
def objective_rf(params):
    return train_evaluate_rf(X_train, y_train, X_val, y_val, params)

def objective_keras(params):
    return train_evaluate_keras(X_train, y_train, X_val, y_val, params)


# Define Hyperparameter-space for RandomForestRegressor
rf_space = {}
rf_space['n_estimators'] = hp.choice('n_estimators', range(1, 201, 1))
rf_space['max_depth'] = hp.choice('max_depth', range(1, 81, 1))
rf_space['min_samples_leaf'] = hp.choice('min_samples_leaf', range(1, 30, 1))
rf_space['min_samples_split'] = hp.choice('min_samples_split', range(2, 20, 1))
rf_space['max_features'] = hp.choice('max_features', ['auto', 'sqrt'])

# Define Hyperparameter-space for Keras-Regressor
keras_space = {}
keras_space['lr'] = hp.loguniform('lr', low=1e-6, high=1e-1)
keras_space['dropout_rate'] = hp.uniform('dropout_rate', low=0.0, high=0.9)
keras_space['width_1stlayer'] = hp.choice('width_1stlayer', range(8, 513, 1))

# only binary choices for conditional hyperparameter (hidden layer 1 (yes/no))
keras_space['hidden_layer_no1'] = hp.choice('hidden_layer_no1', [
    ('no', 0),
    ('yes', hp.choice('width_hidlayer1', range(8, 513, 8)))
])

keras_space['hidden_layer_no2'] = hp.choice('hidden_layer_no2', [
    ('no', 0),
    ('yes', hp.choice('width_hidlayer2', range(8, 257, 8)))
])

# >> Handle conditional hyperparameters https://github.com/hyperopt/hyperopt/wiki/FMin


ALGORITHM = 'Keras' # 'RandomForestRegressor', 'Keras'

trials = Trials()

if ALGORITHM == 'RandomForestRegressor':
    res = fmin(fn=objective_rf, space=rf_space, trials=trials, algo=tpe.suggest, max_evals=100)
elif ALGORITHM == 'Keras':
    res = fmin(fn=objective_keras, space=keras_space, trials=trials, algo=tpe.suggest, max_evals=100)

print(res)