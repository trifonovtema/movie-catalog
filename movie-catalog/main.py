import logging

from fastapi import (
    FastAPI,
    Request,
)

from api import router as api_router
from core import config

logging.basicConfig(
    level=config.LOG_LEVEL,
    format=config.LOG_FORMAT,
)

app = FastAPI(
    title="Movie Catalog",
)

app.include_router(api_router)


@app.get("/")
async def root(
    request: Request,
):
    docs_url = request.url.replace(path="/docs")
    return {
        "message": "This is the root of the movie catalog API",
        "docs": str(docs_url),
    }
