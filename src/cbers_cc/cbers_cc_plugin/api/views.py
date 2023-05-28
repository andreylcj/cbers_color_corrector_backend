

from rest_flex_fields import FlexFieldsModelViewSet
from cbers_cc_plugin.api.serializers import (
    EmbeddingSerializer,
    ReferenceImageSerializer
)
from cbers_cc_plugin.models import (
    Embedding,
    ReferenceImage
)


class EmbeddingViewSet(FlexFieldsModelViewSet):
    serializer_class = EmbeddingSerializer
    queryset = Embedding.objects.all().order_by('id')
    Model = Embedding
    # filterset_class = EmbeddingFilters
    
    
class ReferenceImageViewSet(FlexFieldsModelViewSet):
    serializer_class = ReferenceImageSerializer
    queryset = ReferenceImage.objects.all().order_by('id')
    Model = ReferenceImage
    # filterset_class = ReferenceImageFilters