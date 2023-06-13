

from rest_flex_fields import FlexFieldsModelSerializer
from cbers_cc_plugin.models import (
    Embedding,
    ReferenceImage
)


class EmbeddingSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Embedding
        fields = '__all__'
    
    
class ReferenceImageSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = ReferenceImage
        fields = '__all__'
