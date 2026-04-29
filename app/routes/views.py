from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.templates import render_index

router = APIRouter(tags=["views"])


@router.get("/", response_class=HTMLResponse)
async def index():
    return HTMLResponse(content=render_index())