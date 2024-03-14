"""
Module to train movie revenue model
"""
import os
import pandas as pd
import catboost as cb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib

#pylint: disable=invalid-name, line-too-long

def train_movie_revenue_model(df: pd.DataFrame):
    """
    Train a CatBoost regression model to predict movie revenue.

    Args:
        data_path (str): The path to the CSV file containing the movie data.

    Returns:
        cb.CatBoostRegressor: The trained CatBoost regression model.
    """

    df = df.rename(columns={'Revenue_InflationCorrected':'Revenue'})
    features = ['actor', 'actress', 'director', 'writer', 'Production_Company', 'runtimeMinutes', 'genres', 'isAdult', 'averageRating']
    target = 'Revenue'

    X = df[features]
    y = df[target]

    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    categorical_features_indices = [X_train.columns.get_loc(col) for col in ['actor', 'actress', 'director', 'Production_Company', 'writer', 'genres']]

    # Hyperparameter tuning (run only once)
    # param_grid = {
    #     'depth': np.arange(6,11,1),
    #     'learning_rate': [0.01, 0.05, 0.1],
    #     'l2_leaf_reg': [1, 3,5,7]  # Values for L2 regularization
    # }
    # cbobject = cb.CatBoostRegressor(
    #     eval_metric='RMSE',
    #     cat_features=categorical_features_indices
    # )
    # cbobject.randomized_search(param_grid, X=X_train, y=y_train, cv=5, n_iter=10, plot=True)

    # Train the model
    model_revenue = cb.CatBoostRegressor(
        iterations=1500,
        learning_rate=0.1,
        depth=9,
        eval_metric='RMSE',
        l2_leaf_reg=5,
        cat_features=categorical_features_indices,
        use_best_model=True
    )
    model_revenue.fit(X_train, y_train, eval_set=(X_test, y_test), early_stopping_rounds=50, verbose=100)

    # Save the model
    #joblib.dump(model_revenue, 'revenueModelv2.joblib')

    return model_revenue


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
        model = joblib.load(os.path.abspath("../../models/revenueModelv2.joblib"))
    y_pred = model.predict(X_test)
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    r2 = r2_score(y_pred=y_pred, y_true=y_test)
    return (rmse, r2)

# revenue_model = train_movie_revenue_model(df=pd.read_csv(os.path.abspath("../data/cleaned/data_clean_v6.csv")))
