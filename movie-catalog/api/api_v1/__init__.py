from fastapi import APIRouter
from api.api_v1.movie_catalog.views import router as movie_catalog_router

router = APIRouter(
    prefix="/v1",
)

router.include_router(movie_catalog_router)
