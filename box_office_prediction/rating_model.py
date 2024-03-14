"""
Module to train movie rating model
"""
import os
import pandas as pd
import catboost as cb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib

#pylint: disable=invalid-name, line-too-long


def train_model(df: pd.DataFrame) -> cb.CatBoostRegressor:
    """
    Train a CatBoost regression model on the given DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing the training data.

    Returns:
        cb.CatBoostRegressor: The trained CatBoost regression model.
    """
    features = ['actor', 'actress', 'director', 'writer', 'Production_Company', 'runtimeMinutes', 'genres', 'isAdult']
    target = 'averageRating'

    X_train, X_test, y_train, y_test = train_test_split(df[features], df[target], test_size=0.3, random_state=42)
    categorical_features_indices = [X_train.columns.get_loc(col) for col in ['actor', 'actress', 'director', 'Production_Company', 'writer', 'genres']]

    model = cb.CatBoostRegressor(
        iterations=1500,
        learning_rate=0.1,
        depth=8,
        eval_metric='RMSE',
        l2_leaf_reg=5,
        cat_features=categorical_features_indices,
        use_best_model=True
    )

    model.fit(X_train, y_train, eval_set=(X_test, y_test), early_stopping_rounds=50, verbose=100)

    # Run only once to get optimal params
    # param_grid = {
    #     'iterations': [1000, 1500, 2000],
    #     'depth': [6, 7, 8],
    #     'learning_rate': [0.01, 0.05, 0.1],
    #     'l2_leaf_reg': [1, 3, 5]  # Values for L2 regularization
    # }

    # #Perform grid search with cross-validation
    # grid_search = GridSearchCV(model, param_grid, cv=5, scoring='neg_mean_squared_error', n_jobs=-1)
    # grid_search.fit(X_train, y_train, eval_set=(X_test, y_test), early_stopping_rounds=50, verbose=100)
    # print(grid_search.best_params_)

    #joblib.dump(model, os.path.abspath("../../models/ratingModel.joblib"))
    return model


def predict_model(X_test: pd.DataFrame, y_test: pd.Series, model) -> tuple:
    """
    Predict using the trained CatBoost regression model.

    Args:
        X_test (pd.DataFrame): The features of the test data.
        y_test (pd.Series): The target variable of the test data.

    Returns:
        tuple: A tuple containing the RMSE and R^2 score of the predictions.
    """

    if X_test.empty or y_test.empty:
        raise ValueError("Atleast one output or input feature required")
    if not model:
        model = joblib.load(os.path.abspath("../../models/ratingModelv2.joblib"))
    y_pred = model.predict(X_test)
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    r2 = r2_score(y_pred=y_pred, y_true=y_test)
    return (rmse, r2)


#ratings_model = train_model(df=pd.read_csv(os.path.abspath("../../../data/cleaned/data_clean_v6.csv")))
