__all__ = ("router",)

from api.api_v1.movie_catalog.views.list_views import router
from api.api_v1.movie_catalog.views.detail_views import router as detail_router

router.include_router(detail_router)
