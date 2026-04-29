import os
from sqlalchemy import create_engine, Column, Integer, Float, DateTime, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime


DB_PATH = os.environ.get("DATABASE_URL", "sqlite:////tmp/user_data.db")

engine = create_engine(
    DB_PATH,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class UserDataPoint(Base):
    __tablename__ = "user_data"

    id = Column(Integer, primary_key=True, index=True)
    med_inc = Column(Float, nullable=False)
    house_age = Column(Float, nullable=False)
    ave_rooms = Column(Float, nullable=False)
    ave_bedrms = Column(Float, nullable=False)
    population = Column(Float, nullable=False)
    ave_occup = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    med_house_val = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()