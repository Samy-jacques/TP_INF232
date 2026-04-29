from __future__ import annotations
from pydantic import BaseModel, Field, model_validator
from datetime import datetime
 
 
CA_CITIES: dict[str, tuple[float, float]] = {
    "Los Angeles":     (34.052, -118.244),
    "San Francisco":   (37.774, -122.419),
    "San Diego":       (32.716, -117.161),
    "San Jose":        (37.338, -121.886),
    "Sacramento":      (38.582, -121.494),
    "Oakland":         (37.804, -122.271),
    "Fresno":          (36.737, -119.787),
    "Long Beach":      (33.770, -118.193),
    "Bakersfield":     (35.373, -119.019),
    "Anaheim":         (33.836, -117.914),
    "Santa Ana":       (33.746, -117.868),
    "Riverside":       (33.980, -117.375),
    "Stockton":        (37.957, -121.291),
    "Irvine":          (33.684, -117.826),
    "San Bernardino":  (34.108, -117.289),
    "Modesto":         (37.639, -120.997),
    "Santa Rosa":      (38.440, -122.714),
    "Oxnard":          (34.197, -119.177),
    "Fontana":         (34.092, -117.435),
    "Moreno Valley":   (33.937, -117.230),
}
 
 
NEIGHBOURHOOD_POPULATION: dict[str, float] = {
    "quiet":    350.0,
    "suburban": 1100.0,
    "busy":     2500.0,
    "dense":    6000.0,
}
 
 
def _rooms_from_bedrooms(bedrooms: int) -> tuple[float, float]:
    mapping = {0: (2.5, 1.0), 1: (3.5, 1.0), 2: (4.5, 2.0),
               3: (5.5, 3.0), 4: (7.0, 4.0), 5: (8.5, 5.0)}
    return mapping.get(bedrooms, (10.0, float(min(bedrooms, 8))))
 
 
 
class FriendlyDataPoint(BaseModel):
    city:               str
    annual_income_usd:  float = Field(..., ge=5_000,  le=500_000)
    home_value_usd:     float = Field(..., ge=15_000, le=1_500_000)
    year_built:         int   = Field(..., ge=1940,   le=2024)
    bedrooms:           int   = Field(..., ge=0,      le=8)
    people_in_home:     int   = Field(..., ge=1,      le=12)
    neighbourhood:      str
 
    @model_validator(mode="after")
    def check_lookups(self) -> "FriendlyDataPoint":
        if self.city not in CA_CITIES:
            raise ValueError(f"Unknown city '{self.city}'.")
        if self.neighbourhood not in NEIGHBOURHOOD_POPULATION:
            raise ValueError(f"neighbourhood must be one of: {list(NEIGHBOURHOOD_POPULATION)}")
        return self
 
    def to_housing_point(self) -> "HousingDataPoint":
        lat, lng         = CA_CITIES[self.city]
        rooms, bedrms    = _rooms_from_bedrooms(self.bedrooms)
        return HousingDataPoint(
            med_inc       = round(self.annual_income_usd / 10_000, 4),
            house_age     = float(2024 - self.year_built),
            ave_rooms     = rooms,
            ave_bedrms    = bedrms,
            population    = NEIGHBOURHOOD_POPULATION[self.neighbourhood],
            ave_occup     = float(self.people_in_home),
            latitude      = lat,
            longitude     = lng,
            med_house_val = round(self.home_value_usd / 100_000, 4),
        )
 

 
class HousingDataPoint(BaseModel):
    med_inc:       float
    house_age:     float
    ave_rooms:     float
    ave_bedrms:    float
    population:    float
    ave_occup:     float
    latitude:      float
    longitude:     float
    med_house_val: float
 

 
class HousingDataResponse(BaseModel):
    id:            int
    med_inc:       float
    house_age:     float
    ave_rooms:     float
    ave_bedrms:    float
    population:    float
    ave_occup:     float
    latitude:      float
    longitude:     float
    med_house_val: float
    created_at:    datetime
    model_config = {"from_attributes": True}