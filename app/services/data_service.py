import io
import csv
import numpy as np
import pandas as pd
from sklearn.datasets import fetch_california_housing
from sqlalchemy.orm import Session
from app.database.db import UserDataPoint


FEATURE_LABELS = {
    "MedInc": "Median Income ($10k)",
    "HouseAge": "House Age (years)",
    "AveRooms": "Avg Rooms",
    "AveBedrms": "Avg Bedrooms",
    "Population": "Population",
    "AveOccup": "Avg Occupancy",
    "Latitude": "Latitude",
    "Longitude": "Longitude",
}

TARGET_LABEL = "MedHouseVal"


KEY_TO_FEATURE = {
    "med_inc": "MedInc",
    "house_age": "HouseAge",
    "ave_rooms": "AveRooms",
    "ave_bedrms": "AveBedrms",
    "population": "Population",
    "ave_occup": "AveOccup",
    "latitude": "Latitude",
    "longitude": "Longitude",
    "med_house_val": "MedHouseVal",
}


def load_original_dataset() -> pd.DataFrame:
    housing = fetch_california_housing(as_frame=True)
    df = housing.frame.copy()
    df["_source"] = "original"
    return df


_ORIGINAL_DF: pd.DataFrame | None = None


def get_original_df() -> pd.DataFrame:
    global _ORIGINAL_DF
    if _ORIGINAL_DF is None:
        _ORIGINAL_DF = load_original_dataset()
    return _ORIGINAL_DF.copy()


def get_user_df(db: Session) -> pd.DataFrame:
    records = db.query(UserDataPoint).order_by(UserDataPoint.created_at).all()

    if not records:
        return pd.DataFrame(columns=list(KEY_TO_FEATURE.values()) + ["_source", "_id"])

    rows = []
    for r in records:
        rows.append({
            "MedInc": r.med_inc,
            "HouseAge": r.house_age,
            "AveRooms": r.ave_rooms,
            "AveBedrms": r.ave_bedrms,
            "Population": r.population,
            "AveOccup": r.ave_occup,
            "Latitude": r.latitude,
            "Longitude": r.longitude,
            "MedHouseVal": r.med_house_val,
            "_source": "user",
            "_id": r.id,
        })

    return pd.DataFrame(rows)


def get_combined_df(db: Session) -> pd.DataFrame:
    original = get_original_df()
    user = get_user_df(db)
    return pd.concat([original, user], ignore_index=True)


def get_dataset(mode: str, db: Session) -> pd.DataFrame:
    if mode == "original":
        return get_original_df()
    elif mode == "user":
        return get_user_df(db)
    elif mode == "combined":
        return get_combined_df(db)
    else:
        raise ValueError(f"Unknown dataset mode: {mode!r}")


def df_to_csv_string(df: pd.DataFrame) -> str:
    export_df = df.drop(columns=[c for c in ["_source", "_id"] if c in df.columns])
    output = io.StringIO()
    export_df.to_csv(output, index=False)
    return output.getvalue()


def compute_bin_distribution(series: pd.Series, n_bins: int = 10) -> dict:
    counts, bin_edges = np.histogram(series.dropna(), bins=n_bins)
    labels = [
        f"{bin_edges[i]:.2f}–{bin_edges[i + 1]:.2f}"
        for i in range(len(bin_edges) - 1)
    ]
    return {"labels": labels, "counts": counts.tolist()}


def compute_value_categories(series: pd.Series) -> dict:
    low = (series < 1.5).sum()
    medium = ((series >= 1.5) & (series < 3.0)).sum()
    high = (series >= 3.0).sum()
    return {
        "labels": ["Low (<$150k)", "Medium ($150k–$300k)", "High (>$300k)"],
        "values": [int(low), int(medium), int(high)],
    }


def compute_stats(series: pd.Series) -> dict:
    return {
        "count": int(series.count()),
        "mean": round(float(series.mean()), 4),
        "std": round(float(series.std()), 4),
        "min": round(float(series.min()), 4),
        "max": round(float(series.max()), 4),
    }