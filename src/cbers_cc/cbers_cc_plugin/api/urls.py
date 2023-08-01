

from rest_framework.routers import DefaultRouter
from .views import (
    Tile512ViewSet,
)


router = DefaultRouter()
router.register(r'tiles-512', Tile512ViewSet, basename='Tile512ViewSet')
urlpatterns = router.urls
