import skopt

# Hyperparameter spaces according to skopt
# MLP
space_mlp = [
    skopt.space.Integer(0, 4, name='n_hidden_layers'),
    skopt.space.Integer(10, 100, name='hidden_layer_size'),
    skopt.space.Categorical(['identity', 'logistic', 'tanh', 'relu'], name='activation'),
    skopt.space.Categorical(['constant', 'invscaling', 'adaptive'], name='learning_rate')
]

# Random Forest Regressor
space_rf_reg = [
    skopt.space.Integer(1, 20, name='min_samples_leaf'),
    skopt.space.Real(low=0.1, high=0.9, name='max_features'),
    skopt.space.Categorical([True, False], name='bootstrap'),
    skopt.space.Integer(2, 20, name='min_samples_split'),
    skopt.space.Categorical(['mse', 'mae'], name='criterion')
]

# Random Forest Classifier
space_rf_clf = [
    skopt.space.Integer(1, 20, name='min_samples_leaf'),
    skopt.space.Real(low=0.1, high=0.9, name='max_features'),
    skopt.space.Categorical([True, False], name='bootstrap'),
    skopt.space.Integer(2, 20, name='min_samples_split'),
    skopt.space.Categorical(['entropy', 'gini'], name='criterion')
]

# SVM-Classifier (SVC) & SVM-Regressor (SVR)
space_svm = [
    skopt.space.Real(low=2e-5, high=2e15, name='C'),
    skopt.space.Real(low=2e-15, high=2e3, name='gamma'),
    skopt.space.Categorical(['sigmoid', 'rbf', 'poly'], name='kernel'),
    skopt.space.Real(low=1e-4, high=1.0, name='tol')
]

# KerasRegressor
# Based on: https://arxiv.org/pdf/1905.04970.pdf
space_keras = [
    skopt.space.Categorical([.0005, .001, .005, .01, .1], name='init_lr'),
    skopt.space.Categorical([8, 16, 32, 64], name='batch_size'),
    skopt.space.Categorical(['cosine', 'constant'], name='lr_schedule'),
    skopt.space.Categorical(['relu', 'tanh'], name='hidden_layer1_activation'),
    skopt.space.Categorical(['relu', 'tanh'], name='hidden_layer2_activation'),
    skopt.space.Categorical(['relu', 'tanh'], name='hidden_layer3_activation'),
    skopt.space.Categorical([0, 32, 64, 128, 256, 512], name='hidden_layer1_size'),
    skopt.space.Categorical([0, 32, 64, 128, 256, 512], name='hidden_layer2_size'),
    skopt.space.Categorical([0, 32, 64, 128, 256, 512], name='hidden_layer3_size'),
    skopt.space.Categorical([.0, .3, .6], name='dropout1'),
    skopt.space.Categorical([.0, .3, .6], name='dropout2'),
    skopt.space.Categorical([.0, .3, .6], name='dropout3'),
]

# HP values for warm starting a Keras model //
# https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html#sklearn.neural_network.MLPClassifier
warmstart_keras = {'init_lr': 0.001,
                   'batch_size': 200,
                   'lr_schedule': 'constant',
                   'hidden_layer1_activation': 'relu',
                   'hidden_layer2_activation': 'relu',
                   'hidden_layer3_activation': 'relu',
                   'hidden_layer1_size': 100,
                   'hidden_layer2_size': 100,
                   'hidden_layer3_size': 100,
                   'dropout1': 0.0,
                   'dropout2': 0.0,
                   'dropout3': 0.0}

# XGBoostModel
# https://xgboost.readthedocs.io/en/latest/parameter.html
space_xgb = [
    skopt.space.Real(9.77e-4, 1.0, name='eta'),
    skopt.space.Categorical(['gbtree', 'gblinear', 'dart'], name='booster'),
    skopt.space.Real(0.1, 1.0, name='subsample'),
    skopt.space.Integer(1, 15, name='max_depth'),
    skopt.space.Real(1.0, 128.0, name='min_child_weight'),
    skopt.space.Real(0.0, 1.0, name='colsample_bytree'),
    skopt.space.Real(0.0, 1.0, name='colsample_bylevel'),
    skopt.space.Real(9.77e-4, 1, name='lambda'),
    skopt.space.Real(9.77e-4, 1, name='alpha')
]

