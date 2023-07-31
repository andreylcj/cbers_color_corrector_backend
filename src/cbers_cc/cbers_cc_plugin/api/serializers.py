

from rest_flex_fields import FlexFieldsModelSerializer
from cbers_cc_plugin.models import (
    Tile512,
)


class Tile512Serializer(FlexFieldsModelSerializer):
    class Meta:
        model = Tile512
        fields = '__all__'
