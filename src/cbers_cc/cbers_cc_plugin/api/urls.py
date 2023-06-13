

from rest_framework.routers import DefaultRouter
from .views import (
    EmbeddingViewSet,
    ReferenceImageViewSet,
)


router = DefaultRouter()
router.register(r'embeddings/', EmbeddingViewSet, basename='EmbbedingViewSet')
router.register(r'reference-images/', ReferenceImageViewSet, basename='ReferenceImageViewSet')
urlpatterns = router.urls