# Default / warm start parameters for an XGBoostModel: https://github.com/dmlc/xgboost/blob/master/doc/parameter.rst
warmstart_xgb = {'booster': 'gbtree',
                 'n_estimators': 100,
                 'eta': 0.3,
                 'max_depth': 6,
                 'sample_type': 'uniform',
                 'normalize_type': 'tree',
                 'rate_drop': 0.0,
                 'updater': 'shotgun'}

# AdaBoostRegressor
space_ada_reg = [
    skopt.space.Integer(1, 10, name='max_depth'),
    skopt.space.Real(low=0.01, high=2.0, name='learning_rate'),
    skopt.space.Categorical(['linear', 'square', 'exponential'], name='loss'),
    skopt.space.Integer(40, 100, name='n_estimators')
]

# AdaBoostClassifier
space_ada_clf = [
    skopt.space.Integer(1, 10, name='max_depth'),
    skopt.space.Real(low=0.01, high=2.0, name='learning_rate'),
    skopt.space.Categorical(['SAMME', 'SAMME.R'], name='algorithm'),
    skopt.space.Integer(40, 100, name='n_estimators')
]

# DecisionTreeRegressor & -Classifier
# Hanno treated all integer-HPs as a continuous HP >> only continuous HPs (CMA-ES is applicable)
# A lot more HPs in scikit-learn documentation (e.g. max_features; included in RF HP-space)
space_dt = [
    skopt.space.Integer(1, 60, name='min_samples_split'),
    skopt.space.Integer(1, 30, name='max_depth'),
    skopt.space.Integer(1, 60, name='min_samples_leaf'),
    skopt.space.Real(0, 1, name='ccp_alpha')
]

# Linear Regression
space_linr = [
    skopt.space.Categorical([True, False], name='fit_intercept'),
    skopt.space.Categorical([False, True], name='normalize')
]

# KNNClassifier & KNNRegressor
space_knn = [
    skopt.space.Integer(1, 100, name='n_neighbors'),
    skopt.space.Categorical(['uniform', 'distance'], name='weights'),
    skopt.space.Categorical(['auto', 'ball_tree', 'kd_tree', 'brute'], name='algorithm'),
    skopt.space.Integer(1, 60, name='leaf_size'),
    skopt.space.Integer(1, 2, name='p')
]

# LightGBM model
# Important HPs: https://lightgbm.readthedocs.io/en/latest/Parameters-Tuning.html
# Example of HP tuning with Optuna:
# https://medium.com/optuna/lightgbm-tuner-new-optuna-integration-for-hyperparameter-optimization-8b7095e99258
space_lgb = [skopt.space.Integer(2, 256, name='num_leaves'),
             skopt.space.Integer(20, 1000, name='min_data_in_leaf'),
             skopt.space.Integer(-1, 100, name='max_depth'),
             skopt.space.Real(low=0.1, high=1.0, name='feature_fraction'),
             skopt.space.Real(low=0.1, high=1.0, name='bagging_fraction')]

# HP values for warm starting a LightGBM model // HP values need to be inside the bounds of the predefined HP-space
# for a LightGBM model (see above)
warmstart_lgb = {'num_leaves': 31,
                 'min_data_in_leaf': 20,
                 'max_depth': -1,
                 'lambda_l1': 0.0,
                 'lambda_l2': 0.0}

# Logistic Regression
# https://machinelearningmastery.com/hyperparameters-for-classification-machine-learning-algorithms/
space_logr = [
    skopt.space.Real(low=1e-6, high=1e-2, name='tol'),
    skopt.space.Real(low=0.1, high=4.0, name='C'),
    skopt.space.Categorical([True, False], name='fit_intercept'),
    skopt.space.Real(low=0.1, high=4.0, name='intercept_scaling'),
    skopt.space.Categorical(['newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga'], name='solver'),
    skopt.space.Integer(low=50, high=150, name='max_iter')
]

# Gaussian Naive Bayes
space_nb = [skopt.space.Real(low=0, high=1, name='var_smoothing')]
