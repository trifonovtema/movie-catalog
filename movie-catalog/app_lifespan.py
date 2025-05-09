import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

# from api.api_v1.movie_catalog.crud import storage

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.warning("Starting app")
    # storage.init_storage()
    yield
    logger.warning("Stopping app")
