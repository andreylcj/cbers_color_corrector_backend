

from rest_flex_fields import FlexFieldsModelViewSet
from cbers_cc_plugin.api.serializers import (
    Tile512Serializer,
)
from cbers_cc_plugin.models import (
    Tile512,
)
from rest_framework.decorators import action
from cbers_cc_plugin.resources.types import (
    Tile512GetSimilarRequest,
    Tile512GetSimilarResponse,
)
from rest_framework.response import Response
from typing import List, Dict
from django.db.models import F
import numpy as np


class Tile512ViewSet(FlexFieldsModelViewSet):
    serializer_class = Tile512Serializer
    queryset = Tile512.objects.all().order_by('id')
    Model = Tile512
    # filterset_class = EmbeddingFilters
    
    @action(
        detail=False, 
        methods=['GET'], 
        url_path=f'similar', 
        url_name='get_similar'
    )
    def get_similar(self, request, *args, **kwargs):
        request_data: Tile512GetSimilarRequest = request.data
        embedding: List[float] = request_data['embedding']
        distance_expression = sum((F('embedding') - val) ** 2 for val in embedding)
        similar_tile = Tile512.objects \
            .annotate(distance=distance_expression) \
            .order_by('distance') \
            .first()
        
        response_kwargs: Dict = {}
        
        if similar_tile is not None:
            response_data = Tile512GetSimilarResponse(
                cdf=similar_tile.cdf,
                similarity=np.sqrt(similar_tile.distance),
            )
            
        else:
            response_data = {'error': 'No similar tile found.'}
            response_kwargs['status'] = 400
        
        return Response(response_data, **response_kwargs)