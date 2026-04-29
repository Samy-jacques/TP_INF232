from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session
from typing import Literal
 
from app.database.db import get_db, UserDataPoint
from app.models.schemas import FriendlyDataPoint, HousingDataResponse, CA_CITIES, NEIGHBOURHOOD_POPULATION
from app.services import data_service as ds
from app.services import ml_service as ml
 
router = APIRouter(prefix="/api", tags=["data"])
 

VALID_FEATURES = list(ds.FEATURE_LABELS.keys())
 
@router.get("/health")
async def health_check():
    return {"status": "up and running"}

@router.get("/dataset")
def get_dataset(
    mode: Literal["original", "user", "combined"] = Query("combined"),
    db: Session = Depends(get_db),
):
    df = ds.get_dataset(mode, db)
    cols = list(ds.FEATURE_LABELS.keys()) + [ds.TARGET_LABEL, "_source"]
    available = [c for c in cols if c in df.columns]
    sample = df[available].head(500)
    return sample.to_dict(orient="records")
 
 
@router.get("/chart-data")
def get_chart_data(
    mode: Literal["original", "user", "combined"] = Query("combined"),
    feature: str = Query("MedInc"),
    db: Session = Depends(get_db),
):
    if feature not in VALID_FEATURES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid feature '{feature}'. Choose from: {VALID_FEATURES}"
        )
 
    df = ds.get_dataset(mode, db)

    if "_source" not in df.columns:
        df["_source"] = "original"

    if df.empty or len(df) == 0:
        raise HTTPException(
            status_code=404,
            detail="No data available. Submit some data points first."
        )
    regression = ml.run_regression(df, feature=feature, target="MedHouseVal")
    bar_data = ds.compute_bin_distribution(df[feature])
    pie_data = ds.compute_value_categories(df["MedHouseVal"])
    stats = {
        feature:      ds.compute_stats(df[feature]),
        "MedHouseVal": ds.compute_stats(df["MedHouseVal"]),
    }
 
    return {
        "scatter":        regression,
        "bar":            bar_data,
        "pie":            pie_data,
        "stats":          stats,
        "feature_label":  ds.FEATURE_LABELS.get(feature, feature),
        "n_user_points":  int((df["_source"] == "user").sum()),
        "n_total_points": int(len(df)),
    }
 
 
@router.post("/submit", response_model=HousingDataResponse, status_code=201)
def submit_data_point(
    payload: FriendlyDataPoint,
    db: Session = Depends(get_db),
):
    h = payload.to_housing_point()
    record = UserDataPoint(
        med_inc       = h.med_inc,
        house_age     = h.house_age,
        ave_rooms     = h.ave_rooms,
        ave_bedrms    = h.ave_bedrms,
        population    = h.population,
        ave_occup     = h.ave_occup,
        latitude      = h.latitude,
        longitude     = h.longitude,
        med_house_val = h.med_house_val,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record
 
 
@router.get("/cities")
def list_cities():
    return sorted(CA_CITIES.keys())
 
 
@router.get("/neighbourhoods")
def list_neighbourhoods():
    labels = {
        "quiet":    "Quiet street / cul-de-sac",
        "suburban": "Typical suburb",
        "busy":     "Busy urban block",
        "dense":    "Dense city centre",
    }
    return [{"key": k, "label": labels[k]} for k in NEIGHBOURHOOD_POPULATION]
 
 
@router.get("/user-data", response_model=list[HousingDataResponse])
def list_user_data(db: Session = Depends(get_db)):
    records = (
        db.query(UserDataPoint)
        .order_by(UserDataPoint.created_at.desc())
        .all()
    )
    return records
 
 
@router.delete("/user-data/reset", status_code=200)
def reset_user_data(db: Session = Depends(get_db)):
    deleted = db.query(UserDataPoint).delete()
    db.commit()
    return {"deleted": deleted, "message": "User data has been reset."}
 
 
@router.get("/export")
def export_csv(
    mode: Literal["original", "user", "combined"] = Query("combined"),
    db: Session = Depends(get_db),
):
    df = ds.get_dataset(mode, db)
    csv_content = ds.df_to_csv_string(df)
    filename = f"california_housing_{mode}.csv"
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
 
 
@router.get("/features")
def get_features():
    return [
        {"key": k, "label": v}
        for k, v in ds.FEATURE_LABELS.items()
    ]