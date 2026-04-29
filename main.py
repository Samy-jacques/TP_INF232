from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.db import init_db
from app.routes import api, views


app = FastAPI(
    title="California Housing Analytics Platform",
    description=(
        "Interactive data collection and visualization platform built on the "
        "California Housing dataset with user-submitted data and live ML regression."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(views.router)
app.include_router(api.router)


@app.on_event("startup")
async def on_startup():
    init_db()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)