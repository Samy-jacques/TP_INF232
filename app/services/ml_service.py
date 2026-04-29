import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error


def run_regression(
        df: pd.DataFrame,
        feature: str,
        target: str = "MedHouseVal",
) -> dict:
    subset = df[[feature, target, "_source"]].dropna()

    if len(subset) < 2:
        return _empty_result(feature)

    X = subset[[feature]].values
    y = subset[target].values

    model = LinearRegression()
    model.fit(X, y)

    y_pred = model.predict(X)
    r2 = r2_score(y, y_pred)
    mse = mean_squared_error(y, y_pred)

    user_indices = [
        i for i, src in enumerate(subset["_source"].values)
        if src == "user"
    ]

    sort_order = np.argsort(X.ravel())
    x_sorted = X.ravel()[sort_order].tolist()
    y_pred_sorted = y_pred[sort_order].tolist()

    x_scatter = X.ravel().tolist()
    y_scatter = y.tolist()

    x_line = [float(x_sorted[0]), float(x_sorted[-1])]
    y_line = [float(y_pred_sorted[0]), float(y_pred_sorted[-1])]

    return {
        "feature": feature,
        "coefficient": round(float(model.coef_[0]), 6),
        "intercept": round(float(model.intercept_), 6),
        "r2_score": round(float(r2), 6),
        "mse": round(float(mse), 6),
        "x_values": x_scatter,
        "y_values": y_scatter,
        "y_pred": y_pred_sorted,
        "x_line": x_line,
        "y_line": y_line,
        "user_indices": user_indices,
        "n_samples": int(len(subset)),
    }


def _empty_result(feature: str) -> dict:
    return {
        "feature": feature,
        "coefficient": 0.0,
        "intercept": 0.0,
        "r2_score": 0.0,
        "mse": 0.0,
        "x_values": [],
        "y_values": [],
        "y_pred": [],
        "x_line": [],
        "y_line": [],
        "user_indices": [],
        "n_samples": 0,
    }